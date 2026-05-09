import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.INTERNAL_API_URL || "http://eko-backend.:8000";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const response = await fetch(`${API_URL}/api/v1/leads/public`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Proxy error:", error);
    return NextResponse.json(
      { status: "error", message: "Failed to process request" },
      { status: 500 }
    );
  }
}
