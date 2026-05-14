import { NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";

const OUTPUT_DIR = "/Users/enderj/EkoContentStudio/output";

export async function GET() {
  try {
    const raw = await readFile(
      join(OUTPUT_DIR, "scripts_latest.json"),
      "utf-8"
    );
    const data = JSON.parse(raw);
    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to load scripts" },
      { status: 500 }
    );
  }
}
