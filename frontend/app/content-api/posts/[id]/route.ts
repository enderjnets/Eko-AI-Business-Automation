import { NextResponse } from "next/server";
import { bufferGraphQL } from "@/lib/buffer-api";

export async function GET(
  _request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const query = `
      query {
        post(input: { id: "${params.id}" }) {
          id
          text
          status
          dueAt
          sentAt
          createdAt
          updatedAt
          channelId
          channelService
          channel { name }
          assets { source thumbnail mimeType }
          metadata { ... on PostMetadata { instagram { type shouldShareToFeed } facebook { type } tiktok { title } } }
          error { message }
          shareMode
          externalLink
          sharedNow
          tags
          notes
          allowedActions
        }
      }
    `;

    const data = await bufferGraphQL(query);
    return NextResponse.json({ post: data.post });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to fetch post" },
      { status: 500 }
    );
  }
}
