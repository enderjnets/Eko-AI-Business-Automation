/**
 * POST /content-api/publish
 *
 * Publishes a video (or queues / schedules it) to one or more Buffer channels
 * (TikTok / Instagram / Facebook). Returns per-channel result so the UI can
 * show success / error individually.
 *
 * Body:
 *   {
 *     videoUrl: string           // public URL to the .mp4
 *     thumbnailUrl?: string      // public URL to a JPG/PNG
 *     caption: string            // default caption used on every channel...
 *     captionsByChannel?: {      // ...unless an override exists for the channel
 *       [channelId: string]: string
 *     }
 *     channels: Array<{
 *       id: string               // Buffer channel id
 *       service: "tiktok" | "instagram" | "facebook"
 *     }>
 *     mode: "shareNow" | "addToQueue" | "customScheduled"
 *     dueAt?: string             // ISO datetime (required when mode = customScheduled)
 *     title?: string             // optional, used as TikTok title
 *     instagramType?: "reel" | "post"   // default: reel
 *     facebookType?: "reel" | "post"    // default: reel
 *   }
 */
import { NextRequest, NextResponse } from "next/server";
import { isAllowedOrigin } from "@/lib/origin-check";
import { getBufferKey } from "@/lib/buffer-key";

interface PublishChannel {
  id: string;
  service: "tiktok" | "instagram" | "facebook";
}

interface PublishBody {
  videoUrl: string;
  thumbnailUrl?: string;
  caption: string;
  captionsByChannel?: Record<string, string>;
  channels: PublishChannel[];
  mode: "shareNow" | "addToQueue" | "customScheduled";
  dueAt?: string;
  title?: string;
  instagramType?: "reel" | "post";
  facebookType?: "reel" | "post";
}

interface ChannelResult {
  channelId: string;
  service: string;
  ok: boolean;
  postId?: string;
  status?: string;
  error?: string;
}

function escapeGraphQLString(s: string): string {
  // Triple-quoted block strings need escaping of triple quotes only.
  return s.replace(/"""/g, '\\"""');
}

function buildMetadataBlock(
  service: PublishChannel["service"],
  body: PublishBody
): string {
  const igType = body.instagramType || "reel";
  const fbType = body.facebookType || "reel";
  const title = body.title || "";

  if (service === "instagram") {
    return `instagram: { type: ${igType}, shouldShareToFeed: true }`;
  }
  if (service === "facebook") {
    return `facebook: { type: ${fbType} }`;
  }
  if (service === "tiktok") {
    if (!title) return `tiktok: { title: "" }`;
    return `tiktok: { title: "${title.replace(/"/g, '\\"').slice(0, 150)}" }`;
  }
  return "";
}

async function bufferMutation(query: string): Promise<any> {
  const res = await fetch("https://api.buffer.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getBufferKey()}`,
    },
    body: JSON.stringify({ query }),
  });
  const data = await res.json();
  if (data.errors && data.errors.length) {
    throw new Error(data.errors[0].message);
  }
  return data.data;
}

async function publishToChannel(
  body: PublishBody,
  channel: PublishChannel
): Promise<ChannelResult> {
  try {
    const text =
      (body.captionsByChannel && body.captionsByChannel[channel.id]) ||
      body.caption ||
      "";
    const metadataBlock = buildMetadataBlock(channel.service, body);
    const dueAtPart =
      body.mode === "customScheduled" && body.dueAt
        ? `dueAt: "${body.dueAt}"`
        : "";
    const thumbPart = body.thumbnailUrl
      ? `thumbnailUrl: "${body.thumbnailUrl}"`
      : "";
    const videoTitle = body.title
      ? `metadata: { title: "${body.title.replace(/"/g, '\\"').slice(0, 150)}" }`
      : "";

    const query = `
      mutation Publish {
        createPost(input: {
          channelId: "${channel.id}"
          schedulingType: automatic
          mode: ${body.mode}
          ${dueAtPart}
          text: """${escapeGraphQLString(text)}"""
          assets: [{
            video: {
              url: "${body.videoUrl}"
              ${thumbPart}
              ${videoTitle}
            }
          }]
          metadata: { ${metadataBlock} }
          source: "content-studio"
          aiAssisted: true
        }) {
          __typename
          ... on PostActionSuccess {
            post { id status text dueAt }
          }
          ... on MutationError {
            message
          }
        }
      }
    `;

    const data = await bufferMutation(query);
    const result = data?.createPost;
    if (!result) {
      return {
        channelId: channel.id,
        service: channel.service,
        ok: false,
        error: "No createPost result from Buffer",
      };
    }
    if (result.__typename === "PostActionSuccess" && result.post) {
      return {
        channelId: channel.id,
        service: channel.service,
        ok: true,
        postId: result.post.id,
        status: result.post.status,
      };
    }
    return {
      channelId: channel.id,
      service: channel.service,
      ok: false,
      error: result.message || `Buffer returned ${result.__typename}`,
    };
  } catch (err: any) {
    return {
      channelId: channel.id,
      service: channel.service,
      ok: false,
      error: err.message || "Unknown error",
    };
  }
}

export async function POST(request: NextRequest) {
  if (!isAllowedOrigin(request)) {
    return NextResponse.json(
      { error: "cross-origin request blocked" },
      { status: 403 }
    );
  }
  try {
    const body = (await request.json()) as PublishBody;

    if (!body.videoUrl) {
      return NextResponse.json(
        { error: "videoUrl is required" },
        { status: 400 }
      );
    }
    if (!Array.isArray(body.channels) || body.channels.length === 0) {
      return NextResponse.json(
        { error: "At least one channel is required" },
        { status: 400 }
      );
    }
    if (!["shareNow", "addToQueue", "customScheduled"].includes(body.mode)) {
      return NextResponse.json(
        { error: "Invalid mode" },
        { status: 400 }
      );
    }
    if (body.mode === "customScheduled" && !body.dueAt) {
      return NextResponse.json(
        { error: "dueAt is required when mode = customScheduled" },
        { status: 400 }
      );
    }

    const results = await Promise.all(
      body.channels.map((ch) => publishToChannel(body, ch))
    );

    const ok = results.every((r) => r.ok);
    const anyOk = results.some((r) => r.ok);

    return NextResponse.json(
      {
        ok,
        anyOk,
        results,
        publishedAt: new Date().toISOString(),
      },
      { status: ok ? 200 : 207 }
    );
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to publish" },
      { status: 500 }
    );
  }
}
