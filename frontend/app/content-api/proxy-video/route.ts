import { NextRequest, NextResponse } from "next/server";
import { isAllowedProxyHost, isBufferHost, getBufferKey } from "@/lib/buffer-key";

const MAX_BYTES = 250 * 1024 * 1024; // 250MB cap — videos can be larger than images but still bounded
const FETCH_TIMEOUT_MS = 30000;

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const videoUrl = searchParams.get("url");

  if (!videoUrl) {
    return NextResponse.json({ error: "Missing url param" }, { status: 400 });
  }

  let parsed: URL;
  try {
    parsed = new URL(videoUrl);
  } catch {
    return NextResponse.json({ error: "Invalid url" }, { status: 400 });
  }

  if (parsed.protocol !== "https:" && parsed.protocol !== "http:") {
    return NextResponse.json({ error: "Only http(s) URLs allowed" }, { status: 400 });
  }

  if (!isAllowedProxyHost(parsed.hostname)) {
    return NextResponse.json({ error: "Host not allowed" }, { status: 403 });
  }

  const headers: Record<string, string> = {
    Accept: "video/mp4,video/*,*/*",
  };

  if (isBufferHost(parsed.hostname)) {
    headers.Authorization = `Bearer ${getBufferKey()}`;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    const res = await fetch(videoUrl, { headers, signal: controller.signal });

    if (!res.ok) {
      return NextResponse.json(
        { error: `Failed to fetch video: ${res.status}` },
        { status: 502 }
      );
    }

    const lenHeader = res.headers.get("content-length");
    if (lenHeader && parseInt(lenHeader, 10) > MAX_BYTES) {
      return NextResponse.json({ error: "Video too large" }, { status: 413 });
    }

    const contentType = res.headers.get("content-type") || "video/mp4";
    if (!contentType.startsWith("video/") && !contentType.startsWith("application/octet-stream")) {
      return NextResponse.json({ error: "Not a video" }, { status: 415 });
    }

    const arrayBuffer = await res.arrayBuffer();
    if (arrayBuffer.byteLength > MAX_BYTES) {
      return NextResponse.json({ error: "Video too large" }, { status: 413 });
    }

    return new NextResponse(arrayBuffer, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=3600",
        "Accept-Ranges": "bytes",
      },
    });
  } catch (err: any) {
    const isAbort = err?.name === "AbortError";
    return NextResponse.json(
      { error: isAbort ? "Upstream timeout" : (err.message || "Proxy failed") },
      { status: isAbort ? 504 : 500 }
    );
  } finally {
    clearTimeout(timer);
  }
}
