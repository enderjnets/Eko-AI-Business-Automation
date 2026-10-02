"""Google Maps discovery through SerpApi (engine=google_maps).

The item below mirrors one entry of `local_results` from a live SerpApi
response (2026-10-02, "plumbers in Denver, CO"), with made-up business data.
"""

import httpx
import pytest

from app.agents.discovery.sources.google_maps import GoogleMapsSource
from app.services.serpapi import SerpApiClient


def serpapi_place(n: int = 1) -> dict:
    return {
        "position": n,
        "title": f"Mile High Plumbing {n}",
        "place_id": f"ChIJplace{n}",
        "gps_coordinates": {"latitude": 39.7583, "longitude": -105.0512},
        "rating": 4.8,
        "reviews": 120,
        "type": "Plumber",
        "types": ["Plumber", "HVAC contractor"],
        "address": "5000 W 29th Ave, Denver, CO 80212",
        "phone": "(303) 555-0100",
        "website": "https://milehighplumbing.example/",
    }


class FakeMapsClient:
    """Stands in for SerpApiClient: serves pages of 20 places, records offsets."""

    def __init__(self, total: int, fail_at_start: int | None = None):
        self.total = total
        self.fail_at_start = fail_at_start
        self.starts = []

    async def search_google_maps(self, query: str, start: int = 0):
        self.starts.append(start)
        if start == self.fail_at_start:
            raise RuntimeError("SerpApi error: Google hasn't returned any results for this query.")
        return [serpapi_place(n) for n in range(start + 1, min(start + 20, self.total) + 1)]


def source_with(client) -> GoogleMapsSource:
    source = GoogleMapsSource()
    source.client = client
    return source


class TestNormalizeSerpApiPlace:
    def test_maps_serpapi_fields_to_lead(self):
        lead = GoogleMapsSource()._normalize_place(serpapi_place())
        assert lead["business_name"] == "Mile High Plumbing 1"
        assert lead["category"] == "Plumber"
        assert lead["phone"] == "(303) 555-0100"
        assert lead["website"] == "https://milehighplumbing.example/"
        assert lead["address"] == "5000 W 29th Ave, Denver, CO 80212"
        assert lead["city"] == "Denver"
        assert lead["state"] == "CO"
        assert lead["source"] == "google_maps"

    def test_reads_coordinates_from_gps_coordinates(self):
        lead = GoogleMapsSource()._normalize_place(serpapi_place())
        assert lead["latitude"] == 39.7583
        assert lead["longitude"] == -105.0512

    def test_parses_zip_code_from_address(self):
        lead = GoogleMapsSource()._normalize_place(serpapi_place())
        assert lead["zip_code"] == "80212"


class TestSearchPagination:
    @pytest.mark.asyncio
    async def test_requests_pages_of_20_until_max_results(self):
        client = FakeMapsClient(total=200)
        leads = await source_with(client).search("plumbers", "Denver", max_results=50)
        assert client.starts == [0, 20, 40]
        assert len(leads) == 50

    @pytest.mark.asyncio
    async def test_stops_when_a_page_comes_back_short(self):
        client = FakeMapsClient(total=27)
        leads = await source_with(client).search("plumbers", "Denver", max_results=50)
        assert client.starts == [0, 20]
        assert len(leads) == 27

    @pytest.mark.asyncio
    async def test_never_requests_beyond_start_100(self):
        client = FakeMapsClient(total=1000)
        await source_with(client).search("plumbers", "Denver", max_results=500)
        assert client.starts == [0, 20, 40, 60, 80, 100]

    @pytest.mark.asyncio
    async def test_keeps_earlier_pages_when_a_later_page_fails(self):
        client = FakeMapsClient(total=200, fail_at_start=20)
        leads = await source_with(client).search("plumbers", "Denver", max_results=50)
        assert len(leads) == 20

    @pytest.mark.asyncio
    async def test_sends_city_and_state_in_the_query(self):
        seen = []

        class RecordingClient(FakeMapsClient):
            async def search_google_maps(self, query: str, start: int = 0):
                seen.append(query)
                return []

        await source_with(RecordingClient(total=0)).search("plumbers", "Denver", state="CO")
        assert seen == ["plumbers in Denver, CO"]


class TestSerpApiClientGoogleMaps:
    @pytest.mark.asyncio
    async def test_sends_google_maps_search_params_and_returns_local_results(self):
        captured = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured.update(request.url.params)
            return httpx.Response(200, json={"local_results": [serpapi_place()]})

        client = SerpApiClient(api_key="test-key")
        client.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        results = await client.search_google_maps("plumbers in Denver, CO", start=40)

        assert results == [serpapi_place()]
        assert captured["engine"] == "google_maps"
        assert captured["type"] == "search"
        assert captured["q"] == "plumbers in Denver, CO"
        assert captured["start"] == "40"
        assert captured["api_key"] == "test-key"

    @pytest.mark.asyncio
    async def test_raises_on_serpapi_error_body(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"error": "Invalid API key."})

        client = SerpApiClient(api_key="bad")
        client.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with pytest.raises(RuntimeError, match="Invalid API key"):
            await client.search_google_maps("plumbers in Denver, CO")
