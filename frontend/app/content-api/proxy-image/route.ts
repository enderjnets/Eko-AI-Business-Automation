import { NextRequest, NextResponse } from "next/server";

const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const imageUrl = searchParams.get("url");

  if (!imageUrl) {
    return NextResponse.json({ error: "Missing url param" }, { status: 400 });
  }

  try {
    const res = await fetch(imageUrl, {
      headers: {
        Authorization: `Bearer ${BUFFER_API_KEY}`,
        Referer: "https://publish.buffer.com/",
      },
    });

    if (!res.ok) {
      return NextResponse.json(
        { error: `Failed to fetch image: ${res.status}` },
        { status: res.status }
      );
    }

    const contentType = res.headers.get("content-type") || "image/jpeg";
    const arrayBuffer = await res.arrayBuffer();

    return new NextResponse(arrayBuffer, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=3600",
      },
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Proxy failed" },
      { status: 500 }
    );
  }
}
