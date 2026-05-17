import { NextResponse } from "next/server";
import { getCached, setCache } from "@/lib/api-cache";

const BUFFER_API_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

async function getOrgId() {
  const cached = getCached<string>("buffer:orgId");
  if (cached) return cached;

  const res = await fetch("https://api.buffer.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${BUFFER_API_KEY}`,
    },
    body: JSON.stringify({
      query: `{ account { organizations { id } } }`,
    }),
  });
  const data = await res.json();
  const orgId = data.data?.account?.organizations?.[0]?.id || "";
  if (orgId) setCache("buffer:orgId", orgId, 300000);
  return orgId;
}

async function bufferGraphQL(query: string) {
  const cacheKey = "buffer:gql:" + Buffer.from(query).toString("base64").slice(0, 64);
  const cached = getCached<any>(cacheKey);
  if (cached) return cached;

  const res = await fetch("https://api.buffer.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${BUFFER_API_KEY}`,
    },
    body: JSON.stringify({ query }),
  });

  const data = await res.json();
  if (data.errors) {
    const stale = getCached<any>(cacheKey + ":stale");
    if (stale) return stale;
    throw new Error(data.errors[0].message);
  }

  setCache(cacheKey, data.data, 30000);
  setCache(cacheKey + ":stale", data.data, 300000);
  return data.data;
}

export async function GET() {
  try {
    const orgId = await getOrgId();

    // Get channels first
    const channelsData = await bufferGraphQL(`
      query {
        channels(input: { organizationId: "${orgId}" }) {
          id
          name
          service
        }
      }
    `);

    const channels = channelsData.channels || [];
    const channelIds = channels.map((c: any) => c.id);

    if (channelIds.length === 0) {
      return NextResponse.json({ limits: [] });
    }

    const today = new Date().toISOString().split("T")[0];

    const limitsData = await bufferGraphQL(`
      query {
        dailyPostingLimits(input: {
          organizationId: "${orgId}"
          channelIds: [${channelIds.map((id: string) => `"${id}"`).join(", ")}]
          date: "${today}"
        }) {
          channelId
          sent
          scheduled
          limit
        }
      }
    `);

    const limits = (limitsData.dailyPostingLimits || []).map((l: any) => {
      const ch = channels.find((c: any) => c.id === l.channelId);
      return { ...l, name: ch?.name, service: ch?.service };
    });

    return NextResponse.json({ limits });
  } catch (err: any) {
    const staleLimits = getCached<any>("buffer:limits:stale");
    if (staleLimits) {
      return NextResponse.json({
        limits: staleLimits,
        stale: true,
        error: err.message,
      });
    }
    return NextResponse.json(
      { error: err.message || "Failed to fetch limits" },
      { status: 500 }
    );
  }
}
