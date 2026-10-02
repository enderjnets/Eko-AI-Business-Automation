"""SerpApi client for search engine results (Google, Bing, etc.)."""

import logging
from typing import Optional, List, Dict, Any

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

SERPAPI_BASE_URL = "https://serpapi.com/search"


class SerpApiClient:
    """Client for SerpApi — structured search engine results.

    Free tier: 100 searches/month.
    Get a key at: https://serpapi.com/dashboard
    """

    def __init__(self, api_key: Optional[str] = None):
        settings = get_settings()
        self.api_key = api_key or settings.SERPAPI_API_KEY or ""
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
        )

    async def search_google(
        self,
        query: str,
        num_results: int = 10,
        location: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search Google via SerpApi and return organic results."""
        if not self.api_key:
            raise ValueError("SerpApi API key not configured. Get one free at https://serpapi.com/dashboard")

        params = {
            "engine": "google",
            "q": query,
            "num": min(num_results, 100),
            "api_key": self.api_key,
            "output": "json",
        }
        if location:
            params["location"] = location

        resp = await self.client.get(SERPAPI_BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        # Check for SerpApi errors
        if "error" in data:
            raise RuntimeError(f"SerpApi error: {data['error']}")

        organic = data.get("organic_results", [])
        logger.info(f"SerpApi Google search returned {len(organic)} results for: {query}")
        return organic

    async def search_google_maps(self, query: str, start: int = 0) -> List[Dict[str, Any]]:
        """Search Google Maps via SerpApi and return one page (up to 20) of local results.

        Each call is one SerpApi search. Pages advance by 20 through `start`.
        """
        if not self.api_key:
            raise ValueError("SerpApi API key not configured. Get one free at https://serpapi.com/dashboard")

        params = {
            "engine": "google_maps",
            "type": "search",
            "q": query,
            "start": start,
            "hl": "en",
            "gl": "us",
            "api_key": self.api_key,
            "output": "json",
        }

        resp = await self.client.get(SERPAPI_BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise RuntimeError(f"SerpApi error: {data['error']}")

        local = data.get("local_results", [])
        logger.info(f"SerpApi Google Maps returned {len(local)} places for: {query} (start={start})")
        return local

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
