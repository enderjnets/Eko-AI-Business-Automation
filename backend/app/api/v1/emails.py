from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.lead import Lead
from app.agents.outreach.channels.email import EmailOutreach

router = APIRouter()


@router.post("/{lead_id}/send")
async def send_email_to_lead(
    lead_id: int,
    subject: str,
    body: str,
    db: AsyncSession = Depends(get_db),
):
    """Send a personalized email to a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if not lead.email:
        raise HTTPException(status_code=400, detail="Lead has no email address")
    
    if lead.do_not_contact:
        raise HTTPException(status_code=400, detail="Lead is marked as do-not-contact")
    
    email_outreach = EmailOutreach()
    response = await email_outreach.send(
        to_email=lead.email,
        subject=subject,
        body=body,
        lead_id=lead_id,
    )
    
    return {"status": "sent", "message_id": response.get("id")}


@router.post("/{lead_id}/generate-and-send")
async def generate_and_send_email(
    lead_id: int,
    campaign_context: str = "",
    db: AsyncSession = Depends(get_db),
):
    """Generate a personalized email using AI and send it."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if not lead.email:
        raise HTTPException(status_code=400, detail="Lead has no email address")
    
    email_outreach = EmailOutreach()
    response = await email_outreach.generate_and_send(
        lead=lead,
        campaign_context=campaign_context,
    )
    
    return {"status": "sent", "message_id": response.get("id")}
