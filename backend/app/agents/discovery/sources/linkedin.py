"""Discovery source using Apify LinkedIn company scraper."""

from typing import List, Dict, Optional
import logging

from app.services.apify import ApifyClient

logger = logging.getLogger(__name__)

# Default Apify actor for LinkedIn company search
DEFAULT_LINKEDIN_ACTOR = "apify/linkedin-company-scraper"


class LinkedInSource:
    """Discovery source using LinkedIn via Apify actor."""

    def __init__(self, actor_id: Optional[str] = None):
        self.client = ApifyClient()
        self.actor_id = actor_id or DEFAULT_LINKEDIN_ACTOR

    async def search(
        self,
        query: str,
        city: str,
        state: Optional[str] = "CO",
        radius_miles: int = 25,
        max_results: int = 50,
    ) -> List[Dict]:
        """Search for companies on LinkedIn."""
        search_terms = f"{query} {city}"
        logger.info(f"LinkedIn discovery: {search_terms}")

        try:
            results = await self.client.run_actor(
                actor_id=self.actor_id,
                run_input={
                    "searchTerms": [search_terms],
                    "location": f"{city}, {state}, United States",
                    "maxResults": min(max_results, 100),
                },
                wait_for_finish=True,
                max_wait_seconds=60,
            )
        except Exception as e:
            logger.warning(f"LinkedIn/Apify discovery failed: {e}")
            return []

        leads = []
        for company in results:
            lead = self._normalize_company(company)
            if lead:
                leads.append(lead)

        logger.info(f"Found {len(leads)} leads from LinkedIn")
        return leads

    def _normalize_company(self, company: Dict) -> Optional[Dict]:
        """Normalize LinkedIn company data to Lead format."""
        name = (
            company.get("companyName")
            or company.get("name")
            or company.get("title")
        )
        if not name:
            return None

        # Extract location
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

        # Website
        website = company.get("companyUrl") or company.get("website")
        linkedin_url = company.get("linkedinUrl") or company.get("url")

        # Industry / category
        industry = company.get("industry") or company.get("category")

        # Description
        about = company.get("about") or company.get("headline") or company.get("specialties", "")
        if isinstance(about, list):
            about = ", ".join(about)

        # Employee count
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
