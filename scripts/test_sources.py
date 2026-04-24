#!/usr/bin/env python3
"""Standalone test of all 4 discovery sources."""

import asyncio
import json
import sys
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

# Load env vars
env_path = Path(__file__).parent.parent / ".env"
env_vars = {}
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env_vars[k] = v

OUTSCRAPER_KEY = env_vars.get("OUTSCRAPER_API_KEY", "").strip()
YELP_KEY = env_vars.get("YELP_API_KEY", "").strip()
APIFY_KEY = env_vars.get("APIFY_API_KEY", "").strip()
SERPAPI_KEY = env_vars.get("SERPAPI_API_KEY", "").strip()

QUERY = "restaurant"
CITY = "Denver"
STATE = "CO"
MAX_RESULTS = 5


async def test_colorado_sos():
    """Colorado SOS — Official Open Data API (no key required)."""
    print("\n🏛️  COLORADO SOS")
    print("-" * 50)
    try:
        url = "https://data.colorado.gov/resource/4ykn-tg5h.json"
        params = {
            "$where": f"lower(entityname) like '%{QUERY}%' and principalcity = '{CITY.upper()}'",
            "$limit": MAX_RESULTS,
            "$order": "entityformdate DESC",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        print(f"✅ Status: {resp.status_code} | Results: {len(data)}")
        for item in data[:3]:
            print(f"   • {item.get('entityname')} | {item.get('principalcity')}, {item.get('principalstate')} | {item.get('entitystatus')} | {item.get('entitytype')}")
        return len(data) > 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_linkedin():
    """LinkedIn — SerpApi primary + DuckDuckGo fallback."""
    print("\n🔗 LINKEDIN (SerpApi + DuckDuckGo fallback)")
    print("-" * 50)

    # Try SerpApi first
    if SERPAPI_KEY and SERPAPI_KEY != "...":
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(
                    "https://serpapi.com/search",
                    params={
                        "engine": "google",
                        "q": f'site:linkedin.com/company "{QUERY}" "{CITY}"',
                        "num": MAX_RESULTS,
                        "api_key": SERPAPI_KEY,
                        "output": "json",
                    },
                )
                resp.raise_for_status()
                data = resp.json()

                if "error" in data:
                    print(f"⚠️  SerpApi error: {data['error']}")
                else:
                    organic = data.get("organic_results", [])
                    linkedin_urls = [
                        r.get("link") for r in organic
                        if "linkedin.com/company/" in r.get("link", "")
                    ]
                    print(f"✅ SerpApi returned {len(linkedin_urls)} LinkedIn URLs")
                    for url in linkedin_urls[:3]:
                        print(f"   • {url}")
                    if linkedin_urls:
                        return True
        except Exception as e:
            print(f"⚠️  SerpApi failed: {e}")
    else:
        print("⚠️  SERPAPI_API_KEY not configured. Get one free at https://serpapi.com/dashboard")

    # Fallback: DuckDuckGo
    try:
        search_query = f"site:linkedin.com/company {QUERY} {CITY}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://html.duckduckgo.com/html/",
                data={"q": search_query, "kl": "us-en"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.select(".result")

        linkedin_urls = []
        for result in results[:MAX_RESULTS]:
            link = result.select_one(".result__a")
            if link:
                href = link.get("href", "")
                if "linkedin.com/company/" in href:
                    linkedin_urls.append(href)

        print(f"✅ DuckDuckGo fallback: {len(linkedin_urls)} LinkedIn URLs found")
        for url in linkedin_urls[:3]:
            print(f"   • {url}")
        return len(linkedin_urls) > 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_google_maps():
    """Google Maps — Outscraper (requires API key)."""
    print("\n📍 GOOGLE MAPS (Outscraper)")
    print("-" * 50)
    if not OUTSCRAPER_KEY or OUTSCRAPER_KEY == "...":
        print("⚠️  OUTSCRAPER_API_KEY not configured in .env")
        print("   Get one at: https://outscraper.com")
        return False

    try:
        async with httpx.AsyncClient(
            base_url="https://api.app.outscraper.com",
            headers={"X-API-KEY": OUTSCRAPER_KEY},
            timeout=60,
        ) as client:
            resp = await client.get(
                "/maps/search-v3",
                params={
                    "query": f"{QUERY} in {CITY}, {STATE}",
                    "limit": MAX_RESULTS,
                    "async": "false",
                },
            )
            print(f"{'✅' if resp.status_code == 200 else '❌'} Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                businesses = data.get("data", []) if isinstance(data, dict) else data
                print(f"   Results: {len(businesses)}")
                for b in businesses[:2]:
                    print(f"   • {b.get('name')} | {b.get('address')}")
                return len(businesses) > 0
            else:
                print(f"   Response: {resp.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_yelp():
    """Yelp — Fusion API (requires API key)."""
    print("\n⭐ YELP (Fusion API)")
    print("-" * 50)
    if not YELP_KEY or YELP_KEY == "...":
        print("⚠️  YELP_API_KEY not configured in .env")
        print("   Get one free at: https://www.yelp.com/developers/v3/manage_app")
        return False

    try:
        async with httpx.AsyncClient(
            base_url="https://api.yelp.com/v3",
            headers={"Authorization": f"Bearer {YELP_KEY}"},
            timeout=30,
        ) as client:
            resp = await client.get(
                "/businesses/search",
                params={
                    "term": QUERY,
                    "location": f"{CITY}, {STATE}",
                    "limit": MAX_RESULTS,
                },
            )
            print(f"{'✅' if resp.status_code == 200 else '❌'} Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                businesses = data.get("businesses", [])
                print(f"   Results: {len(businesses)}")
                for b in businesses[:2]:
                    print(f"   • {b.get('name')} | {b.get('rating')}⭐ | {b.get('review_count')} reviews | {b.get('location', {}).get('city')}")
                return len(businesses) > 0
            else:
                print(f"   Response: {resp.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    print("=" * 60)
    print("DISCOVERY SOURCES LIVE TEST")
    print(f"Query: '{QUERY}' in {CITY}, {STATE}")
    print("=" * 60)

    results = {
        "colorado_sos": await test_colorado_sos(),
        "linkedin": await test_linkedin(),
        "google_maps": await test_google_maps(),
        "yelp": await test_yelp(),
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for source, ok in results.items():
        icon = "✅" if ok else "❌"
        print(f"{icon} {source:20s} {'WORKING' if ok else 'FAILED / MISSING KEY'}")

    return all(results.values())


if __name__ == "__main__":
    ok = asyncio.run(main())
    sys.exit(0 if ok else 1)
