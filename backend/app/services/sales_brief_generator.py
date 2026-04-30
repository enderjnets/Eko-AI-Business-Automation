from typing import Optional
from app.utils.ai_client import generate_completion
from app.models.lead import Lead


async def generate_sales_brief(lead: Lead, booking_context: Optional[dict] = None) -> str:
    """
    Generate an AI-powered sales brief for a booked meeting.

    Returns a markdown-formatted string with:
    - Lead snapshot
    - Detected needs
    - Likely objections + counters
    - Closing tips
    """

    lead_data = f"""Lead Data:
- Business: {lead.business_name}
- Category: {lead.category or 'N/A'}
- City: {lead.city or 'N/A'}
- Description: {lead.description or 'N/A'}
- Services: {', '.join(lead.services or []) or 'N/A'}
- Pain points: {', '.join(lead.pain_points or []) or 'N/A'}
- Review summary: {lead.review_summary or 'N/A'}
- Scoring reason: {lead.scoring_reason or 'N/A'}
- Proposal suggestion: {lead.proposal_suggestion or 'N/A'}
- Total score: {lead.total_score or 0}/100
- Urgency: {lead.urgency_score or 0}/100
- Fit: {lead.fit_score or 0}/100
"""

    booking_data = ""
    if booking_context:
        booking_data = f"""Booking Context:
- Title: {booking_context.get('title', 'N/A')}
- Start: {booking_context.get('start_time', 'N/A')}
- Location: {booking_context.get('location', 'N/A')}
"""

    system_prompt = """You are an elite sales strategist preparing a rep for a discovery call.
Given lead enrichment data, produce a concise, actionable sales brief in Markdown.

Structure (in Spanish, unless lead context is clearly in English):

## 🎯 Snapshot
2-3 sentences: who they are, what they do, their market position.

## 🔍 Detected Needs
Top 2-3 needs or pain points derived from the data. Be specific.

## 🛡️ Likely Objections & Counters
1-2 objections they may raise + how to counter them with data or positioning.

## 🏁 Closing Tips
Concrete angle to close this specific lead. Mention what to emphasize (ROI, speed, automation, etc.) and any trigger event to leverage.

Rules:
- Be concise. No filler.
- Use the lead's actual data; don't hallucinate.
- If data is sparse, say so and focus on discovery questions."""

    user_prompt = f"""{lead_data}

{booking_data}

Generate the sales brief now."""

    try:
        response = await generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=1500,
        )
        return response.strip()
    except Exception as e:
        # Fallback: static summary from available data
        parts = [f"## 🎯 Snapshot\n\n{lead.business_name} — {lead.category or 'Negocio local'} en {lead.city or 'N/A'}."]
        if lead.description:
            parts.append(f"{lead.description[:200]}")
        parts.append("\n## 🔍 Detected Needs\n")
        if lead.pain_points:
            for pp in lead.pain_points[:3]:
                parts.append(f"- {pp}")
        else:
            parts.append("- No pain points identified yet. Focus on discovery.")
        parts.append("\n## 🛡️ Likely Objections & Counters\n")
        parts.append("- Budget: Emphasize ROI and automation savings.")
        parts.append("- Timing: Offer quick wins and low-friction onboarding.")
        parts.append("\n## 🏁 Closing Tips\n")
        if lead.proposal_suggestion:
            parts.append(f"- {lead.proposal_suggestion}")
        else:
            parts.append("- Focus on understanding their current workflow and showing a quick automation win.")
        return "\n".join(parts)
