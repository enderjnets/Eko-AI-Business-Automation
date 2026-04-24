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

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
