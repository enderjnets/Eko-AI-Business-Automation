import { NextResponse } from "next/server";

const BUFFER_API_URL = "https://api.buffer.com";
const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

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

    const channelsRes = await fetch(BUFFER_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${BUFFER_API_KEY}`,
      },
      body: JSON.stringify({ query: channelsQuery }),
    });

    const channelsData = await channelsRes.json();
    if (channelsData.errors) {
      return NextResponse.json(
        { error: channelsData.errors[0].message },
        { status: 502 }
      );
    }

    const channels =
      channelsData.data?.account?.organizations?.flatMap(
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
        posts(filter: { channelIds: [${activeChannelIds
          .map((id: string) => `"${id}"`)
          .join(", ")}], status: [scheduled, sent, sending, error] }) {
          posts {
            id
            text
            status
            dueAt
            sentAt
            channelId
          }
        }
      }
    `;

    const postsRes = await fetch(BUFFER_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${BUFFER_API_KEY}`,
      },
      body: JSON.stringify({ query: postsQuery }),
    });

    const postsData = await postsRes.json();
    if (postsData.errors) {
      return NextResponse.json(
        { error: postsData.errors[0].message },
        { status: 502 }
      );
    }

    const posts = postsData.data?.posts?.posts || [];

    return NextResponse.json({ channels, posts });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Buffer request failed" },
      { status: 500 }
    );
  }
}
