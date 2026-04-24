"""Discovery source using Colorado Secretary of State Open Data API."""

from typing import List, Dict, Optional
import logging

import httpx

from app.services.apify import ApifyClient

logger = logging.getLogger(__name__)

COLORADO_SODA_API = "https://data.colorado.gov/resource/4ykn-tg5h.json"
DEFAULT_COLORADO_ACTOR = "clawdeus/co-biz-lookup"


class ColoradoSOSSource:
    """Discovery source using Colorado Secretary of State business registry."""

    def __init__(self, actor_id: Optional[str] = None):
        self.apify = ApifyClient()
        self.actor_id = actor_id or DEFAULT_COLORADO_ACTOR
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
        )

    async def search(
        self,
        query: str,
        city: Optional[str] = None,
        state: Optional[str] = "CO",
        radius_miles: int = 25,
        max_results: int = 50,
    ) -> List[Dict]:
        """Search for registered business entities in Colorado."""
        logger.info(f"Colorado SOS discovery: {query} in {city}")

        # Primary: direct Socrata Open Data API (fast, free, no auth)
        try:
            return await self._search_api(query, city, max_results)
        except Exception as e:
            logger.warning(f"Colorado SOS direct API failed: {e}")

        # Fallback: Apify actor
        try:
            if self.apify.api_key:
                return await self._search_apify(query, city, max_results)
        except Exception as e:
            logger.warning(f"Apify Colorado SOS failed: {e}")

        return []

    async def _search_api(
        self, query: str, city: Optional[str], max_results: int
    ) -> List[Dict]:
        """Search via Colorado Open Data API (Socrata)."""
        # Build SoQL query
        where_parts = [f"lower(entityname) like '%{query.lower()}%'"]
        if city:
            where_parts.append(f"principalcity = '{city.upper()}'")

        params = {
            "$where": " and ".join(where_parts),
            "$limit": min(max_results, 100),
            "$order": "entityformdate DESC",
        }

        resp = await self.client.get(COLORADO_SODA_API, params=params)
        resp.raise_for_status()
        results = resp.json()

        leads = []
        for entity in results:
            lead = self._normalize_entity(entity)
            if lead:
                leads.append(lead)

        logger.info(f"Colorado SOS (API) returned {len(leads)} leads")
        return leads

    async def _search_apify(self, query: str, city: Optional[str], max_results: int) -> List[Dict]:
        """Search via Apify actor (fallback)."""
        results = await self.apify.run_actor(
            actor_id=self.actor_id,
            run_input={
                "searchTerms": [query],
                "maxResults": min(max_results, 100),
            },
            wait_for_finish=True,
            max_wait_seconds=60,
        )

        leads = []
        for entity in results:
            lead = self._normalize_entity(entity)
            if lead:
                leads.append(lead)

        logger.info(f"Colorado SOS (Apify) returned {len(leads)} leads")
        return leads

    def _normalize_entity(self, entity: Dict) -> Optional[Dict]:
        """Normalize Colorado SOS entity data to Lead format."""
        name = (
            entity.get("entityname")
            or entity.get("entity_name")
            or entity.get("businessName")
            or entity.get("name")
        )
        if not name:
            return None

        status = entity.get("entitystatus") or entity.get("entityStatus") or "Unknown"
        entity_type = entity.get("entitytype") or entity.get("entityType") or "Business"
        doc_number = entity.get("entityid") or entity.get("entityId") or entity.get("document_number")
        formation_date = entity.get("entityformdate") or entity.get("entityFormDate")

        # Address (Open Data API uses principaladdress1, Apify may use principal_address)
        address = entity.get("principaladdress1") or entity.get("principal_address") or entity.get("address")
        city = entity.get("principalcity") or entity.get("principal_city") or entity.get("city")
        state = entity.get("principalstate") or entity.get("principal_state") or entity.get("state") or "CO"
        zip_code = entity.get("principalzipcode") or entity.get("principal_zipcode") or entity.get("zip_code")
        country = entity.get("principalcountry") or entity.get("principal_country") or entity.get("country") or "US"

        # Agent
        agent_first = entity.get("agentfirstname") or ""
        agent_last = entity.get("agentlastname") or ""
        agent_name = f"{agent_first} {agent_last}".strip() or entity.get("registered_agent")

        return {
            "business_name": name.strip(),
            "category": entity_type.strip() if entity_type else None,
            "description": f"Colorado registered {entity_type}. Status: {status}." if entity_type else f"Status: {status}",
            "email": None,
            "phone": None,
            "website": None,
            "address": address.strip() if address else None,
            "city": city.strip() if city else None,
            "state": state.strip() if state else "CO",
            "zip_code": zip_code.strip() if zip_code else None,
            "country": country.strip() if country else "US",
            "latitude": None,
            "longitude": None,
            "source": "colorado_sos",
            "source_data": {
                **entity,
                "document_number": doc_number,
                "formation_date": formation_date,
                "registered_agent": agent_name,
                "status": status,
            },
        }
