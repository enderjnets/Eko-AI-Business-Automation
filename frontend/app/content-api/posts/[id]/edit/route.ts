import { NextRequest, NextResponse } from "next/server";
import { bufferGraphQL } from "@/lib/buffer-api";

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
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
    return NextResponse.json({ result: data.editPost });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to edit post" },
      { status: 500 }
    );
  }
}
