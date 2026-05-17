import { NextRequest, NextResponse } from "next/server";

const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

// 1x1 transparent PNG
const TRANSPARENT_PNG = Buffer.from(
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
  "base64"
);

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
      // Return transparent PNG so <img> onError fires cleanly
      return new NextResponse(TRANSPARENT_PNG, {
        status: 200,
        headers: {
          "Content-Type": "image/png",
          "Cache-Control": "public, max-age=60",
        },
      });
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
    // Also return transparent PNG on network errors
    return new NextResponse(TRANSPARENT_PNG, {
      status: 200,
      headers: {
        "Content-Type": "image/png",
        "Cache-Control": "public, max-age=60",
      },
    });
  }
}
