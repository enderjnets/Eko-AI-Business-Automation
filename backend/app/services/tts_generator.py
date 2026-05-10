"""Text-to-Speech generator for AI Analysis audio notes.

Uses ElevenLabs TTS with the same voices as VAPI calls and BitTrader content.
"""

import os
from typing import Optional
import httpx

from app.config import get_settings

settings = get_settings()

# ElevenLabs voice mapping by language
# Rachel = EXAVITQu4vr4xnSDxMaL (same as VAPI calls)
# Fernando Martínez = dlGxemPxFMTY7iXagmOj (BitTrader Spanish content)
ELEVENLABS_VOICE_MAP = {
    "es": "dlGxemPxFMTY7iXagmOj",   # Fernando Martínez — BitTrader Spanish
    "en": "EXAVITQu4vr4xnSDxMaL",  # Rachel — same as VAPI calls
}

DEFAULT_VOICE = "EXAVITQu4vr4xnSDxMaL"


async def generate_tts_audio(text: str, language: str = "en", output_path: str = "") -> Optional[str]:
    """Generate TTS audio using ElevenLabs and save to output_path.

    Returns the output_path on success, None on failure.
    """
    api_key = settings.ELEVENLABS_API_KEY or os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        print("[TTS] ELEVENLABS_API_KEY not configured")
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

            print(f"[TTS] Audio saved: {output_path} ({len(response.content)} bytes)")
            return output_path

    except httpx.HTTPStatusError as e:
        print(f"[TTS] HTTP error {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        print(f"[TTS] Error: {e}")
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
