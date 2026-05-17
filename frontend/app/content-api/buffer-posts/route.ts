import { NextResponse } from "next/server";
import { getCached, setCache } from "@/lib/api-cache";

const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

async function bufferGraphQL(query: string) {
  const cacheKey = "buffer:gql:" + Buffer.from(query).toString("base64").slice(0, 64);
  const cached = getCached<any>(cacheKey);
  if (cached) return cached;

  const res = await fetch("https://api.buffer.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${BUFFER_API_KEY}`,
    },
    body: JSON.stringify({ query }),
  });

  const data = await res.json();
  if (data.errors) {
    // Check if cached stale data exists (graceful degradation)
    const stale = getCached<any>(cacheKey + ":stale");
    if (stale) return stale;
    throw new Error(data.errors[0].message);
  }

  setCache(cacheKey, data.data, 30000);
  setCache(cacheKey + ":stale", data.data, 300000); // 5 min stale
  return data.data;
}

export async function GET() {
  try {
    // 1. Get channels
    const channelsQuery = `
      query {
        account {
          organizations {
            channels {
              id
              name
              service
              isDisconnected
            }
          }
        }
      }
    `;

    const channelsData = await bufferGraphQL(channelsQuery);
    const channels =
      channelsData?.account?.organizations?.flatMap(
        (org: any) => org.channels || []
      ) || [];

    const activeChannelIds = channels
      .filter((ch: any) => !ch.isDisconnected)
      .map((ch: any) => ch.id);

    if (activeChannelIds.length === 0) {
      return NextResponse.json({ channels, posts: [] });
    }

    // 2. Get actual posts with status
    const postsQuery = `
      query {
        posts(
          input: {
            filter: {
              channelIds: [${activeChannelIds
                .map((id: string) => `"${id}"`)
                .join(", ")}]
              status: [scheduled, sent, sending, error]
            }
          }
          first: 100
        ) {
          edges {
            node {
              id
              text
              status
              dueAt
              sentAt
              channelId
              channelService
              channel { name }
            }
          }
        }
      }
    `;

    const postsData = await bufferGraphQL(postsQuery);
    const posts = postsData?.posts?.edges?.map((e: any) => e.node) || [];

    return NextResponse.json({ channels, posts });
  } catch (err: any) {
    // Return stale cached data if available during rate limit
    const stalePosts = getCached<any>("buffer:posts:stale");
    const staleChannels = getCached<any>("buffer:channels:stale");
    if (stalePosts || staleChannels) {
      return NextResponse.json({
        channels: staleChannels || [],
        posts: stalePosts || [],
        stale: true,
        error: err.message,
      });
    }
    return NextResponse.json(
      { error: err.message || "Buffer request failed" },
      { status: 500 }
    );
  }
}
