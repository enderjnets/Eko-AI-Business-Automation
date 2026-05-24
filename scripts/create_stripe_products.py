#!/usr/bin/env python3
"""Provision Eko AI pricing v2 (Council 2026-05-24) products and prices in Stripe.

Idempotent: looks up existing products by `metadata.eko_id` and skips creation if a price already
exists at the same amount + interval. Re-running the script is safe.

Usage:
    # Dry-run (default): prints what would be created, touches nothing in Stripe.
    STRIPE_SECRET_KEY=sk_test_... python3 scripts/create_stripe_products.py --dry-run

    # Actually create (test mode):
    STRIPE_SECRET_KEY=sk_test_... python3 scripts/create_stripe_products.py

    # Live mode (be careful):
    STRIPE_SECRET_KEY=sk_live_... python3 scripts/create_stripe_products.py --live

At the end, prints the env-var assignments to paste into `.env`. The new IDs coexist with the
legacy STRIPE_PRICE_STARTER/GROWTH/ENTERPRISE; the checkout flow falls back to legacy if a new
*_MONTHLY/_ANNUAL env var is empty (see backend/app/api/v1/checkout.py:_resolve_price_id).
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import stripe
except ImportError:
    print("ERROR: install stripe first → pip install stripe", file=sys.stderr)
    sys.exit(1)


@dataclass(frozen=True)
class SkuSpec:
    eko_id: str                 # stable identifier stored in metadata.eko_id (idempotency key)
    name: str                   # human-readable Stripe product name
    description: str
    amount_cents: int           # USD cents
    interval: Optional[str]     # "month" | "year" | None for one-time
    env_var: str                # which .env var receives the resulting price ID

    @property
    def is_recurring(self) -> bool:
        return self.interval is not None


# ── Pricing v2 catalog (12 prices + 5 add-on prices = 17 prices, 11 distinct products) ──
SPECS: list[SkuSpec] = [
    # Starter ($249 / mo, $2,388 / yr = $199 / mo equiv)
    SkuSpec("starter",  "Eko AI Starter",  "Solo operator toolkit. 1 agent, 5 users, 1K runs/mo.",
            24900, "month", "STRIPE_PRICE_STARTER_MONTHLY"),
    SkuSpec("starter",  "Eko AI Starter",  "Solo operator toolkit. 1 agent, 5 users, 1K runs/mo.",
            238800, "year", "STRIPE_PRICE_STARTER_ANNUAL"),

    # Growth — Accounting ($749 / mo, $7,188 / yr)
    SkuSpec("growth_accounting", "Eko AI Growth — Accounting",
            "Local invoice OCR, ERPs Contasol/Anfix/SII/Alegra, offline reconciliation. 5 agents, 10 users, 10K runs/mo.",
            74900, "month", "STRIPE_PRICE_GROWTH_ACCOUNTING_MONTHLY"),
    SkuSpec("growth_accounting", "Eko AI Growth — Accounting",
            "Local invoice OCR, ERPs Contasol/Anfix/SII/Alegra, offline reconciliation. 5 agents, 10 users, 10K runs/mo.",
            718800, "year", "STRIPE_PRICE_GROWTH_ACCOUNTING_ANNUAL"),

    # Growth — Real Estate ($749 / mo, $7,188 / yr)
    SkuSpec("growth_realestate", "Eko AI Growth — Real Estate",
            "WhatsApp Business API (2K conv/mo), Idealista/Fotocasa, lead scoring + post-visit sequences.",
            74900, "month", "STRIPE_PRICE_GROWTH_REALESTATE_MONTHLY"),
    SkuSpec("growth_realestate", "Eko AI Growth — Real Estate",
            "WhatsApp Business API (2K conv/mo), Idealista/Fotocasa, lead scoring + post-visit sequences.",
            718800, "year", "STRIPE_PRICE_GROWTH_REALESTATE_ANNUAL"),

    # Growth — Legal/Clinic ($749 / mo, $7,188 / yr)
    SkuSpec("growth_legalhealth", "Eko AI Growth — Legal / Clinic",
            "Document manager + contract OCR + local e-signature + GDPR/HIPAA audit log + DPIA templates.",
            74900, "month", "STRIPE_PRICE_GROWTH_LEGALHEALTH_MONTHLY"),
    SkuSpec("growth_legalhealth", "Eko AI Growth — Legal / Clinic",
            "Document manager + contract OCR + local e-signature + GDPR/HIPAA audit log + DPIA templates.",
            718800, "year", "STRIPE_PRICE_GROWTH_LEGALHEALTH_ANNUAL"),

    # Enterprise ($1,999 / mo, $19,188 / yr)
    SkuSpec("enterprise", "Eko AI Enterprise",
            "All 3 Growth verticals + unlimited agents/users + 100K runs/mo + multi-tenant + white-label + 24/7 support + on-prem install FREE year 1.",
            199900, "month", "STRIPE_PRICE_ENTERPRISE_MONTHLY"),
    SkuSpec("enterprise", "Eko AI Enterprise",
            "All 3 Growth verticals + unlimited agents/users + 100K runs/mo + multi-tenant + white-label + 24/7 support + on-prem install FREE year 1.",
            1918800, "year", "STRIPE_PRICE_ENTERPRISE_ANNUAL"),

    # Add-ons
    SkuSpec("addon_whitelabel", "Eko AI Add-on — White-label",
            "Your domain + portal branding. Removes Eko AI mentions.",
            15000, "month", "STRIPE_PRICE_ADDON_WHITELABEL"),
    SkuSpec("addon_whatsapp_extra", "Eko AI Add-on — Extra WhatsApp number",
            "Additional WhatsApp Business API number, fully provisioned.",
            5000, "month", "STRIPE_PRICE_ADDON_WHATSAPP_EXTRA"),
    SkuSpec("addon_custom_integration_setup", "Eko AI Add-on — Custom integration (setup)",
            "One-time setup fee for a custom integration we build for you.",
            50000, None, "STRIPE_PRICE_ADDON_CUSTOM_INTEGRATION_SETUP"),
    SkuSpec("addon_custom_integration_recurring", "Eko AI Add-on — Custom integration (maintenance)",
            "Monthly maintenance for a custom integration we maintain for you.",
            5000, "month", "STRIPE_PRICE_ADDON_CUSTOM_INTEGRATION_RECURRING"),
    SkuSpec("addon_onprem_setup", "Eko AI Add-on — On-premise install",
            "On-site or remote installation of Eko AI on your hardware. FREE year 1 in Enterprise.",
            150000, None, "STRIPE_PRICE_ONPREM_SETUP"),
]


def find_or_create_product(spec: SkuSpec, dry_run: bool) -> Optional[str]:
    """Return product_id for the spec, creating it if missing."""
    if dry_run:
        return f"prod_DRYRUN_{spec.eko_id}"

    existing = stripe.Product.search(query=f'metadata["eko_id"]:"{spec.eko_id}" AND active:"true"', limit=1)
    if existing.data:
        return existing.data[0].id

    p = stripe.Product.create(
        name=spec.name,
        description=spec.description,
        metadata={"eko_id": spec.eko_id, "eko_version": "v2", "council_date": "2026-05-24"},
    )
    return p.id


def find_or_create_price(spec: SkuSpec, product_id: str, dry_run: bool) -> Optional[str]:
    """Return price_id with the given amount + interval. Creates if no existing match."""
    if dry_run:
        suffix = spec.interval or "once"
        return f"price_DRYRUN_{spec.eko_id}_{suffix}"

    existing = stripe.Price.list(product=product_id, active=True, limit=100)
    for px in existing.data:
        if px.unit_amount != spec.amount_cents:
            continue
        if spec.interval is None and px.type == "one_time":
            return px.id
        if px.recurring and px.recurring.get("interval") == spec.interval:
            return px.id

    payload: dict = {"product": product_id, "currency": "usd", "unit_amount": spec.amount_cents}
    if spec.interval is None:
        payload["nickname"] = f"{spec.eko_id} (one-time)"
    else:
        payload["recurring"] = {"interval": spec.interval}
        payload["nickname"] = f"{spec.eko_id} {spec.interval}ly"
    p = stripe.Price.create(**payload)
    return p.id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print what would be created, touch nothing")
    parser.add_argument("--live", action="store_true", help="Allow running with a sk_live_ key (default rejects to avoid mistakes)")
    args = parser.parse_args()

    key = os.environ.get("STRIPE_SECRET_KEY", "").strip()
    if not args.dry_run and not key:
        print("ERROR: STRIPE_SECRET_KEY env var is required (or pass --dry-run)", file=sys.stderr)
        return 1
    if key.startswith("sk_live_") and not args.live and not args.dry_run:
        print("REFUSING to run against a LIVE key without --live flag. Re-run with --live if intentional.", file=sys.stderr)
        return 2

    if not args.dry_run:
        stripe.api_key = key

    mode = "DRY-RUN" if args.dry_run else ("LIVE" if key.startswith("sk_live_") else "TEST")
    print(f"\n=== Eko AI pricing v2 provisioning — mode={mode} ===\n")

    env_lines: list[str] = []
    for spec in SPECS:
        product_id = find_or_create_product(spec, args.dry_run)
        price_id = find_or_create_price(spec, product_id, args.dry_run)
        cents = f"${spec.amount_cents/100:>9,.2f}"
        kind = spec.interval if spec.interval else "one-time"
        print(f"  {spec.env_var:<55} = {price_id}   [{kind:>7} | {cents}]")
        env_lines.append(f"{spec.env_var}={price_id}")

    print("\n--- Paste into .env ---")
    print("\n".join(env_lines))
    print("\nDone. After updating .env, restart eko-backend: `docker compose restart eko-backend`\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
