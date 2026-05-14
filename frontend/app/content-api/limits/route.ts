import { NextResponse } from "next/server";
import { bufferGraphQL, getOrganizationId } from "@/lib/buffer-api";

export async function GET() {
  try {
    const orgId = await getOrganizationId();

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
    return NextResponse.json(
      { error: err.message || "Failed to fetch limits" },
      { status: 500 }
    );
  }
}
