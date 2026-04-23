import httpx
from typing import Optional, List, Dict
from app.config import get_settings

settings = get_settings()

OUTSCRAPER_BASE_URL = "https://api.app.outscraper.com"


class OutscraperClient:
    """Client for Outscraper API — Google Maps and local business data."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OUTSCRAPER_API_KEY
        self.client = httpx.AsyncClient(
            base_url=OUTSCRAPER_BASE_URL,
            timeout=60.0,
            headers={"X-API-KEY": self.api_key},
        )
    
    async def search_google_maps(
        self,
        query: str,
        limit: int = 50,
        skip: int = 0,
        language: str = "en",
        region: Optional[str] = None,
    ) -> List[Dict]:
        """
        Search Google Maps for businesses.
        
        Args:
            query: Search query, e.g. "restaurants in Denver, CO"
            limit: Max results (max 500)
            skip: Offset for pagination
            language: Language code
            region: Country code (e.g. 'us')
        """
        params = {
            "query": query,
            "limit": min(limit, 500),
            "skip": skip,
            "language": language,
            "async": "false",
        }
        if region:
            params["region"] = region
        
        response = await self.client.get("/maps/search-v3", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Outscraper returns data in .data field
        return data.get("data", []) if isinstance(data, dict) else data
    
    async def search_places(
        self,
        query: str,
        coordinates: Optional[str] = None,
        radius: int = 25000,  # meters
        limit: int = 50,
    ) -> List[Dict]:
        """
        Search places with geographic coordinates.
        
        Args:
            query: Business type or name
            coordinates: "lat,lon" format
            radius: Search radius in meters
            limit: Max results
        """
        params = {
            "query": query,
            "limit": min(limit, 500),
            "async": "false",
        }
        if coordinates:
            params["coordinates"] = coordinates
            params["radius"] = radius
        
        response = await self.client.get("/maps/search-v3", params=params)
        response.raise_for_status()
        data = response.json()
        
        return data.get("data", []) if isinstance(data, dict) else data
    
    async def close(self):
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()
