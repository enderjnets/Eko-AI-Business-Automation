import json
import re
from typing import Optional, List

from app.utils.ai_client import generate_completion
from app.models.lead import Lead, Interaction


def _build_booking_link(lead: Lead) -> str:
    """Build a pre-filled booking link for the lead."""
    from app.config import get_settings
    settings = get_settings()
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3001')
    phone_number = getattr(settings, 'VAPI_INBOUND_PHONE_NUMBER', '')
    email = lead.email or ""
    name = lead.business_name or ""
    return f"{frontend_url}/book-demo?email={email}&name={name}", phone_number


def _inject_booking_cta(body: str, booking_link: str, phone_number: str) -> tuple[str, bool]:
    """
    Post-process the AI body. If it suggests a meeting but doesn't contain
    the booking link or phone number, inject a styled CTA with both options.

    Returns (body, suggested_meeting).
    """
    # Check if body already contains the link
    if booking_link in body and phone_number in body:
        return body, True

    # Detect meeting intent keywords (English)
    meeting_keywords = [
        "call", "demo", "schedule", "calendar", "appointment",
        "meeting", "zoom", "google meet", "teams", "chat",
        "talk", "speak", "connect", "15 minutes", "15 min",
    ]
    lower_body = body.lower()
    has_meeting_intent = any(kw in lower_body for kw in meeting_keywords)

    if not has_meeting_intent:
        return body, False

    # Inject styled HTML CTA with both options
    cta = f"""
<div style="margin-top:24px;padding:20px;background:#0F172A;border-radius:10px;border:1px solid rgba(255,255,255,0.08);">
  <p style="margin:0 0 12px;font-size:14px;font-weight:600;color:#E2E8F0;">Ready to see it in action?</p>
  <table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td width="50%" style="padding-right:6px;">
        <a href="tel:{phone_number}" style="display:block;background:linear-gradient(135deg,#0B4FD8,#7C3AED);color:#fff;text-decoration:none;padding:12px 0;border-radius:8px;font-size:14px;font-weight:600;text-align:center;">📞 Call {phone_number}</a>
      </td>
      <td width="50%" style="padding-left:6px;">
        <a href="{booking_link}" style="display:block;background:transparent;color:#fff;text-decoration:none;padding:12px 0;border-radius:8px;font-size:14px;font-weight:600;text-align:center;border:2px solid rgba(255,255,255,0.15);">Book Online →</a>
      </td>
    </tr>
  </table>
  <p style="margin:10px 0 0;font-size:12px;color:#64748B;">Our AI assistant answers calls 24/7 and can book your demo instantly.</p>
</div>
"""
    body = body.rstrip() + "\n" + cta
    return body, True


async def generate_ai_reply(
    lead: Lead,
    inbound_email: Interaction,
    conversation_history: List[Interaction],
    tone: str = "professional",
    max_length: str = "medium",
    custom_instructions: Optional[str] = None,
) -> dict:
    """
    Generate an AI-powered reply to an inbound email.

    Returns: {
        "subject": str,
        "body": str,
        "tone": str,
        "confidence": float,
        "suggested_next_action": str,
        "suggested_meeting": bool,
        "booking_link": str,
    }
    """

    booking_link, phone_number = _build_booking_link(lead)

    # Build conversation context
    history_text = ""
    for i, interaction in enumerate(conversation_history[-5:]):  # Last 5 interactions
        direction = "Us" if interaction.direction == "outbound" else "Lead"
        history_text += f"\n[{direction}] {interaction.subject or 'No subject'}:\n{interaction.content or ''}\n"

    # Lead context
    lead_context = f"""Lead information:
- Business name: {lead.business_name}
- Category: {lead.category or 'Not specified'}
- City: {lead.city or 'Not specified'}
- Pipeline status: {lead.status.value if lead.status else 'unknown'}
- Description: {lead.description or 'Not available'}
- Services: {', '.join(lead.services or []) or 'Not specified'}
- Pain points: {', '.join(lead.pain_points or []) or 'Not identified'}
- Score: {lead.total_score or 0}/100
"""

    # Inbound email analysis
    inbound_analysis = f"""Received email:
Subject: {inbound_email.subject or 'No subject'}
Content: {inbound_email.content or ''}
"""

    # Get AI analysis from meta if available
    meta = inbound_email.meta or {}
    if meta.get("sentiment") or meta.get("intent"):
        inbound_analysis += f"""
AI analysis of email:
- Sentiment: {meta.get('sentiment', 'unknown')}
- Intent: {meta.get('intent', 'unknown')}
- Summary: {meta.get('summary', '')}
- Key points: {', '.join(meta.get('key_points', []))}
- Suggested next action: {meta.get('next_action', '')}
"""

    # Tone guidance
    tone_guidance = {
        "professional": "Professional and courteous. Use formal but warm business language.",
        "friendly": "Friendly and approachable. Like talking to an acquaintance.",
        "assertive": "Assertive and direct. Get to the point with confidence.",
        "consultative": "Consultative. Ask questions, offer value, don't sell directly.",
    }.get(tone, "Professional and courteous. Use formal but warm business language.")

    length_guidance = {
        "short": "Max 3-4 sentences. Brief and direct.",
        "medium": "Max 2-3 short paragraphs. Balanced.",
        "long": "3-4 paragraphs with detail. Include examples or next-step proposal.",
    }.get(max_length, "Max 2-3 short paragraphs. Balanced.")

    custom = f"\nAdditional instructions: {custom_instructions}\n" if custom_instructions else ""

    system_prompt = f"""You are a B2B sales expert and commercial communication specialist. You generate replies to prospect emails that are:

1. HIGHLY PERSONALIZED: Use the business name, references to their industry/city, and context from previous conversations.
2. CONTEXTUAL: Respond DIRECTLY to what the prospect said. Not generic.
3. APPROPRIATE TONE: {tone_guidance}
4. APPROPRIATE LENGTH: {length_guidance}
5. CLEAR CTA: Always end with a question or concrete next-step suggestion.
6. LANGUAGE: The prospect wrote in English. You MUST reply in English ONLY. Do not use Spanish, Portuguese, or any other language.

RULES:
- Never use "I hope this email finds you well" or generic openers.
- Mention something specific about the lead's business if you have information.
- If the lead shows interest, suggest a meeting or demo.
- If the lead has objections, address them with data or examples.
- If the lead asks for information, provide it concisely.
- Sign as "Eko AI Team" or similar professional signature.
- IMPORTANT: If you suggest a meeting, call, or demo, you MUST include BOTH of these options:
  (a) This booking link so the lead can schedule directly: {booking_link}
  (b) This phone number they can call anytime — our AI assistant answers 24/7: {phone_number}
  Present them as friendly buttons or links within the email body.

Respond ONLY with a valid JSON with this structure:
{{"subject": "...", "body": "...", "tone": "...", "confidence": 0.0-1.0, "suggested_next_action": "..."}}"""

    user_prompt = f"""Generate a reply to the following prospect email:

{lead_context}

{inbound_analysis}

Conversation history:{history_text or ' (No previous history)'}

{custom}

Generate the reply now."""

    try:
        response = await generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=2000,
        )

        # Parse JSON response
        text = response.strip()

        # Remove markdown code fences if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        result = json.loads(text)
        body = result.get("body", "")

        # Post-process: inject CTA with both phone + link if meeting was suggested
        body, suggested_meeting = _inject_booking_cta(body, booking_link, phone_number)

        return {
            "subject": result.get("subject", f"Re: {inbound_email.subject or ''}"),
            "body": body,
            "tone": result.get("tone", tone),
            "confidence": float(result.get("confidence", 0.8)),
            "suggested_next_action": result.get("suggested_next_action", ""),
            "suggested_meeting": suggested_meeting,
            "booking_link": booking_link if suggested_meeting else None,
        }
    except Exception as e:
        # Fallback reply — still respects tone and length
        length_text = {
            "short": "Could you confirm your availability for a quick call?",
            "medium": "Could you confirm the best time for a quick 15-minute call? We'd love to understand your needs better.",
            "long": "Could you confirm the best time for a quick 15-minute call? We'd love to understand your needs better and explore how we can help you reach your goals.",
        }.get(max_length, "Could you confirm the best time for a quick 15-minute call? We'd love to understand your needs better.")

        tone_opener = {
            "professional": f"Dear {lead.business_name},",
            "friendly": f"Hi {lead.business_name},",
            "assertive": f"Hi {lead.business_name},",
            "consultative": f"Hi {lead.business_name},",
        }.get(tone, f"Hi {lead.business_name},")

        tone_body = {
            "professional": "Thank you for your message. We've received your email and want to make sure we give you the best possible response.",
            "friendly": "Thanks for reaching out! We received your email and want to get back to you with the best answer.",
            "assertive": "Thanks for your email. We want to move fast and get you the information you need.",
            "consultative": "Thank you for your message. I'd like to understand your situation better so I can guide you in the best way.",
        }.get(tone, "Thank you for your message. We've received your email and want to make sure we give you the best possible response.")

        custom_str = f"\n{custom_instructions}\n" if custom_instructions else ""

        body_parts = [tone_opener, "", tone_body, custom_str, length_text, "", "Best,", "Eko AI Team"]
        body = "\n".join(p for p in body_parts if p)

        # Inject CTA in fallback too
        body, suggested_meeting = _inject_booking_cta(body, booking_link, phone_number)

        return {
            "subject": f"Re: {inbound_email.subject or ''}",
            "body": body,
            "tone": tone,
            "confidence": 0.5,
            "suggested_next_action": "Schedule follow-up call",
            "suggested_meeting": suggested_meeting,
            "booking_link": booking_link if suggested_meeting else None,
        }


async def get_conversation_history(
    lead_id: int,
    db,
    limit: int = 10,
) -> List[Interaction]:
    """Get recent email interactions for a lead."""
    from sqlalchemy import select, asc
    from app.models.lead import Interaction

    result = await db.execute(
        select(Interaction)
        .where(Interaction.lead_id == lead_id)
        .where(Interaction.interaction_type == "email")
        .order_by(asc(Interaction.created_at))
        .limit(limit)
    )
    return result.scalars().all()
