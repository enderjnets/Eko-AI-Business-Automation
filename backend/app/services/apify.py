"""Generic Apify client for running actors and fetching results."""

import logging
from typing import Optional, List, Dict, Any
import httpx

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

APIFY_BASE_URL = "https://api.apify.com/v2"


class ApifyClient:
    """Client for Apify API — run actors and fetch datasets."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.APIFY_API_KEY
        self.client = httpx.AsyncClient(
            base_url=APIFY_BASE_URL,
            timeout=httpx.Timeout(30.0, connect=10.0),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

    async def run_actor(
        self,
        actor_id: str,
        run_input: Dict[str, Any],
        wait_for_finish: bool = True,
        max_wait_seconds: int = 60,
    ) -> List[Dict]:
        """
        Start an actor run and optionally wait for completion.
        Returns dataset items.
        """
        if not self.api_key:
            raise ValueError("Apify API key is not configured")

        # Start run
        url = f"/acts/{actor_id}/runs"
        resp = await self.client.post(
            url,
            json=run_input,
            params={"waitForFinish": 0},
        )
        resp.raise_for_status()
        run_data = resp.json().get("data", {})
        run_id = run_data.get("id")
        dataset_id = run_data.get("defaultDatasetId")

        if not run_id:
            raise RuntimeError("Apify did not return a run ID")

        logger.info(f"Apify run started: {run_id} for actor {actor_id}")

        if wait_for_finish:
            dataset_id = await self._wait_for_run(
                run_id, max_wait_seconds=max_wait_seconds
            )

        # Fetch results
        items = await self._get_dataset_items(dataset_id)
        logger.info(f"Apify actor {actor_id} returned {len(items)} items")
        return items

    async def _wait_for_run(
        self,
        run_id: str,
        max_wait_seconds: int = 60,
        poll_interval: float = 2.0,
    ) -> str:
        """Poll run status until finished or timeout. Returns datasetId."""
        import asyncio

        elapsed = 0.0
        while elapsed < max_wait_seconds:
            resp = await self.client.get(f"/runs/{run_id}")
            resp.raise_for_status()
            data = resp.json().get("data", {})
            status = data.get("status")
            dataset_id = data.get("defaultDatasetId")

            if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
                if status != "SUCCEEDED":
                    raise RuntimeError(f"Apify run {run_id} finished with status: {status}")
                return dataset_id

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(f"Apify run {run_id} did not finish within {max_wait_seconds}s")

    async def _get_dataset_items(self, dataset_id: Optional[str]) -> List[Dict]:
        """Fetch all items from a dataset."""
        if not dataset_id:
            return []

        resp = await self.client.get(
            f"/datasets/{dataset_id}/items",
            params={"clean": "true", "limit": 500},
        )
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
