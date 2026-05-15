import { NextRequest, NextResponse } from "next/server";
import { bufferGraphQL, getOrganizationId } from "@/lib/buffer-api";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const statusFilter = searchParams.get("status") || "all";
    const channelId = searchParams.get("channelId");
    const first = parseInt(searchParams.get("limit") || "50", 10);
    const after = searchParams.get("cursor") || null;

    const orgId = await getOrganizationId();

    // Build status filter
    let statusArray = "[draft, needs_approval, scheduled, sending, sent, error]";
    if (statusFilter !== "all") {
      statusArray = `[${statusFilter}]`;
    }

    // Build channel filter
    const channelFilter = channelId ? `, channelIds: ["${channelId}"]` : "";

    const query = `
      query {
        posts(input: {
          organizationId: "${orgId}"
          filter: { status: ${statusArray}${channelFilter} }
          sort: [{ field: createdAt, direction: desc }]
          first: ${first}
          ${after ? `after: "${after}"` : ""}
        }) {
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
    return NextResponse.json({
      posts: data.posts?.edges?.map((e: any) => e.node) || [],
      pageInfo: data.posts?.pageInfo || { hasNextPage: false, endCursor: null },
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to fetch posts" },
      { status: 500 }
    );
  }
}
