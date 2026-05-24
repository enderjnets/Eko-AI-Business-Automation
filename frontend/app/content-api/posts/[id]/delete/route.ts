import { NextRequest, NextResponse } from "next/server";
import { isAllowedOrigin } from "@/lib/origin-check";
import { bufferGraphQL } from "@/lib/buffer-api";
import { clearCache } from "@/lib/api-cache";

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  if (!isAllowedOrigin(request)) {
    return NextResponse.json(
      { error: "cross-origin request blocked" },
      { status: 403 }
    );
  }
  try {
    const query = `
      mutation {
        deletePost(input: { id: "${params.id}" }) {
          __typename
        }
      }
    `;

    const data = await bufferGraphQL(query);
    clearCache("buffer:snapshot:");
    return NextResponse.json({ result: data.deletePost });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to delete post" },
      { status: 500 }
    );
  }
}
