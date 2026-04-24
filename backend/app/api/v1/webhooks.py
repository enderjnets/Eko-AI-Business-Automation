from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.lead import Lead, Interaction
from app.models.campaign import Campaign

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
        
        if lead:
            # Update engagement stats
            if event_type == "email.opened":
                lead.email_opened_count += 1
            elif event_type == "email.clicked":
                lead.email_clicked_count += 1
                # If clicked pricing page or booking link, upgrade status
                if lead.status.value == "contacted":
                    lead.status = "engaged"
            
            # Record interaction
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
                from app.models.lead import LeadStatus
                lead.status = LeadStatus.MEETING_BOOKED
            
            await db.commit()
    
    return {"status": "ok"}


@router.get("/unsubscribe")
async def unsubscribe_lead(
    lead_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Unsubscribe a lead from emails (CAN-SPAM compliance)."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    
    if lead:
        lead.do_not_contact = True
        lead.consent_status = "opted_out"
        
        interaction = Interaction(
            lead_id=lead.id,
            interaction_type="email",
            direction="inbound",
            subject="Unsubscribe request",
            content="Lead opted out via unsubscribe link",
        )
        db.add(interaction)
        await db.commit()
        
        return {
            "status": "unsubscribed",
            "message": "You have been unsubscribed from future communications.",
        }
    
    return {"status": "error", "message": "Lead not found"}


@router.get("/track/open")
async def track_email_open(
    lead_id: int = Query(...),
    message_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Track email open via tracking pixel."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    
    if lead:
        lead.email_opened_count += 1
        
        interaction = Interaction(
            lead_id=lead.id,
            interaction_type="email",
            direction="inbound",
            email_status="opened",
            email_message_id=message_id,
        )
        db.add(interaction)
        await db.commit()
    
    # Return 1x1 transparent pixel
    from fastapi.responses import Response
    return Response(
        content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b",
        media_type="image/gif",
    )
