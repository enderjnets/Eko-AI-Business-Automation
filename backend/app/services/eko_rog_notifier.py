"""Send notifications to Eko Rog via Telegram Bot API."""
import logging
import httpx

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def _get_bot_token() -> str:
    return getattr(settings, "TELEGRAM_BOT_TOKEN", "")


def _get_chat_id() -> str:
    return str(getattr(settings, "TELEGRAM_CHAT_ID", ""))


async def notify_eko_rog(message: str, parse_mode: str = "HTML") -> dict:
    """Send a notification message to Eko Rog via Telegram.

    Args:
        message: The message text (HTML allowed if parse_mode="HTML")
        parse_mode: "HTML", "Markdown", or "MarkdownV2"

    Returns:
        Telegram API response or error dict
    """
    token = _get_bot_token()
    chat_id = _get_chat_id()

    if not token or not chat_id:
        logger.warning("Telegram bot token or chat ID not configured, skipping Eko Rog notification")
        return {"status": "skipped", "reason": "not_configured"}

    url = TELEGRAM_API_URL.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                logger.info("Eko Rog notification sent successfully")
                return {"status": "sent", "message_id": data["result"]["message_id"]}
            else:
                logger.warning(f"Telegram API returned error: {data}")
                return {"status": "error", "detail": data}
        except httpx.HTTPStatusError as e:
            logger.error(f"Telegram HTTP error: {e.response.status_code} {e.response.text}")
            return {"status": "error", "code": e.response.status_code, "detail": e.response.text}
        except Exception as e:
            logger.error(f"Failed to notify Eko Rog: {e}")
            return {"status": "error", "detail": str(e)}


def format_booking_notification(
    business_name: str,
    caller_name: str,
    phone: str,
    date_str: str,
    time_str: str,
    contact_method: str,
    notes: str = "",
    calendar_link: str = "",
) -> str:
    """Format a rich HTML message for a new booking via VAPI inbound call."""
    msg = f"""<b>📞 New Demo Booked via Voice Call</b>

<b>Business:</b> {business_name}
<b>Contact:</b> {caller_name}
<b>Phone:</b> {phone}
<b>Date:</b> {date_str}
<b>Time:</b> {time_str} MT
<b>Method:</b> {contact_method}"""

    if notes:
        msg += f"\n<b>Notes:</b> {notes}"

    if calendar_link:
        msg += f"\n\n<a href='{calendar_link}'>➕ Add to Google Calendar</a>"

    return msg


def format_call_notification(
    business_name: str,
    duration: str,
    interest_level: str,
    summary: str,
    recording_url: str = "",
    lead_url: str = "",
) -> str:
    """Format a rich HTML message for an inbound call summary."""
    interest_emoji = {
        "HIGH": "🔥",
        "MEDIUM": "⚡",
        "LOW": "📉",
        "NONE": "😐",
    }.get(interest_level, "📞")

    msg = f"""<b>{interest_emoji} Inbound Call Completed</b>

<b>Business:</b> {business_name}
<b>Duration:</b> {duration}
<b>Interest:</b> {interest_level}

<b>Summary:</b>
{summary[:800]}"""

    if recording_url and recording_url != "#":
        msg += f"\n\n<a href='{recording_url}'>🎙 Listen to Recording</a>"

    if lead_url and lead_url != "#":
        msg += f"\n<a href='{lead_url}'>👤 View Lead Profile</a>"

    return msg
