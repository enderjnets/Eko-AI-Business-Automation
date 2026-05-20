import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Forces no-cache headers on dashboard HTML responses. Next.js's default for
// static-shell pages is `s-maxage=31536000, stale-while-revalidate` which
// caused users to load stale HTML referencing OLD JS chunk hashes for up to
// a year after frontend deploys. Static asset chunks (under /_next/static/)
// stay immutable since their filenames include content hashes.
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  response.headers.set("Cache-Control", "no-store, must-revalidate");
  response.headers.set("Pragma", "no-cache");
  return response;
}

export const config = {
  matcher: [
    // Match all paths EXCEPT static assets and API routes.
    "/((?!_next/static|_next/image|favicon.ico|api/).*)",
  ],
};
