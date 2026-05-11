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


def _inject_booking_cta(body: str, booking_link: str, phone_number: str, language: str = "en") -> tuple[str, bool]:
    """
    Post-process the AI body. If it suggests a meeting but doesn't contain
    the booking link or phone number, inject a styled CTA with both options.

    Returns (body, suggested_meeting).
    """
    # Check if body already contains the link
    if booking_link in body and phone_number in body:
        return body, True

    # Localized meeting keywords and CTA text
    _cta_translations = {
        "en": {
            "keywords": ["call", "demo", "schedule", "calendar", "appointment", "meeting", "zoom", "google meet", "teams", "chat", "talk", "speak", "connect", "15 minutes", "15 min"],
            "heading": "Ready to see it in action?",
            "call_btn": f"📞 Call {phone_number}",
            "book_btn": "Book Online →",
            "footer": "Our AI assistant answers calls 24/7 and can book your demo instantly.",
        },
        "es": {
            "keywords": ["llamada", "demo", "demostración", "agendar", "calendario", "cita", "reunión", "zoom", "google meet", "teams", "charlar", "hablar", "conectar", "15 minutos", "15 min"],
            "heading": "¿Listo para verlo en acción?",
            "call_btn": f"📞 Llamar al {phone_number}",
            "book_btn": "Agendar en línea →",
            "footer": "Nuestro asistente de IA responde llamadas 24/7 y puede agendar tu demo al instante.",
        },
        "pt": {
            "keywords": ["ligação", "demo", "demonstração", "agendar", "calendário", "consulta", "reunião", "zoom", "google meet", "teams", "conversar", "falar", "conectar", "15 minutos", "15 min"],
            "heading": "Pronto para ver em ação?",
            "call_btn": f"📞 Ligar para {phone_number}",
            "book_btn": "Agendar online →",
            "footer": "Nosso assistente de IA atende chamadas 24/7 e pode agendar sua demo instantaneamente.",
        },
        "fr": {
            "keywords": ["appel", "démo", "démonstration", "planifier", "calendrier", "rendez-vous", "réunion", "zoom", "google meet", "teams", "discuter", "parler", "connecter", "15 minutes", "15 min"],
            "heading": "Prêt à voir ça en action?",
            "call_btn": f"📞 Appeler {phone_number}",
            "book_btn": "Réserver en ligne →",
            "footer": "Notre assistant IA répond aux appels 24/7 et peut réserver votre démo instantanément.",
        },
        "de": {
            "keywords": ["anruf", "demo", "demonstration", "termin", "kalender", "besprechung", "meeting", "zoom", "google meet", "teams", "sprechen", "reden", "verbinden", "15 minuten", "15 min"],
            "heading": "Bereit, es in Aktion zu sehen?",
            "call_btn": f"📞 Anrufen {phone_number}",
            "book_btn": "Online buchen →",
            "footer": "Unser KI-Assistent beantwortet Anrufe rund um die Uhr und kann Ihre Demo sofort buchen.",
        },
        "it": {
            "keywords": ["chiamata", "demo", "dimostrazione", "pianificare", "calendario", "appuntamento", "riunione", "zoom", "google meet", "teams", "parlare", "discutere", "connettere", "15 minuti", "15 min"],
            "heading": "Pronto a vederlo in azione?",
            "call_btn": f"📞 Chiama {phone_number}",
            "book_btn": "Prenota online →",
            "footer": "Il nostro assistente AI risponde alle chiamate 24/7 e può prenotare la tua demo all'istante.",
        },
    }
    lang = language.lower()[:2] if language else "en"
    t = _cta_translations.get(lang, _cta_translations["en"])

    lower_body = body.lower()
    has_meeting_intent = any(kw in lower_body for kw in t["keywords"])

    if not has_meeting_intent:
        return body, False

    # Inject styled HTML CTA with localized text
    cta = f"""
<div style="margin-top:24px;padding:20px;background:#0F172A;border-radius:10px;border:1px solid rgba(255,255,255,0.08);">
  <p style="margin:0 0 12px;font-size:14px;font-weight:600;color:#E2E8F0;">{t['heading']}</p>
  <table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td width="50%" style="padding-right:6px;">
        <a href="tel:{phone_number}" style="display:block;background:linear-gradient(135deg,#0B4FD8,#7C3AED);color:#fff;text-decoration:none;padding:12px 0;border-radius:8px;font-size:14px;font-weight:600;text-align:center;">{t['call_btn']}</a>
      </td>
      <td width="50%" style="padding-left:6px;">
        <a href="{booking_link}" style="display:block;background:transparent;color:#fff;text-decoration:none;padding:12px 0;border-radius:8px;font-size:14px;font-weight:600;text-align:center;border:2px solid rgba(255,255,255,0.15);">{t['book_btn']}</a>
      </td>
    </tr>
  </table>
  <p style="margin:10px 0 0;font-size:12px;color:#64748B;">{t['footer']}</p>
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
    language: Optional[str] = None,
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

    # Determine language: prioritize passed param, then meta, then lead, then auto-detect
    meta = inbound_email.meta or {}
    detected_lang = meta.get("detected_language")
    language = (language or detected_lang or lead.language or "en").lower().strip()
    # Ensure we only use 2-letter codes
    language = language[:2]

    lang_names = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "pt": "Portuguese", "it": "Italian"}
    lang_name = lang_names.get(language, language)

    system_prompt = f"""You are a B2B sales expert and commercial communication specialist. You generate replies to prospect emails that are:

1. HIGHLY PERSONALIZED: Use the business name, references to their industry/city, and context from previous conversations.
2. CONTEXTUAL: Respond DIRECTLY to what the prospect said. Not generic.
3. APPROPRIATE TONE: {tone_guidance}
4. APPROPRIATE LENGTH: {length_guidance}
5. CLEAR CTA: Always end with a question or concrete next-step suggestion.
6. LANGUAGE — CRITICAL: The prospect wrote in {lang_name}. You MUST write the ENTIRE reply in {lang_name} ONLY. Under no circumstances should you use Chinese, English, or any other language. Every single word, including the CTA buttons and footer, must be in {lang_name}.

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
        body, suggested_meeting = _inject_booking_cta(body, booking_link, phone_number, language=language)

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
        # Fallback reply — fully localized
        _fb = {
            "en": {
                "short": "Could you confirm your availability for a quick call?",
                "medium": "Could you confirm the best time for a quick 15-minute call? We'd love to understand your needs better.",
                "long": "Could you confirm the best time for a quick 15-minute call? We'd love to understand your needs better and explore how we can help you reach your goals.",
                "professional": "Thank you for your message. We've received your email and want to make sure we give you the best possible response.",
                "friendly": "Thanks for reaching out! We received your email and want to get back to you with the best answer.",
                "assertive": "Thanks for your email. We want to move fast and get you the information you need.",
                "consultative": "Thank you for your message. I'd like to understand your situation better so I can guide you in the best way.",
                "signoff": "Best,",
                "team": "Eko AI Team",
            },
            "es": {
                "short": "¿Podrías confirmar tu disponibilidad para una llamada rápida?",
                "medium": "¿Podrías confirmar el mejor horario para una llamada rápida de 15 minutos? Nos encantaría entender mejor tus necesidades.",
                "long": "¿Podrías confirmar el mejor horario para una llamada rápida de 15 minutos? Nos encantaría entender mejor tus necesidades y explorar cómo podemos ayudarte a alcanzar tus objetivos.",
                "professional": "Gracias por tu mensaje. Hemos recibido tu correo y queremos asegurarnos de darte la mejor respuesta posible.",
                "friendly": "¡Gracias por contactarnos! Recibimos tu correo y queremos responderte con la mejor respuesta.",
                "assertive": "Gracias por tu correo. Queremos actuar rápido y darte la información que necesitas.",
                "consultative": "Gracias por tu mensaje. Me gustaría entender mejor tu situación para poder orientarte de la mejor manera.",
                "signoff": "Saludos,",
                "team": "Equipo de Eko AI",
            },
            "pt": {
                "short": "Você poderia confirmar sua disponibilidade para uma ligação rápida?",
                "medium": "Você poderia confirmar o melhor horário para uma ligação rápida de 15 minutos? Adoraríamos entender melhor suas necessidades.",
                "long": "Você poderia confirmar o melhor horário para uma ligação rápida de 15 minutos? Adoraríamos entender melhor suas necessidades e explorar como podemos ajudá-lo a alcançar seus objetivos.",
                "professional": "Obrigado pela sua mensagem. Recebemos seu e-mail e queremos garantir que você receba a melhor resposta possível.",
                "friendly": "Obrigado por entrar em contato! Recebemos seu e-mail e queremos responder com a melhor resposta.",
                "assertive": "Obrigado pelo seu e-mail. Queremos agir rápido e fornecer as informações que você precisa.",
                "consultative": "Obrigado pela sua mensagem. Gostaria de entender melhor sua situação para poder orientá-lo da melhor maneira.",
                "signoff": "Atenciosamente,",
                "team": "Equipe Eko AI",
            },
            "fr": {
                "short": "Pourriez-vous confirmer votre disponibilité pour un appel rapide?",
                "medium": "Pourriez-vous confirmer le meilleur moment pour un appel rapide de 15 minutes? Nous aimerions mieux comprendre vos besoins.",
                "long": "Pourriez-vous confirmer le meilleur moment pour un appel rapide de 15 minutes? Nous aimerions mieux comprendre vos besoins et explorer comment nous pouvons vous aider à atteindre vos objectifs.",
                "professional": "Merci pour votre message. Nous avons reçu votre e-mail et voulons nous assurer de vous donner la meilleure réponse possible.",
                "friendly": "Merci de nous avoir contactés! Nous avons reçu votre e-mail et voulons vous répondre avec la meilleure réponse.",
                "assertive": "Merci pour votre e-mail. Nous voulons agir rapidement et vous donner les informations dont vous avez besoin.",
                "consultative": "Merci pour votre message. J'aimerais mieux comprendre votre situation pour pouvoir vous orienter de la meilleure manière.",
                "signoff": "Cordialement,",
                "team": "L'équipe Eko AI",
            },
            "de": {
                "short": "Könnten Sie Ihre Verfügbarkeit für einen kurzen Anruf bestätigen?",
                "medium": "Könnten Sie den besten Zeitpunkt für einen kurzen 15-minütigen Anruf bestätigen? Wir würden Ihre Bedürfnisse gerne besser verstehen.",
                "long": "Könnten Sie den besten Zeitpunkt für einen kurzen 15-minütigen Anruf bestätigen? Wir würden Ihre Bedürfnisse gerne besser verstehen und erkunden, wie wir Ihnen helfen können, Ihre Ziele zu erreichen.",
                "professional": "Vielen Dank für Ihre Nachricht. Wir haben Ihre E-Mail erhalten und möchten sicherstellen, dass wir Ihnen die bestmögliche Antwort geben.",
                "friendly": "Danke, dass Sie sich bei uns gemeldet haben! Wir haben Ihre E-Mail erhalten und möchten Ihnen die beste Antwort geben.",
                "assertive": "Danke für Ihre E-Mail. Wir wollen schnell handeln und Ihnen die Informationen geben, die Sie brauchen.",
                "consultative": "Vielen Dank für Ihre Nachricht. Ich möchte Ihre Situation besser verstehen, um Sie auf die beste Weise beraten zu können.",
                "signoff": "Mit freundlichen Grüßen,",
                "team": "Das Eko AI Team",
            },
            "it": {
                "short": "Potresti confermare la tua disponibilità per una chiamata rapida?",
                "medium": "Potresti confermare il momento migliore per una chiamata rapida di 15 minuti? Ci piacerebbe capire meglio le tue esigenze.",
                "long": "Potresti confermare il momento migliore per una chiamata rapida di 15 minuti? Ci piacerebbe capire meglio le tue esigenze ed esplorare come possiamo aiutarti a raggiungere i tuoi obiettivi.",
                "professional": "Grazie per il tuo messaggio. Abbiamo ricevuto la tua email e vogliamo assicurarci di darti la migliore risposta possibile.",
                "friendly": "Grazie per averci contattato! Abbiamo ricevuto la tua email e vogliamo risponderti con la migliore risposta.",
                "assertive": "Grazie per la tua email. Vogliamo agire rapidamente e fornirti le informazioni di cui hai bisogno.",
                "consultative": "Grazie per il tuo messaggio. Mi piacerebbe capire meglio la tua situazione per poterti orientare nel migliore dei modi.",
                "signoff": "Cordiali saluti,",
                "team": "Il team di Eko AI",
            },
        }
        lang = language[:2] if language else "en"
        fb = _fb.get(lang, _fb["en"])

        length_text = {
            "short": fb["short"],
            "medium": fb["medium"],
            "long": fb["long"],
        }.get(max_length, fb["medium"])

        tone_opener = f"Hi {lead.business_name},"
        if lang == "es":
            tone_opener = f"Hola {lead.business_name},"
        elif lang == "pt":
            tone_opener = f"Olá {lead.business_name},"
        elif lang == "fr":
            tone_opener = f"Bonjour {lead.business_name},"
        elif lang == "de":
            tone_opener = f"Hallo {lead.business_name},"
        elif lang == "it":
            tone_opener = f"Ciao {lead.business_name},"

        tone_body = fb.get(tone, fb["professional"])

        custom_str = f"\n{custom_instructions}\n" if custom_instructions else ""

        body_parts = [tone_opener, "", tone_body, custom_str, length_text, "", fb["signoff"], fb["team"]]
        body = "\n".join(p for p in body_parts if p)

        # Inject localized CTA in fallback too
        body, suggested_meeting = _inject_booking_cta(body, booking_link, phone_number, language=lang)

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
