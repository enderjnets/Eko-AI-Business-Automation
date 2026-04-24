from typing import List, Dict, Optional
import logging

from app.agents.discovery.sources.google_maps import GoogleMapsSource
from app.agents.discovery.sources.yelp import YelpSource
from app.agents.discovery.sources.linkedin import LinkedInSource
from app.agents.discovery.sources.colorado_sos import ColoradoSOSSource
from app.services.paperclip import on_discovery_complete

logger = logging.getLogger(__name__)


class DiscoveryAgent:
    """
    Discovery Agent: Finds potential leads from multiple sources.
    
    Currently supports:
    - Google Maps (via Outscraper)
    - Yelp (web scraping)
    - LinkedIn (via Apify)
    - Colorado Secretary of State (Apify + scraping)
    
    Future sources:
    - Job boards
    """
    
    
    def __init__(self):
        self.google_maps = GoogleMapsSource()
        self.yelp = YelpSource()
        self.linkedin = LinkedInSource()
        self.colorado_sos = ColoradoSOSSource()
    
    async def discover(
        self,
        query: str,
        city: str,
        state: Optional[str] = "CO",
        radius_miles: int = 25,
        max_results: int = 50,
        sources: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        Run discovery across configured sources.
        
        Args:
            query: Business category or search term
            city: Target city
            state: State code (default: CO)
            radius_miles: Search radius
            max_results: Max results per source
            sources: List of source names to use (default: all)
        
        Returns:
            List of normalized lead dictionaries
        """
        sources = sources or ["google_maps"]
        all_leads = []
        
        logger.info(f"DiscoveryAgent: searching '{query}' in {city}, {state}")
        
        if "google_maps" in sources:
            try:
                gmaps_leads = await self.google_maps.search(
                    query=query,
                    city=city,
                    state=state,
                    radius_miles=radius_miles,
                    max_results=max_results,
                )
                all_leads.extend(gmaps_leads)
                logger.info(f"Google Maps returned {len(gmaps_leads)} leads")
            except Exception as e:
                logger.error(f"Google Maps discovery failed: {e}")
        
        if "yelp" in sources:
            try:
                yelp_leads = await self.yelp.search(
                    query=query,
                    city=city,
                    state=state,
                    radius_miles=radius_miles,
                    max_results=max_results,
                )
                all_leads.extend(yelp_leads)
                logger.info(f"Yelp returned {len(yelp_leads)} leads")
            except Exception as e:
                logger.error(f"Yelp discovery failed: {e}")
        
        if "linkedin" in sources:
            try:
                linkedin_leads = await self.linkedin.search(
                    query=query,
                    city=city,
                    state=state,
                    radius_miles=radius_miles,
                    max_results=max_results,
                )
                all_leads.extend(linkedin_leads)
                logger.info(f"LinkedIn returned {len(linkedin_leads)} leads")
            except Exception as e:
                logger.error(f"LinkedIn discovery failed: {e}")
        
        if "colorado_sos" in sources:
            try:
                sos_leads = await self.colorado_sos.search(
                    query=query,
                    city=city,
                    state=state,
                    radius_miles=radius_miles,
                    max_results=max_results,
                )
                all_leads.extend(sos_leads)
                logger.info(f"Colorado SOS returned {len(sos_leads)} leads")
            except Exception as e:
                logger.error(f"Colorado SOS discovery failed: {e}")
        
        # Deduplicate by business_name + city
        seen = set()
        unique_leads = []
        for lead in all_leads:
            key = (lead.get("business_name", "").lower(), lead.get("city", "").lower())
            if key not in seen and lead.get("business_name"):
                seen.add(key)
                unique_leads.append(lead)
        
        logger.info(f"DiscoveryAgent: {len(unique_leads)} unique leads found")
        
        # Paperclip: log discovery run
        try:
            on_discovery_complete(
                query=query,
                city=city,
                leads_found=len(all_leads),
                leads_created=len(unique_leads),
            )
        except Exception:
            pass  # Never break main flow
        
        return unique_leads
