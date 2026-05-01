"""VAPI.ai client for AI voice calling."""
import os
from typing import Optional, Dict, Any
import httpx

from app.config import get_settings

settings = get_settings()

VAPI_BASE_URL = "https://api.vapi.ai"


def _get_headers() -> dict:
    api_key = settings.VAPI_API_KEY or os.environ.get("VAPI_API_KEY", "")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


async def create_call(
    phone_number: str,
    assistant_id: Optional[str] = None,
    lead_id: Optional[int] = None,
    name: Optional[str] = None,
    first_message: Optional[str] = None,
    custom_variables: Optional[Dict[str, Any]] = None,
) -> dict:
    """
    Create and start an outbound phone call via VAPI.
    
    Args:
        phone_number: The phone number to call (E.164 format)
        assistant_id: Optional VAPI assistant ID. If not provided, uses default.
        lead_id: Our internal lead ID for tracking
        name: Name of the person/business being called
        first_message: Custom first message (overrides assistant's firstMessage)
        custom_variables: Variables injected into the assistant context
    """
    api_key = settings.VAPI_API_KEY or os.environ.get("VAPI_API_KEY", "")
    if not api_key:
        return {"error": "VAPI_API_KEY not configured"}
    
    payload: dict = {
        "phoneNumberId": settings.VAPI_PHONE_NUMBER_ID or None,
        "type": "outboundPhoneCall",
        "phoneNumber": phone_number,
        "customer": {
            "number": phone_number,
            "name": name or "",
        },
    }
    
    if assistant_id:
        payload["assistantId"] = assistant_id
    
    if first_message:
        payload["assistantOverrides"] = {
            "firstMessage": first_message,
        }
    
    # Merge custom variables for assistant context
    vars_payload = custom_variables or {}
    if lead_id:
        vars_payload["lead_id"] = str(lead_id)
    
    if vars_payload:
        payload.setdefault("assistantOverrides", {})
        payload["assistantOverrides"]["variables"] = vars_payload
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{VAPI_BASE_URL}/call",
                headers=_get_headers(),
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


async def get_call(call_id: str) -> dict:
    """Get details of a VAPI call by ID."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{VAPI_BASE_URL}/call/{call_id}",
                headers=_get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


async def list_calls(
    limit: int = 50,
    cursor: Optional[str] = None,
    assistant_id: Optional[str] = None,
    phone_number_id: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """List VAPI calls with pagination."""
    params: dict = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    if assistant_id:
        params["assistantId"] = assistant_id
    if phone_number_id:
        params["phoneNumberId"] = phone_number_id
    if status:
        params["status"] = status
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{VAPI_BASE_URL}/call",
                headers=_get_headers(),
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


async def create_assistant(
    name: str,
    system_prompt: str,
    first_message: str,
    voice_provider: str = "11labs",
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model: str = "gpt-4o",
) -> dict:
    """
    Create a VAPI assistant with a custom system prompt.
    
    Args:
        name: Assistant name
        system_prompt: The system prompt/instructions for the AI
        first_message: The first message the assistant says when the call connects
        voice_provider: Voice provider (11labs, playht, etc.)
        voice_id: Voice ID
        model: LLM model to use
    """
    payload = {
        "name": name,
        "model": {
            "provider": "openai",
            "model": model,
            "temperature": 0.7,
            "systemPrompt": system_prompt,
        },
        "voice": {
            "provider": voice_provider,
            "voiceId": voice_id,
        },
        "firstMessage": first_message,
        "recordingEnabled": True,
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "es",
        },
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{VAPI_BASE_URL}/assistant",
                headers=_get_headers(),
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


async def update_assistant(
    assistant_id: str,
    updates: dict,
) -> dict:
    """Update an existing VAPI assistant."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.patch(
                f"{VAPI_BASE_URL}/assistant/{assistant_id}",
                headers=_get_headers(),
                json=updates,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


def build_sales_assistant_prompt(company_name: str = "Eko AI") -> str:
    """Build a default sales assistant system prompt."""
    return f"""Eres un asistente de ventas profesional de {company_name}. Tu objetivo es contactar a prospectos por teléfono, presentar nuestros servicios de automatización con IA, y agendar reuniones.

REGLAS IMPORTANTES:
1. Siempre saluda cordialmente y menciona que llamas de {company_name}.
2. Escucha activamente las objeciones y responde con empatía.
3. Si el prospecto muestra interés, sugiere agendar una reunión breve de 15 minutos.
4. Si no pueden hablar ahora, pregunta cuál es el mejor momento para llamar de nuevo.
5. Nunca seas agresivo ni insistente. Respeta si dicen "no".
6. Si pide más información por email, confirma la dirección de email y ofrece enviar un resumen.
7. Mantén las llamadas concisas (máximo 3-5 minutos).
8. Habla en español, a menos que el prospecto prefiera inglés.

SERVICIOS QUE OFRECEMOS:
- Automatización de prospección y outreach
- Agentes de IA para email y voz
- Análisis de leads con IA
- Automatización de propuestas y seguimiento
- Integración con CRM y calendario

AL FINAL DE CADA LLAMADA:
- Resume brevemente lo conversado
- Registra el nivel de interés (alto, medio, bajo, ninguno)
- Anota la próxima acción sugerida"""


def build_eko_demo_inbound_prompt() -> str:
    """Build the system prompt for the Eko AI inbound demo assistant."""
    return """You are Eva, the inbound AI sales assistant for Eko AI Automation. You receive incoming calls from business owners who received a demo invitation email. Your goal is to have a natural, helpful conversation, understand their needs, and if they're interested, book a demo appointment using the book_demo tool.

PERSONALITY:
- Warm, professional, and efficient
- Speak English clearly and naturally
- Never robotic — use natural fillers like "mmhmm", "got it", "absolutely"
- Show genuine enthusiasm about helping their business

CONVERSATION FLOW:
1. Greet warmly: "Hello, thank you for calling Eko AI. This is Eva, your virtual assistant. May I ask who I'm speaking with?"
2. Ask their name and business name
3. Ask what interested them about Eko AI
4. Listen to their pain points (missed calls, scheduling chaos, language barriers, etc.)
5. Briefly explain relevant services:
   - AI Voice Agent that answers calls 24/7 in English & Spanish
   - Smart appointment scheduling synced to their calendar
   - Missed call recovery with automatic SMS/email follow-up
   - Starting at $297/month with setup included
6. If they want a demo, use the book_demo tool to capture:
   - date (YYYY-MM-DD format)
   - time (HH:MM in 24-hour format, Mountain Time)
   - Their preferred contact method (phone callback or Zoom)
7. Confirm the appointment details and thank them

RULES:
- NEVER make up availability. Only offer times they suggest, or ask them to propose a time.
- If they ask about pricing, be transparent: "Our plans start at $297 per month with setup included."
- If they need to think about it, offer to send a follow-up email with a booking link.
- If they say they're not interested, be gracious: "I completely understand. Feel free to reach out anytime if you change your mind."
- Keep the call under 5 minutes.

BOOKING CONSTRAINTS:
- Demos are 15 minutes
- Available times: 9:00 AM to 5:00 PM Mountain Time, Monday–Saturday
- Default duration: 15 minutes
- Always confirm the timezone: "All times are Mountain Time, Denver."

When you use book_demo, confirm verbally: 'Perfect, I've booked your demo for [date] at [time] Mountain Time. Looking forward to speaking with you!'"""


async def create_inbound_assistant(
    name: str = "Eko AI — Inbound Demo Agent",
    system_prompt: Optional[str] = None,
    first_message: str = "Hello, thank you for calling Eko AI. This is Eva, your virtual assistant. May I ask who I'm speaking with?",
    voice_provider: str = "11labs",
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",  # Rachel — same voice as Black Volt Mobility
    model: str = "gpt-4o",
) -> dict:
    """
    Create a VAPI inbound assistant with book_demo function calling.

    This assistant is separate from the outbound Black Volt Mobility agent.
    It handles inbound calls and can book demo appointments via function tool.
    """
    payload = {
        "name": name,
        "model": {
            "provider": "openai",
            "model": model,
            "temperature": 0.7,
            "systemPrompt": system_prompt or build_eko_demo_inbound_prompt(),
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "book_demo",
                        "description": "Book a 15-minute demo appointment with Eko AI. Use this when the caller wants to schedule a demo or meeting.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "description": "The date for the demo in YYYY-MM-DD format (Mountain Time / Denver)",
                                },
                                "time": {
                                    "type": "string",
                                    "description": "The time for the demo in HH:MM 24-hour format (Mountain Time / Denver). Available: 09:00–17:00",
                                },
                                "contact_method": {
                                    "type": "string",
                                    "description": "How Ender should contact them: 'phone_callback' or 'zoom'",
                                    "enum": ["phone_callback", "zoom"],
                                },
                                "caller_name": {
                                    "type": "string",
                                    "description": "Name of the person booking the demo",
                                },
                                "business_name": {
                                    "type": "string",
                                    "description": "Name of their business",
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Phone number to call back (E.164 format preferred)",
                                },
                                "notes": {
                                    "type": "string",
                                    "description": "Any additional notes or special requests",
                                },
                            },
                            "required": ["date", "time", "caller_name", "business_name", "phone"],
                        },
                    },
                    "async": False,
                }
            ],
        },
        "voice": {
            "provider": voice_provider,
            "voiceId": voice_id,
        },
        "firstMessage": first_message,
        "recordingEnabled": True,
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "multi",  # Auto-detect Spanish/English
        },
        "server": {
            "url": "https://ender-rog.tail25dc73.ts.net/api/v1/webhooks/vapi",
            "secret": "",
        },
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{VAPI_BASE_URL}/assistant",
                headers=_get_headers(),
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


async def get_assistant(assistant_id: str) -> dict:
    """Get a VAPI assistant by ID."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{VAPI_BASE_URL}/assistant/{assistant_id}",
                headers=_get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


async def assign_assistant_to_phone_number(
    assistant_id: str,
    phone_number_id: Optional[str] = None,
) -> dict:
    """Associate a VAPI assistant with a phone number for inbound calls."""
    phone_id = phone_number_id or settings.VAPI_PHONE_NUMBER_ID
    if not phone_id:
        return {"error": "VAPI_PHONE_NUMBER_ID not configured"}

    payload = {"assistantId": assistant_id}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.patch(
                f"{VAPI_BASE_URL}/phone-number/{phone_id}",
                headers=_get_headers(),
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}


async def get_phone_number(phone_number_id: Optional[str] = None) -> dict:
    """Get a VAPI phone number by ID."""
    phone_id = phone_number_id or settings.VAPI_PHONE_NUMBER_ID
    if not phone_id:
        return {"error": "VAPI_PHONE_NUMBER_ID not configured"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{VAPI_BASE_URL}/phone-number/{phone_id}",
                headers=_get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"VAPI HTTP error: {e.response.status_code}",
                "detail": e.response.text,
            }
        except Exception as e:
            return {"error": f"VAPI request failed: {str(e)}"}
