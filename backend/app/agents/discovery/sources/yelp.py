"""Discovery source using Yelp search scraping."""

from typing import List, Dict, Optional
import logging
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class YelpSource:
    """Discovery source using Yelp search page scraping."""

    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            },
            timeout=15.0,
            follow_redirects=True,
        )

    async def search(
        self,
        query: str,
        city: str,
        state: Optional[str] = "CO",
        radius_miles: int = 25,
        max_results: int = 50,
    ) -> List[Dict]:
        """Search for businesses on Yelp."""
        search_query = f"{query} in {city}, {state}"
        logger.info(f"Yelp discovery: {search_query}")

        try:
            results = await self._scrape_search(query, city, state, max_results)
        except Exception as e:
            logger.warning(f"Yelp scraping failed: {e}")
            return []

        leads = []
        for biz in results:
            lead = self._normalize_business(biz)
            if lead:
                leads.append(lead)

        logger.info(f"Found {len(leads)} leads from Yelp")
        return leads

    async def _scrape_search(
        self, query: str, city: str, state: str, max_results: int
    ) -> List[Dict]:
        """Scrape Yelp search results page."""
        url = "https://www.yelp.com/search"
        params = {
            "find_desc": query,
            "find_loc": f"{city}, {state}",
            "start": 0,
        }

        resp = await self.client.get(url, params=params)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        businesses = []

        # Yelp uses various markup patterns; try several selectors
        containers = soup.select("[data-testid='serp-ia-card']")
        if not containers:
            containers = soup.select(".y__1dc2i5d")
        if not containers:
            containers = soup.select("[class*='container']:has(h3)")

        for card in containers[:max_results]:
            biz = self._parse_card(card)
            if biz:
                businesses.append(biz)

        return businesses

    def _parse_card(self, card: BeautifulSoup) -> Optional[Dict]:
        """Extract business data from a Yelp search card."""
        # Try multiple selectors for business name
        name_tag = (
            card.select_one("a.css-19v1rkv")
            or card.select_one("a.css-1422juy")
            or card.select_one("h3 a")
            or card.select_one("a[href*='/biz/']")
        )
        if not name_tag:
            return None

        name = name_tag.get_text(strip=True)
        href = name_tag.get("href", "")
        if href.startswith("/"):
            href = f"https://www.yelp.com{href}"

        # Rating and review count
        rating_tag = card.select_one("[aria-label*='star rating']")
        rating = None
        review_count = None
        if rating_tag:
            aria = rating_tag.get("aria-label", "")
            # e.g. "4.5 star rating"
            try:
                rating = float(aria.split()[0])
            except (ValueError, IndexError):
                pass

        review_tag = card.select_one("span.css-chan6m")
        if review_tag:
            text = review_tag.get_text(strip=True)
            if "review" in text.lower():
                try:
                    review_count = int(text.split()[0])
                except (ValueError, IndexError):
                    pass

        # Category
        category_tag = card.select_one("p.css-1p8aobs") or card.select_one("p.css-16lqlh0")
        category = category_tag.get_text(strip=True) if category_tag else ""

        # Address / neighborhood
        address_tag = (
            card.select_one("p.css-1p8aobs + p")
            or card.select_one("span.css-chan6m + span")
        )
        address = address_tag.get_text(strip=True) if address_tag else ""

        # Phone
        phone_tag = card.select_one("p.css-1h1j0y3")
        phone = phone_tag.get_text(strip=True) if phone_tag else ""

        return {
            "name": name,
            "yelp_url": href,
            "rating": rating,
            "review_count": review_count,
            "category": category,
            "address": address,
            "phone": phone,
        }

    def _normalize_business(self, biz: Dict) -> Optional[Dict]:
        """Normalize Yelp business data to Lead format."""
        name = biz.get("name", "").strip()
        if not name:
            return None

        # Build description from rating/reviews
        parts = []
        if biz.get("rating"):
            parts.append(f"{biz['rating']} stars on Yelp")
        if biz.get("review_count"):
            parts.append(f"{biz['review_count']} reviews")
        description = " | ".join(parts) if parts else ""

        return {
            "business_name": name,
            "category": biz.get("category") or None,
            "description": description or None,
            "email": None,
            "phone": biz.get("phone") or None,
            "website": biz.get("yelp_url") or None,
            "address": biz.get("address") or None,
            "city": None,
            "state": None,
            "zip_code": None,
            "country": "US",
            "latitude": None,
            "longitude": None,
            "source": "yelp",
            "source_data": biz,
        }
