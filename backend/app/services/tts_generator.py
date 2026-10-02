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


# ─── v0.7.X: Coqui XTTS-v2 local server (PRIMARY TTS) ──────────────────
COQUI_TTS_URL = os.environ.get("COQUI_TTS_URL", "http://127.0.0.1:7777/tts")
# Voice cloned from lead_601.mp3 (Sarah/Bella ElevenLabs reference)
COQUI_VOICE_BY_LANG = {
    "es": "spanish_female",
    "en": "spanish_female",  # Sarah/Bella speaks both
}


async def _coqui_tts(text: str, language: str, output_path: str) -> Optional[str]:
    """Call local Coqui XTTS-v2 server (~/coqui-xtts/server.py on ROG)."""
    voice = COQUI_VOICE_BY_LANG.get(language[:2].lower(), "spanish_female")
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                COQUI_TTS_URL,
                json={
                    "text": text,
                    "voice": voice,
                    "speed": 1.10,           # +10% A/B-tested sweet spot
                    "language": "es" if language[:2].lower() == "es" else "en",
                    "padding": True,         # adds "Gracias por escuchar." buffer (avoids cut-off)
                    "format": "mp3",
                },
            )
            response.raise_for_status()
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            gen_time = response.headers.get("X-Generation-Time-Sec", "?")
            logger.info(f"[TTS Coqui] saved {output_path} ({len(response.content)} bytes, gen={gen_time}s)")
            return output_path
    except httpx.HTTPStatusError as e:
        logger.warning(f"[TTS Coqui] HTTP {e.response.status_code}: {e.response.text[:200]}")
        return None
    except Exception as e:
        logger.warning(f"[TTS Coqui] error: {e}")
        return None


async def generate_tts_audio(text: str, language: str = "en", output_path: str = "") -> Optional[str]:
    """Generate TTS audio: Coqui XTTS-v2 PRIMARY (free, local) -> ElevenLabs fallback.

    v0.7.X: Coqui XTTS-v2 server on ROG clones Sarah/Bella voice. Free, no quota.
    ElevenLabs kept as fallback during 1-week validation period before cancellation.
    """
    # 1. PRIMARY: Coqui XTTS-v2 local (free, no quota)
    result = await _coqui_tts(text, language, output_path)
    if result:
        return result

    logger.warning("[TTS] Coqui local failed, falling back to ElevenLabs")

    # 2. FALLBACK: ElevenLabs (legacy, remove after week 1 validation)
    api_key = settings.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        logger.warning("[TTS] ELEVENLABS_API_KEY not configured — no fallback available")
        return None

    if _is_tts_quota_breaker_open():
        logger.info("[TTS] Quota breaker open, skipping ElevenLabs fallback")
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
            logger.info(f"[TTS ElevenLabs fallback] saved {output_path} ({len(response.content)} bytes)")
            return output_path

    except httpx.HTTPStatusError as e:
        body_text = ""
        try:
            body_text = e.response.text.lower()
        except Exception:
            pass
        is_quota = e.response.status_code == 401 and (
            "quota_exceeded" in body_text or "exceeds your quota" in body_text
        )
        logger.warning(f"[TTS ElevenLabs] HTTP error {e.response.status_code}: {e.response.text[:200]}")
        if is_quota:
            _trip_tts_quota_breaker(f"HTTP 401 quota_exceeded: {body_text[:160]}")
        return None
    except Exception as e:
        logger.warning(f"[TTS ElevenLabs] error: {e}")
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
