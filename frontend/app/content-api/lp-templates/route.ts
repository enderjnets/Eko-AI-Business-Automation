/**
 * Proxies the landing page templates list from the backend so the Create modal
 * can show all available designs without a direct backend call from the browser.
 */
import { NextResponse } from "next/server";

const BACKEND = process.env.BACKEND_URL || "http://eko-backend:8000";

export async function GET() {
  try {
    const res = await fetch(`${BACKEND}/api/v1/landing-pages/templates`, {
      cache: "no-store",
    });
    if (!res.ok) {
      return NextResponse.json(
        { templates: [], error: `backend ${res.status}` },
        { status: res.status }
      );
    }
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json(
      { templates: [], error: err?.message || "fetch failed" },
      { status: 502 }
    );
  }
}
