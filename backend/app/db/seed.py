"""Seed data for Eko AI — creates default nurture sequence on startup."""

import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sequence import EmailSequence, SequenceStep, SequenceStatus, SequenceStepType

logger = logging.getLogger(__name__)

NURTURE_SEQUENCE_NAME = "Landing Page Nurturing"

# 9-step nurture sequence for leads captured from the public website.
# Pattern: EMAIL → WAIT 24h → EMAIL → WAIT 24h → ...
# The scheduler (hourly) will send the first email within 1 hour of enrollment,
# then wait ~24h between each subsequent email.
NURTURE_STEPS = [
    {
        "position": 0,
        "step_type": SequenceStepType.EMAIL,
        "name": "Bienvenida + análisis gratuito",
        "template_key": "nurture_welcome",
        "ai_generate": True,
        "delay_hours": 0,
    },
    {
        "position": 1,
        "step_type": SequenceStepType.WAIT,
        "name": "Wait 24 hours",
        "delay_hours": 24,
        "ai_generate": False,
    },
    {
        "position": 2,
        "step_type": SequenceStepType.EMAIL,
        "name": "Social proof — ahorro de tiempo",
        "template_key": "nurture_social_proof",
        "ai_generate": True,
        "delay_hours": 0,
    },
    {
        "position": 3,
        "step_type": SequenceStepType.WAIT,
        "name": "Wait 24 hours",
        "delay_hours": 24,
        "ai_generate": False,
    },
    {
        "position": 4,
        "step_type": SequenceStepType.EMAIL,
        "name": "Educación — 3 señales de que necesitan IA",
        "template_key": "nurture_education",
        "ai_generate": True,
        "delay_hours": 0,
    },
    {
        "position": 5,
        "step_type": SequenceStepType.WAIT,
        "name": "Wait 24 hours",
        "delay_hours": 24,
        "ai_generate": False,
    },
    {
        "position": 6,
        "step_type": SequenceStepType.EMAIL,
        "name": "Oferta de demo gratuita",
        "template_key": "nurture_demo_offer",
        "ai_generate": True,
        "delay_hours": 0,
    },
    {
        "position": 7,
        "step_type": SequenceStepType.WAIT,
        "name": "Wait 24 hours",
        "delay_hours": 24,
        "ai_generate": False,
    },
    {
        "position": 8,
        "step_type": SequenceStepType.EMAIL,
        "name": "Urgencia — setup gratuito",
        "template_key": "nurture_urgency",
        "ai_generate": True,
        "delay_hours": 0,
    },
]


async def seed_nurture_sequence(db: AsyncSession):
    """Create or update the default landing-page nurture sequence."""
    result = await db.execute(
        select(EmailSequence).where(EmailSequence.name == NURTURE_SEQUENCE_NAME)
    )
    existing = result.scalar_one_or_none()

    if existing:
        # Check if steps count matches — if not, rebuild steps
        steps_result = await db.execute(
            select(SequenceStep).where(SequenceStep.sequence_id == existing.id)
        )
        current_steps = steps_result.scalars().all()
        if len(current_steps) == len(NURTURE_STEPS):
            logger.info(f"Nurture sequence '{NURTURE_SEQUENCE_NAME}' already exists with correct steps (id={existing.id})")
            return existing

        # Rebuild steps (keep enrollments intact)
        logger.warning(f"Rebuilding steps for nurture sequence '{NURTURE_SEQUENCE_NAME}' (id={existing.id})")
        await db.execute(delete(SequenceStep).where(SequenceStep.sequence_id == existing.id))
        for step_data in NURTURE_STEPS:
            step = SequenceStep(sequence_id=existing.id, **step_data)
            db.add(step)
        await db.commit()
        return existing

    seq = EmailSequence(
        name=NURTURE_SEQUENCE_NAME,
        description="Automated email sequence for leads captured from the public website. 5 value-first emails over 4 days.",
        status=SequenceStatus.ACTIVE,
        entry_criteria={"source": "website_landing"},
    )
    db.add(seq)
    await db.flush()  # Get seq.id

    for step_data in NURTURE_STEPS:
        step = SequenceStep(sequence_id=seq.id, **step_data)
        db.add(step)

    await db.commit()
    await db.refresh(seq)
    logger.info(f"Created nurture sequence '{NURTURE_SEQUENCE_NAME}' (id={seq.id}) with {len(NURTURE_STEPS)} steps")
    return seq
