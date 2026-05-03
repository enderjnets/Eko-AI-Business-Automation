"""Stripe webhook handler for subscriptions and payments."""

import json
import logging
from datetime import datetime

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.lead import Lead, LeadStatus
from app.models.deal import Deal, DealStatus
from app.models.payment import Payment, PaymentStatus, PaymentType
from app.agents.outreach.channels.email import EmailOutreach
from app.config import get_settings

settings = get_settings()
router = APIRouter()
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not settings.STRIPE_WEBHOOK_SECRET:
        logger.warning("STRIPE_WEBHOOK_SECRET not set — skipping verification")
        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]
    data = event["data"]["object"]
    logger.info(f"Stripe webhook: {event_type} — {data.get('id', 'no-id')}")

    if event_type == "checkout.session.completed":
        await _handle_checkout_completed(data, db)
    elif event_type == "invoice.payment_succeeded":
        await _handle_invoice_payment_succeeded(data, db)
    elif event_type == "invoice.payment_failed":
        await _handle_invoice_payment_failed(data, db)
    elif event_type == "customer.subscription.updated":
        await _handle_subscription_updated(data, db)
    elif event_type == "customer.subscription.deleted":
        await _handle_subscription_deleted(data, db)
    elif event_type == "checkout.session.expired":
        await _handle_checkout_expired(data, db)
    elif event_type == "charge.refunded":
        await _handle_refund(data, db)
    else:
        logger.info(f"Unhandled Stripe event: {event_type}")

    return {"status": "ok"}


async def _handle_checkout_completed(session: dict, db: AsyncSession):
    """Process successful checkout — activate customer + send onboarding email."""
    metadata = session.get("metadata", {})
    lead_id = int(metadata.get("lead_id", 0))
    plan = metadata.get("plan", "unknown")
    session_id = session.get("id")
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")

    if not lead_id:
        logger.error("No lead_id in session metadata")
        return

    # Find or create payment record
    result = await db.execute(
        select(Payment).where(Payment.stripe_checkout_session_id == session_id)
    )
    payment = result.scalar_one_or_none()

    if not payment:
        payment = Payment(
            lead_id=lead_id,
            stripe_checkout_session_id=session_id,
            stripe_customer_id=customer_id,
            stripe_subscription_id=subscription_id,
            stripe_payment_intent_id=session.get("payment_intent"),
            amount_cents=session.get("amount_total", 0),
            currency=session.get("currency", "usd"),
            plan_name=plan,
            payment_type=PaymentType.SETUP,
            status=PaymentStatus.COMPLETED,
            paid_at=datetime.utcnow(),
            meta={
                "customer_email": session.get("customer_email"),
                "plan": plan,
                "subscription_id": subscription_id,
            },
        )
        db.add(payment)
    else:
        payment.status = PaymentStatus.COMPLETED
        payment.stripe_payment_intent_id = session.get("payment_intent")
        payment.stripe_customer_id = customer_id
        payment.stripe_subscription_id = subscription_id
        payment.paid_at = datetime.utcnow()

    # Update lead to ACTIVE
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if lead:
        lead.status = LeadStatus.ACTIVE
        lead.payment_plan = plan
        lead.subscription_status = "active"
        lead.stripe_customer_id = customer_id
        if lead.source_data is None:
            lead.source_data = {}
        lead.source_data["payment"] = {
            "plan": plan,
            "paid_at": datetime.utcnow().isoformat(),
            "amount_cents": session.get("amount_total"),
            "session_id": session_id,
            "subscription_id": subscription_id,
        }

        # Update deal to CLOSED_WON
        deal_result = await db.execute(
            select(Deal).where(Deal.lead_id == lead.id).order_by(Deal.created_at.desc())
        )
        deal = deal_result.scalar_one_or_none()
        if deal:
            deal.status = DealStatus.CLOSED_WON
            deal.value = (session.get("amount_total", 0)) / 100.0
            deal.actual_revenue = deal.value
            if deal.meta is None:
                deal.meta = {}
            deal.meta["paid_at"] = datetime.utcnow().isoformat()
            deal.meta["plan"] = plan
            deal.meta["subscription_id"] = subscription_id

        # Send onboarding welcome email
        try:
            await _send_onboarding_email(lead)
        except Exception as e:
            logger.error(f"Failed to send onboarding email: {e}")

    await db.commit()
    logger.info(f"Lead {lead_id} activated — plan: {plan}, subscription: {subscription_id}")


async def _handle_invoice_payment_succeeded(invoice: dict, db: AsyncSession):
    """Record a successful subscription payment (monthly recurrence)."""
    subscription_id = invoice.get("subscription")
    customer_id = invoice.get("customer")
    invoice_id = invoice.get("id")
    amount_paid = invoice.get("amount_paid", 0)
    currency = invoice.get("currency", "usd")
    period_start = invoice.get("period_start")
    period_end = invoice.get("period_end")

    # Find lead by customer_id
    result = await db.execute(select(Lead).where(Lead.stripe_customer_id == customer_id))
    lead = result.scalar_one_or_none()
    if not lead:
        logger.warning(f"No lead found for customer {customer_id}")
        return

    # Skip if this is the first invoice (already handled by checkout.session.completed)
    # The first invoice for a subscription includes the setup fee
    lines = invoice.get("lines", {}).get("data", [])
    is_first_invoice = any(
        line.get("price", {}).get("type") == "one_time" or line.get("description", "").lower().startswith("setup")
        for line in lines
    )

    if is_first_invoice:
        logger.info(f"First invoice for subscription {subscription_id} — skipping (handled by checkout)")
        return

    # Record subscription payment
    payment = Payment(
        lead_id=lead.id,
        stripe_subscription_id=subscription_id,
        stripe_invoice_id=invoice_id,
        stripe_customer_id=customer_id,
        amount_cents=amount_paid,
        currency=currency,
        plan_name=lead.payment_plan or "unknown",
        payment_type=PaymentType.SUBSCRIPTION,
        status=PaymentStatus.COMPLETED,
        paid_at=datetime.utcnow(),
        billing_period_start=datetime.fromtimestamp(period_start) if period_start else None,
        billing_period_end=datetime.fromtimestamp(period_end) if period_end else None,
        meta={
            "invoice_number": invoice.get("number"),
            "hosted_invoice_url": invoice.get("hosted_invoice_url"),
            "invoice_pdf": invoice.get("invoice_pdf"),
        },
    )
    db.add(payment)

    lead.subscription_status = "active"
    lead.past_due_since = None

    await db.commit()
    logger.info(f"Subscription payment recorded for lead {lead.id} — ${amount_paid / 100:.2f}")


async def _handle_invoice_payment_failed(invoice: dict, db: AsyncSession):
    """Mark subscription as past_due when payment fails."""
    customer_id = invoice.get("customer")
    subscription_id = invoice.get("subscription")
    attempt_count = invoice.get("attempt_count", 0)

    result = await db.execute(select(Lead).where(Lead.stripe_customer_id == customer_id))
    lead = result.scalar_one_or_none()
    if not lead:
        logger.warning(f"No lead found for customer {customer_id}")
        return

    lead.subscription_status = "past_due"
    if not lead.past_due_since:
        lead.past_due_since = datetime.utcnow()

    # Send payment failed email if this is the first attempt
    if attempt_count == 1:
        try:
            await _send_payment_failed_email(lead, invoice)
        except Exception as e:
            logger.error(f"Failed to send payment failed email: {e}")

    await db.commit()
    logger.info(f"Lead {lead.id} marked past_due (attempt {attempt_count})")


async def _handle_subscription_updated(subscription: dict, db: AsyncSession):
    """Handle plan changes, cancelation schedules, etc."""
    customer_id = subscription.get("customer")
    status = subscription.get("status")  # active, past_due, canceled, unpaid, etc.
    cancel_at_period_end = subscription.get("cancel_at_period_end", False)
    current_period_end = subscription.get("current_period_end")

    result = await db.execute(select(Lead).where(Lead.stripe_customer_id == customer_id))
    lead = result.scalar_one_or_none()
    if not lead:
        logger.warning(f"No lead found for customer {customer_id}")
        return

    old_status = lead.subscription_status
    lead.subscription_status = status

    # Handle cancellation scheduled
    if cancel_at_period_end and old_status != "canceling":
        lead.subscription_status = "canceling"
        try:
            await _send_cancellation_scheduled_email(lead, subscription)
        except Exception as e:
            logger.error(f"Failed to send cancellation scheduled email: {e}")

    # Handle reactivation (cancel_at_period_end flipped to false)
    if not cancel_at_period_end and old_status == "canceling":
        lead.subscription_status = "active"
        logger.info(f"Lead {lead.id} reactivated subscription")

    await db.commit()
    logger.info(f"Lead {lead.id} subscription updated — status: {lead.subscription_status}")


async def _handle_subscription_deleted(subscription: dict, db: AsyncSession):
    """Handle subscription cancellation — suspend service."""
    customer_id = subscription.get("customer")

    result = await db.execute(select(Lead).where(Lead.stripe_customer_id == customer_id))
    lead = result.scalar_one_or_none()
    if not lead:
        logger.warning(f"No lead found for customer {customer_id}")
        return

    lead.subscription_status = "canceled"
    lead.status = LeadStatus.AT_RISK

    try:
        await _send_subscription_canceled_email(lead)
    except Exception as e:
        logger.error(f"Failed to send subscription canceled email: {e}")

    await db.commit()
    logger.info(f"Lead {lead.id} subscription canceled")


async def _handle_checkout_expired(session: dict, db: AsyncSession):
    """Mark payment as abandoned."""
    session_id = session.get("id")
    result = await db.execute(
        select(Payment).where(Payment.stripe_checkout_session_id == session_id)
    )
    payment = result.scalar_one_or_none()
    if payment and payment.status == PaymentStatus.PENDING:
        payment.status = PaymentStatus.ABANDONED
        await db.commit()
        logger.info(f"Payment {payment.id} marked abandoned")


async def _handle_refund(charge: dict, db: AsyncSession):
    """Process refund."""
    payment_intent = charge.get("payment_intent")
    if not payment_intent:
        return

    result = await db.execute(
        select(Payment).where(Payment.stripe_payment_intent_id == payment_intent)
    )
    payment = result.scalar_one_or_none()
    if payment:
        payment.status = PaymentStatus.REFUNDED
        if payment.meta is None:
            payment.meta = {}
        payment.meta["refunded_at"] = datetime.utcnow().isoformat()
        payment.meta["refund_amount_cents"] = charge.get("amount_refunded", 0)
        await db.commit()
        logger.info(f"Payment {payment.id} marked refunded")


# ---------------------------------------------------------------------------
# Email notifications
# ---------------------------------------------------------------------------

async def _send_onboarding_email(lead: Lead):
    """Send welcome onboarding email to new customer."""
    email = EmailOutreach()

    context = f"""
    El cliente {lead.business_name or lead.name} acaba de completar el pago para Eko AI.
    Plan contratado: {lead.payment_plan or 'Starter'}.
    Mensaje a enviar: Bienvenida como cliente, próximos pasos del onboarding,
    link al portal de cliente, y contacto directo con el equipo de implementación.
    """

    await email.generate_and_send(
        lead=lead,
        template_key="welcome_onboarding",
        campaign_context=context,
    )

    logger.info(f"Onboarding email sent to {lead.email}")


async def _send_payment_failed_email(lead: Lead, invoice: dict):
    """Send payment failed reminder with portal link."""
    email = EmailOutreach()

    context = f"""
    El cliente {lead.business_name or lead.name} tiene un pago fallido de su suscripción Eko AI.
    Plan: {lead.payment_plan or 'Starter'}.
    Mensaje a enviar: Amable recordatorio de que el pago mensual no pudo procesarse.
    Instrucciones para actualizar método de pago en el portal de cliente.
    No alarmista — tono profesional y de ayuda.
    """

    await email.generate_and_send(
        lead=lead,
        template_key="payment_failed",
        campaign_context=context,
    )

    logger.info(f"Payment failed email sent to {lead.email}")


async def _send_cancellation_scheduled_email(lead: Lead, subscription: dict):
    """Notify customer that cancellation is scheduled at period end."""
    email = EmailOutreach()
    current_period_end = subscription.get("current_period_end")
    end_date = ""
    if current_period_end:
        end_date = datetime.fromtimestamp(current_period_end).strftime("%B %d, %Y")

    context = f"""
    El cliente {lead.business_name or lead.name} ha programado la cancelación de su suscripción Eko AI.
    Plan: {lead.payment_plan or 'Starter'}.
    Fecha de cierre: {end_date}.
    Mensaje a enviar: Confirmación de cancelación programada. El servicio seguirá activo hasta esa fecha.
    Oferta de retención suave: si hay algo que no les funcionó, ofrecer una llamada rápida.
    """

    await email.generate_and_send(
        lead=lead,
        template_key="subscription_canceled",
        campaign_context=context,
    )

    logger.info(f"Cancellation scheduled email sent to {lead.email}")


async def _send_subscription_canceled_email(lead: Lead):
    """Notify that subscription has been canceled."""
    email = EmailOutreach()

    context = f"""
    El cliente {lead.business_name or lead.name} ha cancelado su suscripción Eko AI.
    Plan: {lead.payment_plan or 'Starter'}.
    Mensaje a enviar: Confirmación de cancelación. Servicio suspendido.
    Puerta abierta para reactivación en el futuro. Tonos amables y profesionales.
    """

    await email.generate_and_send(
        lead=lead,
        template_key="subscription_canceled",
        campaign_context=context,
    )

    logger.info(f"Subscription canceled email sent to {lead.email}")
