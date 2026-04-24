"""Lead embedding utilities for semantic search."""

import logging
from typing import Optional

from app.models.lead import Lead
from app.utils.ai_client import generate_embedding

logger = logging.getLogger(__name__)


def _build_lead_text(lead: Lead) -> str:
    """Build a text representation of a lead for embedding generation."""
    parts = [f"Business: {lead.business_name}"]
    if lead.category:
        parts.append(f"Category: {lead.category}")
    if lead.city:
        parts.append(f"Location: {lead.city}, {lead.state or ''}")
    if lead.description:
        parts.append(f"Description: {lead.description}")
    if lead.pain_points:
        parts.append(f"Pain points: {', '.join(lead.pain_points)}")
    return "\n".join(parts)


async def update_lead_embedding(lead: Lead) -> Optional[list]:
    """Generate and assign an embedding vector to a lead."""
    try:
        text = _build_lead_text(lead)
        embedding = await generate_embedding(text)
        lead.embedding = embedding
        logger.debug(f"Generated embedding for lead {lead.id}")
        return embedding
    except Exception as e:
        logger.warning(f"Failed to generate embedding for lead {lead.id}: {e}")
        return None
