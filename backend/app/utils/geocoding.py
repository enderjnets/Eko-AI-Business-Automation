import logging
from typing import Optional
import httpx

logger = logging.getLogger(__name__)


async def geocode_address(
    address: str,
    city: str = "",
    state: str = "",
    zip_code: str = "",
    lead_id: Optional[int] = None,
) -> Optional[dict]:
    """Geocode an address using Nominatim with retry + detailed logging.

    Returns {"lat": float, "lng": float} or None.
    """
    parts = [p for p in [address, city, state, zip_code] if p]
    if not parts:
        logger.info(f"[geocode] No address parts for lead_id={lead_id}")
        return None

    query = ", ".join(parts)
    url = "https://nominatim.openstreetmap.org/search"
    params = {"format": "json", "q": query, "limit": 1}
    headers = {"User-Agent": "EkoAI-LeadManager/1.0"}

    last_error = None
    for attempt in range(1, 4):
        try:
            logger.info(
                f"[geocode] Attempt {attempt}/3 for lead_id={lead_id}: query='{query}'"
            )
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=headers)
                logger.info(
                    f"[geocode] Response status={res.status_code} for lead_id={lead_id}"
                )
                body = res.json()
                logger.debug(
                    f"[geocode] Response body (truncated): {str(body)[:500]}"
                )

                if not body:
                    logger.warning(
                        f"[geocode] Empty response from Nominatim for lead_id={lead_id}"
                    )
                    return None

                # Nominatim may return a dict on error
                if isinstance(body, dict):
                    logger.warning(
                        f"[geocode] Nominatim returned dict (likely error) for lead_id={lead_id}: {body}"
                    )
                    return None

                if len(body) > 0 and "lat" in body[0] and "lon" in body[0]:
                    lat = float(body[0]["lat"])
                    lng = float(body[0]["lon"])
                    logger.info(
                        f"[geocode] SUCCESS lead_id={lead_id}: lat={lat}, lng={lng}"
                    )
                    return {"lat": lat, "lng": lng}
                else:
                    logger.warning(
                        f"[geocode] No lat/lon in response for lead_id={lead_id}: {body}"
                    )
                    return None

        except httpx.HTTPStatusError as e:
            last_error = e
            logger.warning(
                f"[geocode] HTTP error attempt {attempt}/3 for lead_id={lead_id}: {e}"
            )
        except Exception as e:
            last_error = e
            logger.warning(
                f"[geocode] Exception attempt {attempt}/3 for lead_id={lead_id}: {e}"
            )

        if attempt < 3:
            import asyncio

            delay = attempt  # 1s, 2s
            logger.info(f"[geocode] Retrying in {delay}s...")
            await asyncio.sleep(delay)

    logger.error(
        f"[geocode] FAILED after 3 attempts for lead_id={lead_id}: {last_error}"
    )
    return None
