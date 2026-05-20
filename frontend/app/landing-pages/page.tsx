// Server component shell. Forces Next.js to render this route dynamically
// on every request, so newly-deployed JS chunk hashes are always reflected
// in the HTML. Without this, Next.js statically pre-renders and caches the
// page with s-maxage=31536000, leaving users on stale chunks for up to a
// year after deploys.
//
// Actual UI lives in LandingPagesClient.tsx ("use client").
export const dynamic = "force-dynamic";
export const revalidate = 0;
export const fetchCache = "force-no-store";

import LandingPagesClient from "./LandingPagesClient";

export default function Page() {
  return <LandingPagesClient />;
}
