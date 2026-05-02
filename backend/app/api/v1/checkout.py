"""Stripe Checkout integration for Eko AI."""

import logging
from typing import Optional
from datetime import datetime

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.lead import Lead
from app.models.payment import Payment, PaymentStatus
from app.models.deal import Deal, DealStatus
from app.config import get_settings

settings = get_settings()
router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

PLAN_PRICES = {
    "starter": {"monthly_cents": 19900, "setup_cents": 49900, "name": "Eko AI Starter"},
    "growth": {"monthly_cents": 29900, "setup_cents": 49900, "name": "Eko AI Growth"},
    "enterprise": {"monthly_cents": 39900, "setup_cents": 49900, "name": "Eko AI Enterprise"},
}


class CheckoutSessionRequest(BaseModel):
    lead_id: int
    plan: str  # starter, growth, enterprise
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str


@router.post("/session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a Stripe Checkout Session for a lead to pay setup + first month."""
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    plan = PLAN_PRICES.get(request.plan)
    if not plan:
        raise HTTPException(status_code=400, detail=f"Invalid plan: {request.plan}")

    # Get lead
    result = await db.execute(select(Lead).where(Lead.id == request.lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if not lead.email:
        raise HTTPException(status_code=400, detail="Lead has no email")

    total_cents = plan["monthly_cents"] + plan["setup_cents"]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": plan["name"]},
                        "unit_amount": plan["monthly_cents"],
                    },
                    "quantity": 1,
                },
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Setup Fee"},
                        "unit_amount": plan["setup_cents"],
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            customer_email=lead.email,
            success_url=request.success_url or f"{settings.FRONTEND_URL}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=request.cancel_url or f"{settings.FRONTEND_URL}/checkout/cancel",
            metadata={
                "lead_id": str(lead.id),
                "plan": request.plan,
                "business_name": lead.business_name or "",
            },
        )

        # Record payment intent
        payment = Payment(
            lead_id=lead.id,
            stripe_checkout_session_id=session.id,
            amount_cents=total_cents,
            currency="usd",
            plan_name=request.plan,
            status=PaymentStatus.PENDING,
            meta={
                "plan_name": plan["name"],
                "monthly_cents": plan["monthly_cents"],
                "setup_cents": plan["setup_cents"],
            },
        )
        db.add(payment)
        await db.commit()

        return CheckoutSessionResponse(checkout_url=session.url, session_id=session.id)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_checkout_session(session_id: str):
    """Retrieve a Stripe Checkout Session status."""
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "id": session.id,
            "status": session.status,
            "payment_status": session.payment_status,
            "amount_total": session.amount_total,
            "customer_email": session.customer_email,
            "metadata": session.metadata,
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=404, detail=str(e))
