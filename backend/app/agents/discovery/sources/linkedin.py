"""Discovery source using LinkedIn via Apify + SerpApi + DuckDuckGo fallback."""

from typing import List, Dict, Optional
import logging
import urllib.parse

import httpx
from bs4 import BeautifulSoup

from app.services.apify import ApifyClient
from app.services.serpapi import SerpApiClient

logger = logging.getLogger(__name__)

DEFAULT_LINKEDIN_ACTOR = "harvestapi/linkedin-company"
DUCKDUCKGO_HTML_URL = "https://html.duckduckgo.com/html/"
LINKEDIN_PUBLIC_URL = "https://www.linkedin.com/company/"


class LinkedInSource:
    """Discovery source for LinkedIn companies.

    Hierarchy:
    1. SerpApi (Google search) — most reliable, requires key
    2. Apify actor — requires HarvestAPI token
    3. DuckDuckGo + public page scraping — free but fragile
    """

    def __init__(self, actor_id: Optional[str] = None):
        self.apify = ApifyClient()
        self.serpapi = SerpApiClient()
        self.actor_id = actor_id or DEFAULT_LINKEDIN_ACTOR
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
            },
        )

    async def search(
        self,
        query: str,
        city: str,
        state: Optional[str] = "CO",
        radius_miles: int = 25,
        max_results: int = 50,
    ) -> List[Dict]:
        """Search for companies on LinkedIn."""
        logger.info(f"LinkedIn discovery: {query} in {city}")

        # 1. Try SerpApi first (most reliable)
        try:
            if self.serpapi.api_key:
                results = await self._search_serpapi(query, city, max_results)
                if results:
                    return results
        except Exception as e:
            logger.warning(f"LinkedIn SerpApi failed: {e}")

        # 2. Try Apify actor
        try:
            if self.apify.api_key:
                results = await self._search_apify(query, city, max_results)
                if results:
                    return results
        except Exception as e:
            logger.warning(f"LinkedIn Apify failed: {e}")

        # 3. Fallback: DuckDuckGo search
        try:
            return await self._search_duckduckgo(query, city, max_results)
        except Exception as e:
            logger.warning(f"LinkedIn DuckDuckGo fallback failed: {e}")

        return []

    async def _search_serpapi(self, query: str, city: str, max_results: int) -> List[Dict]:
        """Search via SerpApi Google search for LinkedIn company pages."""
        search_query = f'site:linkedin.com/company "{query}" "{city}"'
        organic = await self.serpapi.search_google(
            query=search_query,
            num_results=min(max_results, 20),
        )

        leads = []
        for result in organic:
            link = result.get("link", "")
            if "linkedin.com/company/" not in link:
                continue

            company_slug = link.split("linkedin.com/company/")[-1].split("/")[0].split("?")[0]
            if not company_slug:
                continue

            # Use title and snippet from search result
            title = result.get("title", "").replace(" | LinkedIn", "").strip()
            snippet = result.get("snippet", "")

            # Try to enrich with public page scrape
            company_data = await self._scrape_linkedin_public(company_slug)
            if company_data:
                if not company_data.get("companyName"):
                    company_data["companyName"] = title
                if not company_data.get("about"):
                    company_data["about"] = snippet
                lead = self._normalize_company(company_data)
            else:
                # Minimal lead from search result only
                lead = self._normalize_company({
                    "companyName": title,
                    "about": snippet,
                    "linkedinUrl": link,
                })

            if lead:
                leads.append(lead)

        logger.info(f"LinkedIn (SerpApi) returned {len(leads)} leads")
        return leads

    async def _search_apify(self, query: str, city: str, max_results: int) -> List[Dict]:
        """Search via Apify actor."""
        results = await self.apify.run_actor(
            actor_id=self.actor_id,
            run_input={
                "companyNames": [query],
                "maxResults": min(max_results, 100),
            },
            wait_for_finish=True,
            max_wait_seconds=60,
        )

        leads = []
        for company in results:
            lead = self._normalize_company(company)
            if lead:
                leads.append(lead)

        logger.info(f"LinkedIn (Apify) returned {len(leads)} leads")
        return leads

    async def _search_duckduckgo(self, query: str, city: str, max_results: int) -> List[Dict]:
        """Search LinkedIn company pages via DuckDuckGo + scrape public pages."""
        search_query = f"site:linkedin.com/company {query} {city}"
        logger.info(f"LinkedIn DuckDuckGo search: {search_query}")

        resp = await self.client.post(
            DUCKDUCKGO_HTML_URL,
            data={"q": search_query, "kl": "us-en"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.select(".result")

        leads = []
        for result in results[:max_results]:
            link_tag = result.select_one(".result__a")
            if not link_tag:
                continue

            href = link_tag.get("href", "")
            if "linkedin.com/company/" not in href:
                continue

            company_slug = href.split("linkedin.com/company/")[-1].split("/")[0].split("?")[0]
            if not company_slug:
                continue

            company_data = await self._scrape_linkedin_public(company_slug)
            if company_data:
                lead = self._normalize_company(company_data)
                if lead:
                    leads.append(lead)

        logger.info(f"LinkedIn (DuckDuckGo) returned {len(leads)} leads")
        return leads

    async def _scrape_linkedin_public(self, company_slug: str) -> Optional[Dict]:
        """Scrape public LinkedIn company page for basic metadata."""
        url = f"{LINKEDIN_PUBLIC_URL}{company_slug}/about/"
        try:
            resp = await self.client.get(url, follow_redirects=True)
            if resp.status_code != 200:
                return None

            soup = BeautifulSoup(resp.text, "html.parser")

            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else company_slug
            title = title.replace(" | LinkedIn", "").strip()

            desc_tag = soup.find("meta", attrs={"name": "description"})
            description = desc_tag.get("content") if desc_tag else None

            # Look for JSON-LD
            scripts = soup.find_all("script", type="application/ld+json")
            for script in scripts:
                try:
                    import json
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get("@type") == "Organization":
                        return {
                            "companyName": data.get("name", title),
                            "about": data.get("description", description),
                            "website": data.get("url"),
                            "industry": data.get("industry"),
                            "linkedinUrl": f"https://www.linkedin.com/company/{company_slug}/",
                            "employeeCount": data.get("numberOfEmployees"),
                            "city": None,
                            "state": None,
                        }
                except Exception:
                    continue

            return {
                "companyName": title,
                "about": description,
                "linkedinUrl": f"https://www.linkedin.com/company/{company_slug}/",
                "industry": None,
                "website": None,
                "employeeCount": None,
                "city": None,
                "state": None,
            }
        except Exception as e:
            logger.debug(f"LinkedIn public scrape failed for {company_slug}: {e}")
            return None

    def _normalize_company(self, company: Dict) -> Optional[Dict]:
        """Normalize LinkedIn company data to Lead format."""
        name = (
            company.get("companyName")
            or company.get("name")
            or company.get("title")
        )
        if not name:
            return None

        location = company.get("locations", [])
        if isinstance(location, list) and location:
            loc = location[0]
            city = loc.get("city", "")
            state = loc.get("state", "")
            country = loc.get("country", "US")
        else:
            city = company.get("city", "")
            state = company.get("state", "")
            country = company.get("country", "US")

        website = company.get("companyUrl") or company.get("website")
        linkedin_url = company.get("linkedinUrl") or company.get("url")
        industry = company.get("industry") or company.get("category")

        about = company.get("about") or company.get("headline") or company.get("specialties", "")
        if isinstance(about, list):
            about = ", ".join(about)

        employee_count = company.get("employeeCount") or company.get("employeesCount")

        return {
            "business_name": name.strip(),
            "category": industry.strip() if industry else None,
            "description": about.strip() if about else None,
            "email": None,
            "phone": None,
            "website": website.strip() if website else (linkedin_url.strip() if linkedin_url else None),
            "address": None,
            "city": city.strip() if city else None,
            "state": state.strip() if state else None,
            "zip_code": None,
            "country": country.strip() if country else "US",
            "latitude": None,
            "longitude": None,
            "source": "linkedin",
            "source_data": {
                **company,
                "linkedin_url": linkedin_url,
                "employee_count": employee_count,
            },
        }
