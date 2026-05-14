import { NextResponse } from "next/server";
import { readdir, readFile } from "fs/promises";
import { join } from "path";

const CONFIG_DIR = "/Users/enderj/EkoContentStudio/config";

export async function GET() {
  try {
    const files = await readdir(CONFIG_DIR);
    const briefFiles = files
      .filter((f) => f.startsWith("brief_") && f.endsWith(".json"))
      .sort()
      .reverse();

    const briefs = await Promise.all(
      briefFiles.map(async (f) => {
        const raw = await readFile(join(CONFIG_DIR, f), "utf-8");
        const data = JSON.parse(raw);
        return {
          filename: f,
          business_name: data.business_name,
          industry: data.industry,
          city: data.city,
          products: data.products,
        };
      })
    );

    return NextResponse.json({ briefs });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to load briefs" },
      { status: 500 }
    );
  }
}
