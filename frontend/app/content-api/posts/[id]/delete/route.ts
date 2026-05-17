import { NextResponse } from "next/server";
import { bufferGraphQL } from "@/lib/buffer-api";

export async function POST(
  _request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const query = `
      mutation {
        deletePost(input: { id: "${params.id}" }) {
          __typename
        }
      }
    `;

    const data = await bufferGraphQL(query);
    return NextResponse.json({ result: data.deletePost });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to delete post" },
      { status: 500 }
    );
  }
}
