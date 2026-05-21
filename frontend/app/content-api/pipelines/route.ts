/**
 * GET /content-api/pipelines
 * Proxies to the pipeline-api `/pipelines` endpoint inside the `eko-pipeline`
 * container. The pipeline JSONs live on the ROG at `~/EkoContentStudio/output`
 * and are mounted into `eko-pipeline:/app/output` — no need for the frontend
 * container to have direct filesystem access.
 *
 * Previous version read from `/Users/enderj/EkoContentStudio/output` via a
 * volume mount that broke when docker-compose was run with `sudo` and `~`
 * expanded to `/root` instead of `/home/enderj`.
 */
import { NextResponse } from "next/server";

const PIPELINE_API = process.env.PIPELINE_API_URL || "http://eko-pipeline:8002";

export async function GET(request: Request) {
  try {
    const url = new URL(request.url);
    const limit = url.searchParams.get("limit") || "30";
    const r = await fetch(`${PIPELINE_API}/pipelines?limit=${limit}`, {
      cache: "no-store",
    });
    if (!r.ok) {
      return NextResponse.json(
        { error: `Pipeline API returned ${r.status}` },
        { status: r.status }
      );
    }
    const data = await r.json();
    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to fetch pipelines" },
      { status: 500 }
    );
  }
}
