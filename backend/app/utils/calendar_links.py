"""Generate Google Calendar add-to-calendar links."""
from datetime import datetime, timedelta, timezone
from urllib.parse import quote


def generate_google_calendar_link(
    title: str,
    start_time: datetime,
    end_time: datetime,
    description: str = "",
    location: str = "",
    timezone: str = "America/Denver",
) -> str:
    """Generate a Google Calendar 'Add to Calendar' link.

    Args:
        title: Event title
        start_time: Event start time (must be timezone-aware)
        end_time: Event end time (must be timezone-aware)
        description: Event description (HTML allowed)
        location: Event location
        timezone: IANA timezone name

    Returns:
        Google Calendar add URL
    """
    base_url = "https://calendar.google.com/calendar/render"

    def _fmt(dt: datetime) -> str:
        """Format datetime to UTC string for Google Calendar."""
        try:
            utc_dt = dt.astimezone(timezone.utc)
            return utc_dt.strftime("%Y%m%dT%H%M%SZ")
        except Exception:
            return dt.strftime("%Y%m%dT%H%M%SZ")

    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{_fmt(start_time)}/{_fmt(end_time)}",
        "details": description,
        "location": location,
        "ctz": timezone,
    }

    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items() if v)
    return f"{base_url}?{query}"
