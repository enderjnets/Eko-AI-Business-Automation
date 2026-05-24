"""Stripe Checkout integration for Eko AI subscriptions."""

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
from app.models.payment import Payment, PaymentStatus, PaymentType
from app.models.deal import Deal, DealStatus
from app.config import get_settings

settings = get_settings()
router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Legacy map kept for backwards-compat (callers that pass only `plan` without billing_cycle/vertical).
STRIPE_PLAN_PRICE_MAP = {
    "starter": settings.STRIPE_PRICE_STARTER,
    "growth": settings.STRIPE_PRICE_GROWTH,
    "enterprise": settings.STRIPE_PRICE_ENTERPRISE,
}

PLAN_NAMES = {
    "starter": "Eko AI Starter",
    "growth": "Eko AI Growth",
    "growth_accounting": "Eko AI Growth — Contable",
    "growth_realestate": "Eko AI Growth — Inmobiliario",
    "growth_legalhealth": "Eko AI Growth — Legal / Clínico",
    "enterprise": "Eko AI Enterprise",
}

# Setup fee removed for pricing v2 (became an add-on "On-premise setup $1,500"). Constant kept
# at zero so any historical reference does not crash; the line item is not appended anymore.
SETUP_FEE_CENTS = 0

# Valid pricing v2 inputs
VALID_BILLING_CYCLES = ("monthly", "annual")
VALID_GROWTH_VERTICALS = ("accounting", "realestate", "legalhealth")


def _resolve_price_id(plan: str, billing_cycle: str, vertical: str | None) -> tuple[str | None, str]:
    """Resolve a Stripe price ID for the given (plan, billing_cycle, vertical).

    Returns (price_id, normalized_plan_key). Falls back to legacy STRIPE_PRICE_* if v2 env vars
    are not configured. Returns (None, key) when no price is available so the caller can 503 cleanly.
    """
    key = plan
    if plan == "growth" and vertical:
        key = f"growth_{vertical}"

    # v2 lookup (monthly/annual variant)
    attr = f"STRIPE_PRICE_{key.upper()}_{billing_cycle.upper()}"
    v2 = getattr(settings, attr, "") or ""
    if v2:
        return v2, key

    # Fallback to legacy single-price map (no cycle/vertical distinction)
    legacy_key = "growth" if plan == "growth" else plan
    legacy = STRIPE_PLAN_PRICE_MAP.get(legacy_key, "") or ""
    if legacy:
        return legacy, legacy_key

    return None, key


class CheckoutSessionRequest(BaseModel):
    lead_id: int
    plan: str  # starter, growth, enterprise
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None
    # Pricing v2 (optional, defaults preserve legacy behaviour for older callers)
    billing_cycle: Optional[str] = None  # "monthly" | "annual" — defaults to monthly
    vertical: Optional[str] = None  # required for plan="growth" under v2: accounting | realestate | legalhealth


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str


class PortalSessionRequest(BaseModel):
    lead_id: int
    return_url: Optional[str] = None


class PortalSessionResponse(BaseModel):
    portal_url: str


@router.post("/session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a Stripe Checkout Session for subscription.

    Pricing v2: setup fee removed (became an add-on). billing_cycle + vertical are optional;
    when omitted, falls back to legacy single-price map for backwards-compat with old callers.
    """
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    billing_cycle = (request.billing_cycle or "monthly").lower()
    if billing_cycle not in VALID_BILLING_CYCLES:
        raise HTTPException(status_code=400, detail=f"Invalid billing_cycle: {billing_cycle}")

    vertical = (request.vertical or None)
    if vertical is not None and vertical not in VALID_GROWTH_VERTICALS:
        raise HTTPException(status_code=400, detail=f"Invalid vertical: {vertical}")

    price_id, plan_key = _resolve_price_id(request.plan, billing_cycle, vertical)
    if not price_id:
        raise HTTPException(
            status_code=503,
            detail=(
                f"Stripe price not configured for plan='{request.plan}' "
                f"billing_cycle='{billing_cycle}' vertical='{vertical}'. "
                f"Set STRIPE_PRICE_{plan_key.upper()}_{billing_cycle.upper()} or the legacy "
                f"STRIPE_PRICE_{request.plan.upper()} env var."
            ),
        )

    # Get lead
    result = await db.execute(select(Lead).where(Lead.id == request.lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if not lead.email:
        raise HTTPException(status_code=400, detail="Lead has no email")

    # Find or create Stripe Customer
    customer_id = lead.stripe_customer_id
    if not customer_id:
        try:
            customer = stripe.Customer.create(
                email=lead.email,
                name=lead.business_name or lead.name,
                metadata={"lead_id": str(lead.id), "business_name": lead.business_name or ""},
            )
            customer_id = customer.id
            lead.stripe_customer_id = customer_id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating customer: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            customer=customer_id,
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            subscription_data={
                "metadata": {
                    "lead_id": str(lead.id),
                    "plan": request.plan,
                    "plan_key": plan_key,
                    "billing_cycle": billing_cycle,
                    "vertical": vertical or "",
                    "business_name": lead.business_name or "",
                },
            },
            success_url=request.success_url or f"{settings.FRONTEND_URL}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=request.cancel_url or f"{settings.FRONTEND_URL}/checkout/cancel",
            metadata={
                "lead_id": str(lead.id),
                "plan": request.plan,
                "plan_key": plan_key,
                "billing_cycle": billing_cycle,
                "vertical": vertical or "",
                "business_name": lead.business_name or "",
                "type": "subscription_signup",
            },
        )

        # Record payment intent (real amount filled by webhook on checkout.session.completed)
        payment = Payment(
            lead_id=lead.id,
            stripe_checkout_session_id=session.id,
            stripe_customer_id=customer_id,
            amount_cents=0,
            currency="usd",
            plan_name=plan_key,
            payment_type=PaymentType.SETUP,
            status=PaymentStatus.PENDING,
            meta={
                "plan_name": PLAN_NAMES.get(plan_key, request.plan),
                "stripe_price_id": price_id,
                "billing_cycle": billing_cycle,
                "vertical": vertical or "",
            },
        )
        db.add(payment)
        await db.commit()

        return CheckoutSessionResponse(checkout_url=session.url, session_id=session.id)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portal", response_model=PortalSessionResponse)
async def create_portal_session(
    request: PortalSessionRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a Stripe Customer Portal session for a lead to manage their subscription."""
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    result = await db.execute(select(Lead).where(Lead.id == request.lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if not lead.stripe_customer_id:
        raise HTTPException(status_code=400, detail="Lead has no Stripe customer")

    try:
        session = stripe.billing_portal.Session.create(
            customer=lead.stripe_customer_id,
            return_url=request.return_url or f"{settings.FRONTEND_URL}/billing",
        )
        return PortalSessionResponse(portal_url=session.url)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating portal session: {e}")
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
            "customer": session.customer,
            "subscription": session.subscription,
            "metadata": session.metadata,
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/billing/{lead_id}")
async def get_billing_info(lead_id: int, db: AsyncSession = Depends(get_db)):
    """Get billing info for a lead — plan, subscription status, payment history."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Fetch payments
    from app.models.payment import Payment
    payments_result = await db.execute(
        select(Payment)
        .where(Payment.lead_id == lead_id)
        .order_by(Payment.created_at.desc())
    )
    payments = payments_result.scalars().all()

    # Fetch subscription from Stripe if customer exists
    subscription_info = None
    if lead.stripe_customer_id and settings.STRIPE_SECRET_KEY:
        try:
            subs = stripe.Subscription.list(
                customer=lead.stripe_customer_id,
                status="all",
                limit=1,
            )
            if subs.data:
                sub = subs.data[0]
                subscription_info = {
                    "id": sub.id,
                    "status": sub.status,
                    "current_period_start": sub.current_period_start,
                    "current_period_end": sub.current_period_end,
                    "cancel_at_period_end": sub.cancel_at_period_end,
                    "plan": sub.plan.nickname if sub.plan else None,
                }
        except stripe.error.StripeError as e:
            logger.warning(f"Stripe error fetching subscription: {e}")

    return {
        "lead_id": lead.id,
        "business_name": lead.business_name,
        "email": lead.email,
        "plan": lead.payment_plan,
        "subscription_status": lead.subscription_status,
        "stripe_customer_id": lead.stripe_customer_id,
        "payments": [
            {
                "id": p.id,
                "type": p.payment_type.value if p.payment_type else None,
                "status": p.status.value if p.status else None,
                "amount_cents": p.amount_cents,
                "currency": p.currency,
                "paid_at": p.paid_at.isoformat() if p.paid_at else None,
                "billing_period_start": p.billing_period_start.isoformat() if p.billing_period_start else None,
                "billing_period_end": p.billing_period_end.isoformat() if p.billing_period_end else None,
                "receipt_url": p.receipt_url,
                "meta": p.meta,
            }
            for p in payments
        ],
        "subscription": subscription_info,
    }


# ---------------------------------------------------------------------------
# Stripe Product/Price Seed (admin only — run once per environment)
# ---------------------------------------------------------------------------

@router.post("/seed-stripe")
async def seed_stripe_products():
    """Create Eko AI Products and recurring Prices in Stripe. Idempotent — safe to run multiple times.
    
    Returns the Price IDs to save in your .env as STRIPE_PRICE_STARTER/GROWTH/ENTERPRISE.
    """
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    plans = [
        {
            "key": "starter",
            "name": "Eko AI Starter",
            "description": "1 Agente IA personalizado, horario comercial, soporte por email.",
            "monthly_cents": 19900,
        },
        {
            "key": "growth",
            "name": "Eko AI Growth",
            "description": "2 Agentes IA, horario extendido, soporte prioritario, dashboard analytics.",
            "monthly_cents": 29900,
        },
        {
            "key": "enterprise",
            "name": "Eko AI Enterprise",
            "description": "Agentes IA ilimitados, 24/7, soporte dedicado, API access.",
            "monthly_cents": 39900,
        },
    ]

    results = []
    for plan in plans:
        try:
            # Search existing product by name to avoid duplicates
            existing_products = stripe.Product.search(
                query=f'name:"{plan["name"]}"',
                limit=1,
            )

            if existing_products.data:
                product = existing_products.data[0]
                logger.info(f"Product '{plan['name']}' already exists: {product.id}")
            else:
                product = stripe.Product.create(
                    name=plan["name"],
                    description=plan["description"],
                    metadata={"plan_key": plan["key"], "source": "eko_ai_seed"},
                )
                logger.info(f"Created product '{plan['name']}': {product.id}")

            # Search existing recurring price for this product
            existing_prices = stripe.Price.list(
                product=product.id,
                type="recurring",
                limit=1,
            )

            if existing_prices.data:
                price = existing_prices.data[0]
                logger.info(f"Price for '{plan['name']}' already exists: {price.id}")
            else:
                price = stripe.Price.create(
                    product=product.id,
                    unit_amount=plan["monthly_cents"],
                    currency="usd",
                    recurring={"interval": "month", "interval_count": 1},
                    metadata={"plan_key": plan["key"], "source": "eko_ai_seed"},
                )
                logger.info(f"Created price for '{plan['name']}': {price.id}")

            results.append({
                "plan": plan["key"],
                "product_id": product.id,
                "price_id": price.id,
                "amount_cents": plan["monthly_cents"],
                "status": "ok",
            })

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error seeding {plan['key']}: {e}")
            results.append({
                "plan": plan["key"],
                "error": str(e),
                "status": "error",
            })

    # Build env snippet
    env_snippet = "\n".join(
        f"STRIPE_PRICE_{r['plan'].upper()}={r.get('price_id', '')}"
        for r in results if r["status"] == "ok"
    )

    return {
        "results": results,
        "env_snippet": env_snippet,
        "note": "Copy the env_snippet above into your .env file and restart the backend.",
    }
