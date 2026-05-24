import type { NextRequest } from "next/server";

/**
 * Allowlist of origins permitted to perform mutating requests against the
 * Content Studio API routes. Add new hostnames here when the dashboard is
 * served from a new tunnel or subdomain — keeping this explicit prevents
 * silent CSRF exposure.
 *
 * The check covers both Origin and Referer headers; if neither is set we
 * reject because mutating requests should always come from a real browser
 * navigation context.
 */
const ALLOWED_ORIGINS: readonly string[] = [
  "http://localhost:3000",
  "http://localhost:3001",
  "http://100.88.47.99:3001",
  "https://ender-rog.tail25dc73.ts.net",
  "https://app.ekoaiautomation.com",
];

export function isAllowedOrigin(req: NextRequest): boolean {
  const origin = req.headers.get("origin");
  const referer = req.headers.get("referer");
  const candidate = (origin || referer || "").trim();
  if (!candidate) return false;
  return ALLOWED_ORIGINS.some((allowed) => candidate.startsWith(allowed));
}
