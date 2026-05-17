// Simple in-memory cache for API routes with TTL
interface CacheEntry<T> {
  data: T;
  expiresAt: number;
}

const cache = new Map<string, CacheEntry<any>>();

export function getCached<T>(key: string): T | null {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expiresAt) {
    cache.delete(key);
    return null;
  }
  return entry.data;
}

export function setCache<T>(key: string, data: T, ttlMs: number = 30000): void {
  cache.set(key, { data, expiresAt: Date.now() + ttlMs });
}

export function clearCache(keyPrefix?: string): void {
  if (!keyPrefix) {
    cache.clear();
    return;
  }
  Array.from(cache.keys()).forEach((key) => {
    if (key.startsWith(keyPrefix)) cache.delete(key);
  });
}
