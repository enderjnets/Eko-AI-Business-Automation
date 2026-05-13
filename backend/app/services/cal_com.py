import httpx
from typing import Optional, Dict
from datetime import datetime

from app.config import get_settings

settings = get_settings()

CAL_COM_BASE_URL = "https://api.cal.com/v2"
CAL_API_VERSION = "2024-08-13"


class CalComClient:
    """Client for Cal.com API v2 — appointment scheduling."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.CAL_COM_API_KEY
        self.username = settings.CAL_COM_USERNAME or "ender-ocando-lfxtkn"
        self.client = httpx.AsyncClient(
            base_url=CAL_COM_BASE_URL,
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "cal-api-version": CAL_API_VERSION,
                "Content-Type": "application/json",
            },
        )

    async def get_event_types(self) -> list:
        """Get available event types (meeting types)."""
        # v2 event-types endpoint requires OAuth app auth; skip for now
        return []

    async def get_available_slots(
        self,
        event_type_slug: str,
        start_date: str,  # YYYY-MM-DD
        end_date: str,
    ) -> list:
        """Get available time slots for an event type."""
        # v2 slots endpoint requires OAuth app auth; skip for now
        return []

    async def create_booking(
        self,
        start_time: str,  # ISO 8601
        attendee_email: str,
        attendee_name: str,
        event_type_slug: str = "15min",
        attendee_phone: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> Dict:
        """Create a booking via Cal.com v2 API."""
        try:
            payload = {
                "eventTypeSlug": event_type_slug,
                "username": self.username,
                "start": start_time,
                "attendee": {
                    "email": attendee_email,
                    "name": attendee_name,
                    "timeZone": "America/Denver",
                },
                "metadata": {k: str(v) for k, v in (metadata or {}).items()},
            }
            if attendee_phone:
                payload["attendee"]["phone"] = attendee_phone

            response = await self.client.post("/bookings", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data) if isinstance(data, dict) else data
        except httpx.HTTPStatusError as e:
            print(f"Cal.com HTTP error: {e.response.status_code} — {e.response.text}")
            return {"error": f"HTTP {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            print(f"Cal.com error: {e}")
            return {"error": str(e)}

    async def cancel_booking(
        self,
        booking_uid: str,
        reason: Optional[str] = None,
    ) -> Dict:
        """Cancel a booking by UID."""
        try:
            payload = {"reason": reason or "Cancelled by system"}
            response = await self.client.post(f"/bookings/{booking_uid}/cancel", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data) if isinstance(data, dict) else data
        except Exception as e:
            print(f"Cal.com error: {e}")
            return {"error": str(e)}

    async def close(self):
        await self.client.aclose()
