"""Find real business websites using search engines."""
import logging
import re
from typing import Optional

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

_BLOCKED_DOMAINS = [
    "yelp.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "linkedin.com",
    "youtube.com",
    "tiktok.com",
    "bbb.org",
    "mapquest.com",
    "yellowpages.com",
    "manta.com",
    "foursquare.com",
    "tripadvisor.com",
    "grubhub.com",
    "doordash.com",
    "ubereats.com",
    "opentable.com",
    "zomato.com",
    "healthgrades.com",
    "ratemds.com",
    "vitals.com",
    "wellness.com",
    "angi.com",
    "thumbtack.com",
    "porch.com",
    "homeadvisor.com",
    # Government and irrelevant domains
    ".gov",
    ".mil",
    ".edu",
    "irs.gov",
    "sos.state",
    "county.",
    "state.",
]

# URL patterns that should be blocked anywhere in the URL
_BLOCKED_URL_PATTERNS = [
    ".pdf",
    ".gov/",
    ".mil/",
]

# Business status keywords from Secretary of State data
_STATUS_KEYWORDS = [
    "dissolved",
    "delinquent",
    "good standing",
    "revoked",
    "withdrawn",
    "suspended",
    "merged",
    "converted",
    "inactive",
    "terminated",
    "forfeited",
    "expired",
    "cancelled",
    "canceled",
]


class WebsiteFinder:
    """Find the real website of a business when we only have Yelp/social URLs."""

    def __init__(self):
        settings = get_settings()
        self.serpapi_key = settings.SERPAPI_API_KEY
        self.client = httpx.AsyncClient(timeout=15.0, follow_redirects=True)

    def _clean_business_name(self, business_name: str) -> str:
        """
        Remove status suffixes from business names (e.g. Colorado SOS data).
        Strips anything after the first comma if the remainder contains status words.
        """
        if "," not in business_name:
            return business_name.strip()

        parts = business_name.split(",", 1)
        name_part = parts[0].strip()
        suffix_part = parts[1].lower()

        # If suffix contains any status keyword, drop it entirely
        if any(keyword in suffix_part for keyword in _STATUS_KEYWORDS):
            return name_part

        # Otherwise return the original (trimmed)
        return business_name.strip()

    async def find_website(self, business_name: str, city: str, state: str) -> Optional[str]:
        """
        Search for the real business website.
        Returns the best matching URL or None.
        """
        cleaned_name = self._clean_business_name(business_name)
        query = f'"{cleaned_name}" {city} {state}'

        # Try SerpApi if available
        if self.serpapi_key:
            try:
                url = await self._search_serpapi(query, business_name)
                if url:
                    logger.info(f"WebsiteFinder: found {url} for {business_name}")
                    return url
            except Exception as e:
                logger.warning(f"SerpApi search failed: {e}")

        # Fallback: try DuckDuckGo lite scrape
        try:
            url = await self._search_duckduckgo(query, business_name)
            if url:
                logger.info(f"WebsiteFinder: found {url} for {business_name} via DDG")
                return url
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")

        return None

    async def _search_serpapi(self, query: str, business_name: str) -> Optional[str]:
        """Use SerpApi Google search."""
        params = {
            "q": query,
            "api_key": self.serpapi_key,
            "engine": "google",
            "num": 10,
            "location": "United States",
        }
        resp = await self.client.get("https://serpapi.com/search", params=params)
        resp.raise_for_status()
        data = resp.json()

        organic = data.get("organic_results", [])
        return self._pick_best_url(organic, business_name)

    async def _search_duckduckgo(self, query: str, business_name: str) -> Optional[str]:
        """Scrape DuckDuckGo HTML results as fallback."""
        resp = await self.client.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        for a in soup.find_all("a", class_="result__a"):
            href = a.get("href", "")
            title = a.get_text(strip=True)
            results.append({"link": href, "title": title})

        return self._pick_best_url(results, business_name)

    def _is_blocked_url(self, url: str) -> bool:
        """Check if a URL matches blocked domain or pattern lists."""
        url_lower = url.lower()
        domain = url.split("/")[2].lower().replace("www.", "")

        if any(blocked in domain for blocked in _BLOCKED_DOMAINS):
            return True

        if any(pattern in url_lower for pattern in _BLOCKED_URL_PATTERNS):
            return True

        return False

    def _pick_best_url(self, results: list, business_name: str) -> Optional[str]:
        """Pick the best URL from search results, filtering out directories."""
        business_lower = business_name.lower()
        words = [w for w in re.findall(r"\w+", business_lower) if len(w) > 2]

        for result in results:
            url = result.get("link") or result.get("url", "")
            if not url.startswith("http"):
                continue

            if self._is_blocked_url(url):
                continue

            # Prefer URLs that match business name words
            domain = url.split("/")[2].lower().replace("www.", "")
            domain_words = re.findall(r"\w+", domain)
            match_score = sum(1 for w in words if w in domain_words)

            # Also check title for match
            title = result.get("title", "").lower()
            title_match = sum(1 for w in words if w in title)

            if match_score > 0 or title_match >= max(1, len(words) // 2):
                return url

        # If no good match, return first non-blocked result
        for result in results:
            url = result.get("link") or result.get("url", "")
            if not url.startswith("http"):
                continue
            if not self._is_blocked_url(url):
                return url

        return None
