/**
 * Unified Buffer snapshot — channels + posts + dailyPostingLimits in one call.
 * All Content Studio tabs read from this single endpoint to minimize Buffer API hits.
 *
 * Channels fallback: in dev / cold start / rate-limit, Buffer can return an
 * empty channels array. We persist the last-known channels to disk so that
 * the Monitor / PublishModal still know which networks are configured.
 */
import { NextRequest, NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";
import os from "os";
import {
  bufferQuery,
  getOrgId,
  getRateLimitHint,
} from "@/lib/buffer";

const CHANNELS_FALLBACK_FILE = path.join(
  os.tmpdir(),
  "eko-buffer-channels.json",
);

// Ultimate fallback for cold-starts before any successful snapshot has
// populated the disk cache. These are the channels we know are configured
// for the Eko AI org — they rarely change. If they do, the disk cache will
// overwrite them the next time Buffer responds successfully.
const HARDCODED_CHANNELS = [
  {
    id: "6a04fa5a090476fb9918d428",
    name: "ekoaiauto",
    service: "tiktok",
    isDisconnected: false,
  },
  {
    id: "6a04ff43090476fb9918e4c1",
    name: "ekoaiauto",
    service: "instagram",
    isDisconnected: false,
  },
  {
    id: "6a050305090476fb9918f5a0",
    name: "Eko Ai Automation",
    service: "facebook",
    isDisconnected: false,
  },
];

interface PersistedChannels {
  channels: Array<{
    id: string;
    name: string;
    service: string;
    isDisconnected: boolean;
  }>;
  saved_at: string;
}

async function loadFallbackChannels(): Promise<PersistedChannels | null> {
  try {
    const raw = await fs.readFile(CHANNELS_FALLBACK_FILE, "utf-8");
    return JSON.parse(raw) as PersistedChannels;
  } catch {
    return {
      channels: HARDCODED_CHANNELS,
      saved_at: "hardcoded",
    };
  }
}

async function saveFallbackChannels(channels: any[]) {
  try {
    await fs.writeFile(
      CHANNELS_FALLBACK_FILE,
      JSON.stringify(
        { channels, saved_at: new Date().toISOString() },
        null,
        2,
      ),
      "utf-8",
    );
  } catch {
    // best-effort; ignore disk errors
  }
}

// Buffer hard-caps pagination at 100 items per request. Asking for more
// returns `{ errors: [{ message: "Pagination limit exceeded. Maximum 100 items..." }] }`
// which our bufferQuery swallowed silently — every tab rendered as "empty".
const BUFFER_MAX_FIRST = 100;

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const rawLimit = parseInt(searchParams.get("limit") || "100", 10);
  const postLimit = Math.min(
    Math.max(Number.isFinite(rawLimit) ? rawLimit : 100, 1),
    BUFFER_MAX_FIRST,
  );

  try {
    const orgId = await getOrgId();

    if (!orgId) {
      const hint = getRateLimitHint();
      const fallback = await loadFallbackChannels();
      return NextResponse.json(
        {
          channels: fallback?.channels || [],
          posts: [],
          limits: [],
          stale: !!fallback,
          rate_limited: !!hint,
          rate_limit: hint
            ? { window: hint.window, reset_at: hint.resetEstimate }
            : null,
          error: hint
            ? "Buffer API rate-limited — showing cached channels only."
            : "No organization id available.",
        },
        { status: 200 }
      );
    }

    const today = new Date().toISOString().split("T")[0];

    // Single GraphQL with three top-level fields — Buffer batches them server-side.
    const query = `
      query Snapshot {
        snapshot_channels: channels(input: { organizationId: "${orgId}" }) {
          id
          name
          service
          isDisconnected
        }
        snapshot_posts: posts(
          input: {
            organizationId: "${orgId}"
            filter: { status: [draft, needs_approval, scheduled, sending, sent, error] }
            sort: [{ field: createdAt, direction: desc }]
          }
          first: ${postLimit}
        ) {
          edges {
            node {
              id
              text
              status
              dueAt
              sentAt
              createdAt
              channelId
              channelService
              channel { name }
              assets { source thumbnail mimeType }
              error { message }
              externalLink
            }
          }
          pageInfo { hasNextPage endCursor }
        }
      }
    `;

    const result = await bufferQuery<any>(
      query,
      `buffer:snapshot:v2:${orgId}:${postLimit}`,
      5 * 60 * 1000
    );

    // If bufferQuery returned null data without rate-limit, propagate so the
    // UI can render a banner instead of an empty list (Buffer errors are
    // otherwise swallowed by the cache layer).
    if (!result.data && !result.rateLimited && result.error) {
      const fallback = await loadFallbackChannels();
      return NextResponse.json(
        {
          channels: fallback?.channels || [],
          posts: [],
          limits: [],
          stale: !!fallback,
          rate_limited: false,
          rate_limit: null,
          error: result.error,
          fetched_at: new Date().toISOString(),
        },
        { status: 200 }
      );
    }

    let channels = result.data?.snapshot_channels || [];
    const rawPosts = result.data?.snapshot_posts?.edges?.map((e: any) => e.node) || [];
    const pageInfo = result.data?.snapshot_posts?.pageInfo || {
      hasNextPage: false,
      endCursor: null,
    };

    // Refresh disk fallback every time we get fresh channels (channels rarely
    // change but we keep the file warm). If channels came back empty AND we
    // are rate-limited / stale, restore from disk so the UI still works.
    if (channels.length > 0) {
      saveFallbackChannels(channels).catch(() => {});
    } else if (result.rateLimited || result.stale) {
      const fallback = await loadFallbackChannels();
      if (fallback?.channels?.length) {
        channels = fallback.channels;
      }
    }

    // Limits: separate query because dailyPostingLimits has different shape.
    // Skip if we have no channel ids OR if rate-limited (avoid extra call).
    let limits: any[] = [];
    if (channels.length > 0 && !result.rateLimited) {
      const activeIds = channels
        .filter((c: any) => !c.isDisconnected)
        .map((c: any) => c.id);
      if (activeIds.length > 0) {
        const limitsResult = await bufferQuery<any>(
          `{
            dailyPostingLimits(input: {
              organizationId: "${orgId}"
              channelIds: [${activeIds.map((id: string) => `"${id}"`).join(", ")}]
              date: "${today}"
            }) {
              channelId
              sent
              scheduled
              limit
            }
          }`,
          `buffer:limits:v2:${orgId}:${today}`,
          5 * 60 * 1000
        );
        const rawLimits = limitsResult.data?.dailyPostingLimits || [];
        limits = rawLimits.map((l: any) => {
          const ch = channels.find((c: any) => c.id === l.channelId);
          return { ...l, name: ch?.name, service: ch?.service };
        });
      }
    } else if (result.rateLimited) {
      // Try to serve stale limits if available
      const stale = await bufferQuery<any>(
        `__unused__`,
        `buffer:limits:v2:${orgId}:${today}`,
        0
      );
      if (stale.data?.dailyPostingLimits) {
        limits = stale.data.dailyPostingLimits.map((l: any) => {
          const ch = channels.find((c: any) => c.id === l.channelId);
          return { ...l, name: ch?.name, service: ch?.service };
        });
      }
    }

    return NextResponse.json({
      channels,
      posts: rawPosts,
      limits,
      pageInfo,
      stale: result.stale,
      rate_limited: result.rateLimited,
      rate_limit: result.rateLimited
        ? {
            window: result.rateLimitWindow,
            reset_at: result.rateLimitResetAt,
          }
        : null,
      fetched_at: new Date().toISOString(),
    });
  } catch (err: any) {
    const hint = getRateLimitHint();
    return NextResponse.json(
      {
        channels: [],
        posts: [],
        limits: [],
        rate_limited: !!hint,
        rate_limit: hint
          ? { window: hint.window, reset_at: hint.resetEstimate }
          : null,
        error: err.message || "Unknown error",
      },
      { status: 200 }
    );
  }
}
