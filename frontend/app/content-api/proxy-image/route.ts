import { NextRequest, NextResponse } from "next/server";
import { getBufferKey, isAllowedProxyHost, isBufferHost } from "@/lib/buffer-key";

const MAX_BYTES = 25 * 1024 * 1024; // 25MB hard cap to prevent memory blowup
const FETCH_TIMEOUT_MS = 8000;

function errorPlaceholder(status: "expired" | "missing" | "blocked", upstreamStatus?: number) {
  // We intentionally return 404 (not 200 + 1x1 PNG like the old impl) so the
  // <img> onError handler fires cleanly and the UI can show a real placeholder
  // with a meaningful label. The diagnostic header lets the frontend
  // distinguish "media expired" from "host blocked" without parsing pixels.
  return new NextResponse(null, {
    status: 404,
    headers: {
      "X-Eko-Proxy-Status": status,
      ...(upstreamStatus ? { "X-Eko-Upstream-Status": String(upstreamStatus) } : {}),
      "Cache-Control": "no-store",
    },
  });
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const imageUrl = searchParams.get("url");

  if (!imageUrl) {
    return NextResponse.json({ error: "Missing url param" }, { status: 400 });
  }

  let parsed: URL;
  try {
    parsed = new URL(imageUrl);
  } catch {
    return NextResponse.json({ error: "Invalid url" }, { status: 400 });
  }

  if (parsed.protocol !== "https:" && parsed.protocol !== "http:") {
    return NextResponse.json({ error: "Only http(s) URLs allowed" }, { status: 400 });
  }

  if (!isAllowedProxyHost(parsed.hostname)) {
    return errorPlaceholder("blocked");
  }

  const headers: Record<string, string> = {
    Accept: "image/*",
  };

  // Only send the Buffer credential to actual Buffer hosts. Stops the credential
  // from leaking via SSRF to any other allowed host (e.g. our own ROG domain).
  if (isBufferHost(parsed.hostname)) {
    headers.Authorization = `Bearer ${getBufferKey()}`;
    headers.Referer = "https://publish.buffer.com/";
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    const res = await fetch(imageUrl, {
      headers,
      signal: controller.signal,
    });

    if (!res.ok) {
      // Buffer returns 422 when the upstream source (e.g. an expired temp file
      // host) is gone. Surface that as "expired" so the UI shows the right
      // label instead of a generic broken image.
      const status = res.status === 422 || res.status === 404 || res.status === 410
        ? "expired"
        : "missing";
      return errorPlaceholder(status, res.status);
    }

    const lenHeader = res.headers.get("content-length");
    if (lenHeader && parseInt(lenHeader, 10) > MAX_BYTES) {
      return errorPlaceholder("blocked", 413);
    }

    const contentType = res.headers.get("content-type") || "image/jpeg";
    if (!contentType.startsWith("image/")) {
      return errorPlaceholder("blocked", 415);
    }

    const arrayBuffer = await res.arrayBuffer();
    if (arrayBuffer.byteLength > MAX_BYTES) {
      return errorPlaceholder("blocked", 413);
    }

    return new NextResponse(arrayBuffer, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=3600",
        "X-Eko-Proxy-Status": "ok",
      },
    });
  } catch (err: any) {
    const isAbort = err?.name === "AbortError";
    return errorPlaceholder(isAbort ? "missing" : "missing");
  } finally {
    clearTimeout(timer);
  }
}
