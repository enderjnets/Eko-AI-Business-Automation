import { NextRequest, NextResponse } from "next/server";
import { getCached, setCache } from "@/lib/api-cache";

const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

async function getOrgId() {
  const cached = getCached<string>("buffer:orgId");
  if (cached) return cached;

  const res = await fetch("https://api.buffer.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${BUFFER_API_KEY}`,
    },
    body: JSON.stringify({
      query: `{ account { organizations { id } } }`,
    }),
  });
  const data = await res.json();
  const orgId = data.data?.account?.organizations?.[0]?.id || "";
  if (orgId) setCache("buffer:orgId", orgId, 300000);
  return orgId;
}

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
    const stale = getCached<any>(cacheKey + ":stale");
    if (stale) return stale;
    throw new Error(data.errors[0].message);
  }

  setCache(cacheKey, data.data, 30000);
  setCache(cacheKey + ":stale", data.data, 300000);
  return data.data;
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const statusFilter = searchParams.get("status") || "all";
    const channelId = searchParams.get("channelId");
    const first = parseInt(searchParams.get("limit") || "100", 10);
    const after = searchParams.get("cursor") || null;
    const startDate = searchParams.get("startDate");
    const endDate = searchParams.get("endDate");

    const orgId = await getOrgId();

    // Build status filter
    let statusArray = "[draft, needs_approval, scheduled, sending, sent, error]";
    if (statusFilter !== "all") {
      statusArray = `[${statusFilter}]`;
    }

    // Build channel filter
    const channelFilter = channelId ? `, channelIds: ["${channelId}"]` : "";

    const query = `
      query {
        posts(
          input: {
            organizationId: "${orgId}"
            filter: { status: ${statusArray}${channelFilter} }
            sort: [{ field: createdAt, direction: desc }]
          }
          first: ${first}
          ${after ? `after: "${after}"` : ""}
        ) {
          edges {
            node {
              id
              text
              status
              dueAt
              sentAt
              createdAt
              channelId
              channelService
              channel { name }
              assets { source thumbnail mimeType }
              error { message }
              shareMode
              externalLink
              sharedNow
            }
            cursor
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    `;

    const data = await bufferGraphQL(query);
    let posts = data.posts?.edges?.map((e: any) => e.node) || [];

    // Client-side date range filter
    if (startDate || endDate) {
      const start = startDate ? new Date(startDate) : null;
      const end = endDate ? new Date(endDate) : null;
      if (end) end.setHours(23, 59, 59, 999);

      posts = posts.filter((post: any) => {
        const postDate = post.dueAt
          ? new Date(post.dueAt)
          : post.sentAt
          ? new Date(post.sentAt)
          : new Date(post.createdAt);
        if (start && postDate < start) return false;
        if (end && postDate > end) return false;
        return true;
      });
    }

    return NextResponse.json({
      posts,
      pageInfo: data.posts?.pageInfo || { hasNextPage: false, endCursor: null },
    });
  } catch (err: any) {
    const stalePosts = getCached<any>("buffer:posts:stale");
    if (stalePosts) {
      return NextResponse.json({
        posts: stalePosts,
        stale: true,
        error: err.message,
      });
    }
    return NextResponse.json(
      { error: err.message || "Failed to fetch posts" },
      { status: 500 }
    );
  }
}
