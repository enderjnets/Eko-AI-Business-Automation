import { NextRequest, NextResponse } from "next/server";
import { isAllowedOrigin } from "@/lib/origin-check";
import { getBufferKey } from "@/lib/buffer-key";
import { clearCache } from "@/lib/api-cache";

const MAX_BATCH = 50;
const PER_DELETE_GAP_MS = 400;

interface DeleteResult {
  id: string;
  ok: boolean;
  error?: string;
}

async function deleteOne(id: string): Promise<DeleteResult> {
  const query = `
    mutation {
      deletePost(input: { id: "${id}" }) {
        __typename
      }
    }
  `;

  const res = await fetch("https://api.buffer.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getBufferKey()}`,
    },
    body: JSON.stringify({ query }),
  });

  const body = await res.json().catch(() => null);

  if (!res.ok) {
    return { id, ok: false, error: `HTTP ${res.status}` };
  }
  if (body?.errors && body.errors.length > 0) {
    const msg = body.errors[0]?.message || "Buffer rejected delete";
    return { id, ok: false, error: msg };
  }
  return { id, ok: true };
}

function isRateLimitError(err: string | undefined): boolean {
  if (!err) return false;
  const e = err.toLowerCase();
  return (
    e.includes("rate_limit_exceeded") ||
    e.includes("rate limit") ||
    e.includes("too many requests") ||
    e.includes("http 429")
  );
}

export async function POST(req: NextRequest) {
  if (!isAllowedOrigin(req)) {
    return NextResponse.json(
      { error: "cross-origin request blocked" },
      { status: 403 }
    );
  }

  let payload: { ids?: unknown };
  try {
    payload = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid json body" }, { status: 400 });
  }

  const ids = Array.isArray(payload?.ids) ? payload.ids : null;
  if (!ids) {
    return NextResponse.json(
      { error: "body must be { ids: string[] }" },
      { status: 400 }
    );
  }

  const cleanIds = ids
    .filter((x): x is string => typeof x === "string" && x.length > 0 && x.length < 128)
    .slice(0, MAX_BATCH);

  if (cleanIds.length === 0) {
    return NextResponse.json(
      { error: "no valid ids provided" },
      { status: 400 }
    );
  }

  const deleted: string[] = [];
  const failed: { id: string; error: string }[] = [];
  let rateLimited = false;

  for (let i = 0; i < cleanIds.length; i++) {
    const id = cleanIds[i];
    const result = await deleteOne(id);
    if (result.ok) {
      deleted.push(id);
    } else {
      failed.push({ id, error: result.error || "unknown" });
      if (isRateLimitError(result.error)) {
        // Stop immediately; let the client retry the rest after the cool-off
        rateLimited = true;
        const remaining = cleanIds.slice(i + 1);
        for (const r of remaining) {
          failed.push({ id: r, error: "skipped: rate limit reached" });
        }
        break;
      }
    }
    // Throttle between calls so we do not trip Buffer mid-batch
    if (i < cleanIds.length - 1) {
      await new Promise((r) => setTimeout(r, PER_DELETE_GAP_MS));
    }
  }

  // Invalidate the snapshot cache so the next snapshot fetch returns the
  // post-delete state (otherwise the 5-min cache would resurrect them).
  if (deleted.length > 0) {
    clearCache("buffer:snapshot:");
  }

  return NextResponse.json({
    deleted,
    failed,
    rate_limited: rateLimited,
    total: cleanIds.length,
  });
}
