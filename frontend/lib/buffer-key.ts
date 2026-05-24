/**
 * Centralized accessor for the Buffer API key.
 *
 * History: the key used to be hardcoded as a string literal in 6+ files
 * throughout frontend/. That made rotating it painful and risked accidental
 * exposure on every diff. This helper reads from BUFFER_API_KEY in the
 * environment, with a single fallback constant kept here for backwards
 * compatibility during the migration window. Once the env var is set
 * everywhere the bot runs, the fallback can be deleted.
 */

const FALLBACK_KEY = "au7VyBXcqYkOpftcaLuE7awhoSHBoXEAM-WPJWh06Fv";

export function getBufferKey(): string {
  return process.env.BUFFER_API_KEY || FALLBACK_KEY;
}

/**
 * Hosts owned by Buffer (image CDN, GraphQL, S3 media buckets). Used by the
 * proxy routes to decide whether attaching the Bearer token is appropriate
 * and whether the upstream URL is allowed at all.
 */
export function isBufferHost(hostname: string): boolean {
  if (!hostname) return false;
  const h = hostname.toLowerCase();
  return (
    h === "buffer.com" ||
    h.endsWith(".buffer.com") ||
    h === "bufferapp.com" ||
    h.endsWith(".bufferapp.com") ||
    h.startsWith("buffer-") && h.endsWith(".s3.amazonaws.com")
  );
}

/**
 * Hosts owned by us (currently the ROG behind the Tailscale-fronted public
 * tunnel). Used by the proxy to allow self-hosted pipeline media.
 */
export function isSelfHost(hostname: string): boolean {
  if (!hostname) return false;
  const h = hostname.toLowerCase();
  return (
    h === "ender-rog.tail25dc73.ts.net" ||
    h.endsWith(".ekoaiautomation.com") ||
    h === "ekoaiautomation.com"
  );
}

export function isAllowedProxyHost(hostname: string): boolean {
  return isBufferHost(hostname) || isSelfHost(hostname);
}
