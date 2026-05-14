import { NextResponse } from "next/server";
import { readdir, readFile } from "fs/promises";
import { join } from "path";

const OUTPUT_DIR = "/Users/enderj/EkoContentStudio/output";

export async function GET() {
  try {
    const files = await readdir(OUTPUT_DIR);
    const pipelineFiles = files
      .filter((f) => f.startsWith("pipeline_") && f.endsWith(".json"))
      .sort()
      .reverse();

    const pipelines = await Promise.all(
      pipelineFiles.slice(0, 20).map(async (f) => {
        const raw = await readFile(join(OUTPUT_DIR, f), "utf-8");
        const data = JSON.parse(raw);
        return {
          filename: f,
          started_at: data.started_at,
          business_name: data.business_name,
          stages: data.stages
            ? Object.fromEntries(
                Object.entries(data.stages).map(([k, v]: [string, any]) => [
                  k,
                  { status: v?.status },
                ])
              )
            : {},
          paperclip_issue_id: data.paperclip_issue_id,
        };
      })
    );

    return NextResponse.json({ pipelines });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to load pipelines" },
      { status: 500 }
    );
  }
}
