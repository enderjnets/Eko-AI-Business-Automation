import httpx
from typing import Optional, Dict
from datetime import datetime

from app.config import get_settings

settings = get_settings()

CAL_COM_BASE_URL = "https://api.cal.com/v1"


class CalComClient:
    """Client for Cal.com API — appointment scheduling."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.CAL_COM_API_KEY
        self.client = httpx.AsyncClient(
            base_url=CAL_COM_BASE_URL,
            timeout=30.0,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
    
    async def get_event_types(self) -> list:
        """Get available event types (meeting types)."""
        try:
            response = await self.client.get("/event-types")
            response.raise_for_status()
            data = response.json()
            return data.get("event_types", [])
        except Exception as e:
            print(f"Cal.com error: {e}")
            return []
    
    async def get_available_slots(
        self,
        event_type_id: int,
        start_date: str,  # YYYY-MM-DD
        end_date: str,
    ) -> list:
        """Get available time slots for an event type."""
        try:
            response = await self.client.get(
                "/availability",
                params={
                    "eventTypeId": event_type_id,
                    "startTime": start_date,
                    "endTime": end_date,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("slots", [])
        except Exception as e:
            print(f"Cal.com error: {e}")
            return []
    
    async def create_booking(
        self,
        event_type_id: int,
        start_time: str,  # ISO 8601
        attendee_email: str,
        attendee_name: str,
        metadata: Optional[Dict] = None,
    ) -> Dict:
        """Create a booking."""
        try:
            payload = {
                "eventTypeId": event_type_id,
                "start": start_time,
                "responses": {
                    "email": attendee_email,
                    "name": attendee_name,
                },
                "metadata": metadata or {},
                "timeZone": "America/Denver",
            }
            
            response = await self.client.post("/bookings", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Cal.com error: {e}")
            return {"error": str(e)}
    
    async def cancel_booking(
        self,
        booking_id: int,
        reason: Optional[str] = None,
    ) -> Dict:
        """Cancel a booking."""
        try:
            payload = {"reason": reason or "Cancelled by system"}
            response = await self.client.post(f"/bookings/{booking_id}/cancel", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Cal.com error: {e}")
            return {"error": str(e)}
    
    async def close(self):
        await self.client.aclose()
