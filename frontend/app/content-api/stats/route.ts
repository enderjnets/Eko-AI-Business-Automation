import { NextResponse } from "next/server";
import { readdir, readFile, stat } from "fs/promises";
import { join } from "path";

const OUTPUT_DIR = "/Users/enderj/EkoContentStudio/output";

export async function GET() {
  try {
    const files = await readdir(OUTPUT_DIR);
    const pipelineFiles = files.filter(
      (f) => f.startsWith("pipeline_") && f.endsWith(".json")
    );

    let totalVideos = 0;
    let totalDuration = 0;
    let totalSizeMb = 0;
    let publishedCount = 0;
    const byPlatform: Record<string, number> = {};

    for (const f of pipelineFiles) {
      try {
        const raw = await readFile(join(OUTPUT_DIR, f), "utf-8");
        const data = JSON.parse(raw);
        const scripts = data.stages?.content?.scripts || [];
        for (const s of scripts) {
          if (s.video_path) {
            totalVideos++;
            totalDuration += s.video_duration || 0;
            totalSizeMb += s.video_size_mb || 0;
          }
          if (s.video_url) {
            publishedCount++;
            const tags = s.tags || [];
            for (const tag of ["tiktok", "instagram", "facebook"]) {
              if (tags.includes(tag) || tags.includes(tag.toLowerCase())) {
                byPlatform[tag] = (byPlatform[tag] || 0) + 1;
              }
            }
          }
        }
        // Also count from publish stage if available
        const published = data.stages?.publish?.published || [];
        for (const p of published) {
          const results = p.posts?.results || {};
          for (const [chId, chRes] of Object.entries(results)) {
            if ((chRes as any)?.success) {
              byPlatform[chId] = (byPlatform[chId] || 0) + 1;
            }
          }
        }
      } catch {
        // skip malformed
      }
    }

    // Count briefs
    const configFiles = await readdir("/Users/enderj/EkoContentStudio/config");
    const briefCount = configFiles.filter(
      (f) => f.startsWith("brief_") && f.endsWith(".json")
    ).length;

    return NextResponse.json({
      total_pipelines: pipelineFiles.length,
      total_videos: totalVideos,
      total_duration_seconds: Math.round(totalDuration),
      total_size_mb: Math.round(totalSizeMb * 10) / 10,
      published_videos: publishedCount,
      total_briefs: briefCount,
      by_platform: byPlatform,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to compute stats" },
      { status: 500 }
    );
  }
}
