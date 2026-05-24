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
    const body = await request.json();
    const { text } = body;

    if (!text) {
      return NextResponse.json(
        { error: "text is required" },
        { status: 400 }
      );
    }

    const query = `
      mutation {
        editPost(input: { id: "${params.id}", text: """${text.replace(/"/g, '\\"')}""" }) {
          ... on PostActionSuccess {
            post {
              id
              text
              status
            }
          }
          ... on MutationError {
            message
          }
        }
      }
    `;

    const data = await bufferGraphQL(query);
    clearCache("buffer:snapshot:");
    return NextResponse.json({ result: data.editPost });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to edit post" },
      { status: 500 }
    );
  }
}
