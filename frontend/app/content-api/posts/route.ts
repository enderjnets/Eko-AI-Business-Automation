import { NextRequest, NextResponse } from "next/server";
import { bufferGraphQL, getOrganizationId } from "@/lib/buffer-api";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const statusFilter = searchParams.get("status") || "all";
    const channelId = searchParams.get("channelId");
    const first = parseInt(searchParams.get("limit") || "200", 10);
    const after = searchParams.get("cursor") || null;
    const startDate = searchParams.get("startDate");
    const endDate = searchParams.get("endDate");

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

    // Client-side date range filter (Buffer GraphQL doesn't support date range on posts)
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
    return NextResponse.json(
      { error: err.message || "Failed to fetch posts" },
      { status: 500 }
    );
  }
}
