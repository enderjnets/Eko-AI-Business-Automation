from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.lead import Lead, Interaction

router = APIRouter()


@router.post("/resend")
async def resend_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Resend webhooks for email events."""
    payload = await request.json()
    event_type = payload.get("type")
    data = payload.get("data", {})
    
    message_id = data.get("email_id")
    to_email = data.get("to", [None])[0] if isinstance(data.get("to"), list) else data.get("to")
    
    # Find lead by email
    if to_email:
        result = await db.execute(select(Lead).where(Lead.email == to_email))
        lead = result.scalar_one_or_none()
        
        if lead and event_type == "email.opened":
            lead.email_opened_count += 1
        elif lead and event_type == "email.clicked":
            lead.email_clicked_count += 1
        
        # Record interaction
        if lead:
            interaction = Interaction(
                lead_id=lead.id,
                interaction_type="email",
                direction="inbound" if event_type in ["email.opened", "email.clicked"] else "outbound",
                email_status=event_type.replace("email.", ""),
                email_message_id=message_id,
                metadata=payload,
            )
            db.add(interaction)
            await db.commit()
    
    return {"status": "ok"}


@router.post("/calcom")
async def calcom_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Cal.com webhooks for booking events."""
    payload = await request.json()
    event_type = payload.get("triggerEvent")
    
    # Extract attendee email
    attendees = payload.get("payload", {}).get("attendees", [])
    attendee_email = attendees[0].get("email") if attendees else None
    
    if attendee_email:
        result = await db.execute(select(Lead).where(Lead.email == attendee_email))
        lead = result.scalar_one_or_none()
        
        if lead:
            interaction = Interaction(
                lead_id=lead.id,
                interaction_type="meeting",
                direction="inbound",
                subject=f"Meeting {event_type}",
                metadata=payload,
            )
            db.add(interaction)
            
            if event_type == "BOOKING_CREATED":
                lead.status = "meeting_booked"
            
            await db.commit()
    
    return {"status": "ok"}
