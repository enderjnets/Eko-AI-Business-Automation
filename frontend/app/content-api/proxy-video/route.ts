import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const videoUrl = searchParams.get("url");

  if (!videoUrl) {
    return NextResponse.json({ error: "Missing url param" }, { status: 400 });
  }

  try {
    const res = await fetch(videoUrl, {
      headers: {
        Accept: "video/mp4,video/*,*/*",
      },
    });

    if (!res.ok) {
      return NextResponse.json(
        { error: `Failed to fetch video: ${res.status}` },
        { status: 502 }
      );
    }

    const contentType = res.headers.get("content-type") || "video/mp4";
    const arrayBuffer = await res.arrayBuffer();

    return new NextResponse(arrayBuffer, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=3600",
        "Accept-Ranges": "bytes",
      },
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Proxy failed" },
      { status: 500 }
    );
  }
}
