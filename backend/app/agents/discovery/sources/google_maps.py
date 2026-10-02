from typing import List, Dict, Optional
import logging

from app.services.serpapi import SerpApiClient

logger = logging.getLogger(__name__)

PAGE_SIZE = 20
# SerpApi docs: past page six (start=100) results get duplicated or irrelevant.
MAX_START = 100


class GoogleMapsSource:
    """Discovery source using SerpApi's Google Maps engine (one search per page of 20)."""

    def __init__(self):
        self.client = SerpApiClient()
    
    async def search(
        self,
        query: str,
        city: str,
        state: Optional[str] = "CO",
        radius_miles: int = 25,
        max_results: int = 50,
    ) -> List[Dict]:
        """
        Search for businesses on Google Maps.
        
        Args:
            query: Business category (e.g., "restaurants", "salons", "plumbers")
            city: City name
            state: State code
            radius_miles: Search radius
            max_results: Maximum results to return
        """
        search_query = f"{query} in {city}, {state}"
        logger.info(f"Google Maps discovery: {search_query}")
        
        results = []
        start = 0
        while len(results) < max_results and start <= MAX_START:
            try:
                page = await self.client.search_google_maps(query=search_query, start=start)
            except Exception as e:
                logger.error(f"SerpApi Google Maps error at start={start}: {e}")
                break
            results.extend(page)
            if len(page) < PAGE_SIZE:
                break
            start += PAGE_SIZE

        leads = []
        for place in results[:max_results]:
            if not isinstance(place, dict):
                continue
            
            lead = self._normalize_place(place)
            if lead:
                leads.append(lead)
        
        logger.info(f"Found {len(leads)} leads from Google Maps")
        return leads
    
    def _normalize_place(self, place: Dict) -> Optional[Dict]:
        """Normalize a Google Maps place (SerpApi fields, or Outscraper-style ones) to Lead format."""
        name = place.get("name") or place.get("title")
        if not name:
            return None
        
        # Extract address components
        address = place.get("address", "")
        full_address = place.get("full_address", address)
        
        # Extract city/state from address or subfields
        city = place.get("city", "")
        state = place.get("state", "")
        zip_code = place.get("postal_code", "") or place.get("zip", "")

        # Try to parse from full_address if city/state missing
        if not city and full_address:
            parts = [p.strip() for p in full_address.split(",")]
            if len(parts) >= 2:
                city = parts[-2]
            if len(parts) >= 1:
                state_zip = parts[-1].strip().split()
                if state_zip:
                    state = state_zip[0]
                if len(state_zip) > 1 and not zip_code:
                    zip_code = state_zip[1]
        
        # Extract phone - Outscraper may have it in different fields
        phone = place.get("phone", "") or place.get("phone_number", "")
        
        # Extract website
        website = place.get("site", "") or place.get("website", "")
        
        # Extract email - may be empty from Google Maps
        email = place.get("email", "")
        
        # Extract category/type
        types = place.get("type", "") or place.get("category", "")
        if isinstance(types, list):
            category = types[0] if types else ""
        else:
            category = types
        
        # Coordinates
        latitude = place.get("latitude")
        longitude = place.get("longitude")
        if latitude is None:
            # SerpApi: gps_coordinates {latitude, longitude}; others: location {lat, lng}
            loc = place.get("gps_coordinates") or place.get("location")
            if isinstance(loc, dict):
                latitude = loc.get("latitude", loc.get("lat"))
                longitude = loc.get("longitude", loc.get("lng"))
        
        return {
            "business_name": name.strip(),
            "category": category.strip() if category else None,
            "description": place.get("description", "") or place.get("about", ""),
            "email": email if email else None,
            "phone": phone if phone else None,
            "website": website if website else None,
            "address": full_address if full_address else None,
            "city": city if city else None,
            "state": state if state else None,
            "zip_code": zip_code,
            "country": "US",
            "latitude": latitude,
            "longitude": longitude,
            "source": "google_maps",
            "source_data": place,
        }
