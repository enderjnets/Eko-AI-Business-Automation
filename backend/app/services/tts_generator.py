"""Text-to-Speech generator for AI Analysis audio notes.

Uses ElevenLabs TTS with a single multilingual female voice (Sarah/Bella)
for both English and Spanish — keeps the brand voice consistent across
languages. Includes a Redis-backed quota breaker so a single
`quota_exceeded` response from ElevenLabs short-circuits every subsequent
TTS attempt for the rest of the billing window, instead of hammering the
API and filling the logs with 401s.
"""

import os
import logging
from typing import Optional
from datetime import datetime, timezone, timedelta

import httpx

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# ElevenLabs voice IDs. We use the SAME female voice for EN and ES so the
# brand sounds consistent in both languages (multilingual_v2 handles the
# accent / intonation natively). Sarah / Bella was chosen because it is
# already the voice used by VAPI inbound calls and has the warmest,
# most business-conversational tone in the multilingual library.
SARAH_BELLA = "EXAVITQu4vr4xnSDxMaL"

ELEVENLABS_VOICE_MAP = {
    "en": SARAH_BELLA,
    "es": SARAH_BELLA,
}
DEFAULT_VOICE = SARAH_BELLA


# ── Redis quota breaker ────────────────────────────────────────────────
# Mirrors the Resend quota breaker pattern from
# `app/agents/outreach/channels/email.py`. Once ElevenLabs returns 401
# with quota_exceeded, set this Redis key with a TTL of 24h (best-effort
# guess — most plans reset monthly but a 24h re-check is conservative).
_QUOTA_KEY = "tts:quota_exhausted:elevenlabs"
_QUOTA_TTL_SECONDS = 24 * 60 * 60


def _redis_client():
    try:
        import redis
        return redis.from_url(settings.REDIS_URL, decode_responses=True)
    except Exception as e:
        logger.warning(f"TTS quota breaker: redis unavailable ({e})")
        return None


def _is_tts_quota_breaker_open() -> bool:
    r = _redis_client()
    if not r:
        return False
    try:
        return bool(r.get(_QUOTA_KEY))
    except Exception as e:
        logger.warning(f"TTS quota breaker: redis read failed ({e})")
        return False


def _trip_tts_quota_breaker(reason: str) -> None:
    r = _redis_client()
    if not r:
        return
    try:
        r.set(_QUOTA_KEY, reason[:200], ex=_QUOTA_TTL_SECONDS)
        until = (datetime.now(timezone.utc) + timedelta(seconds=_QUOTA_TTL_SECONDS)).isoformat()
        logger.warning(
            f"TTS circuit breaker TRIPPED: {reason}. "
            f"All TTS attempts paused for 24h (until {until})."
        )
    except Exception as e:
        logger.warning(f"TTS quota breaker: failed to set redis key ({e})")


async def generate_tts_audio(text: str, language: str = "en", output_path: str = "") -> Optional[str]:
    """Generate TTS audio using ElevenLabs and save to output_path.

    Returns the output_path on success, None on failure. Failure modes
    handled gracefully (no exception bubbles up):
      • API key missing → None + warning
      • Quota breaker open → None (no API call made)
      • 401 quota_exceeded → trip breaker + None
      • Other HTTP / network errors → None + warning
    """
    api_key = settings.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        logger.warning("[TTS] ELEVENLABS_API_KEY not configured")
        return None

    # Short-circuit if a recent call already exhausted the plan quota —
    # avoids dozens of 401s per hour while the user upgrades their plan.
    if _is_tts_quota_breaker_open():
        logger.info("[TTS] Quota breaker open, skipping ElevenLabs call")
        return None

    voice_id = ELEVENLABS_VOICE_MAP.get(language[:2].lower(), DEFAULT_VOICE)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                    },
                },
            )
            response.raise_for_status()

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.info(f"[TTS] Audio saved: {output_path} ({len(response.content)} bytes)")
            return output_path

    except httpx.HTTPStatusError as e:
        # Detect ElevenLabs quota exhausted ('quota_exceeded' code) and
        # trip the breaker so the next ~24h of TTS calls short-circuit.
        body_text = ""
        try:
            body_text = e.response.text.lower()
        except Exception:
            pass
        is_quota = e.response.status_code == 401 and (
            "quota_exceeded" in body_text or "exceeds your quota" in body_text
        )
        logger.warning(f"[TTS] HTTP error {e.response.status_code}: {e.response.text[:200]}")
        if is_quota:
            _trip_tts_quota_breaker(f"HTTP 401 quota_exceeded: {body_text[:160]}")
        return None
    except Exception as e:
        logger.warning(f"[TTS] Error: {e}")
        return None


def build_voice_script(lead, lang: str = "en") -> str:
    """Build a concise, natural-sounding voice script from the lead analysis.

    Returns a ~300-500 character script optimized for TTS.
    """
    from app.services.lead_analysis_generator import _t

    business_name = lead.business_name or _t(lang, "default_business_name")
    total_score = lead.total_score or 0
    client_score = 100 - total_score

    pain_points_text = ""
    if lead.pain_points and len(lead.pain_points) >= 1:
        pain_points_text = ", ".join(lead.pain_points[:2])
    else:
        pain_points_text = _t(lang, "no_data")

    if lang == "es":
        script = (
            f"Hola, soy Eva de Eko AI. Analicé {business_name} y descubrí que tu negocio "
            f"está aprovechando solo una fracción de su potencial digital. "
            f"Tu puntuación de automatización es {client_score} de cien. "
            f"Eso significa que hay muchas oportunidades para capturar más clientes, "
            f"automatizar reservas, y nunca perder una llamada. "
            f"Los puntos más importantes que detecté: {pain_points_text}. "
            f"Podemos ayudarte a implementar un agente de IA que atienda llamadas veinticuatro siete, "
            f"confirme citas automáticamente, y haga seguimiento con tus clientes. "
            f"Agenda una demo gratuita de quince minutos y te muestro exactamente cómo funciona."
        )
    else:
        script = (
            f"Hi, this is Eva from Eko AI. I analyzed {business_name} and found that your business "
            f"is only using a fraction of its digital potential. "
            f"Your automation score is {client_score} out of one hundred. "
            f"That means there are major opportunities to capture more customers, "
            f"automate bookings, and never miss a call again. "
            f"The top issues I detected: {pain_points_text}. "
            f"We can help you deploy an AI agent that answers calls twenty-four seven, "
            f"confirms appointments automatically, and follows up with your customers. "
            f"Book a free fifteen-minute demo and I'll show you exactly how it works."
        )

    return script
