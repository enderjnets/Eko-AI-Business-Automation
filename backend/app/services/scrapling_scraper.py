"""Shared Scrapling-based scraping helper.

Phase 3 of the Scrapling integration. Provides a thin, reusable API for
fetching + parsing pages outside the WebsiteAnalyzer context — used by
Discovery sources as a fallback when paid APIs (Outscraper, Yelp Fusion,
Apify) return errors or quota exhaustion.

Reuses the same Redis circuit breaker as Phase 2 so the system can't be
DoSed by a flood of browser-rendered fetches across both code paths.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Optional

# Reuse the existing helpers from website.py rather than duplicate them.
from app.agents.research.analyzers.website import (
    _stealth_quota_available,
    _stealth_quota_inc,
    _USE_SCRAPLING,
    _USE_STEALTH,
    _SCRAPLING_AVAILABLE,
    _STEALTH_AVAILABLE,
)

logger = logging.getLogger(__name__)


# ── Cost-saving fallback toggle ────────────────────────────────────────
# When SCRAPLING_DISCOVERY_FALLBACK=true, Discovery sources will reach
# into this module after their paid API path errors out or returns 0
# results. Default false until we want to enable broadly.
DISCOVERY_FALLBACK_ENABLED = os.environ.get(
    "SCRAPLING_DISCOVERY_FALLBACK", "false"
).lower() in ("1", "true", "yes", "on")


async def fetch_page(
    url: str,
    *,
    use_browser: bool = False,
    timeout: float = 20.0,
) -> Optional[Any]:
    """Fetch a single page and return a Scrapling Selector object (or None).

    Args:
        url: target URL.
        use_browser: if True, go directly to StealthyFetcher (browser).
                     if False, try HTTP first (TLS impersonation Chrome).
        timeout: per-request timeout in seconds.

    Returns:
        A Scrapling page object (has .css(), .xpath(), .find_all(), .body)
        or None if every tier fails. Caller is responsible for selection.
    """
    if use_browser:
        return await _stealth_fetch(url)

    if _USE_SCRAPLING and _SCRAPLING_AVAILABLE:
        try:
            from scrapling.fetchers import AsyncFetcher
            page = await AsyncFetcher.get(
                url,
                timeout=timeout,
                stealthy_headers=True,
                impersonate="chrome",
                follow_redirects=True,
            )
            status = getattr(page, "status", 0) or 0
            if status and status < 400:
                return page
            logger.info(f"[scrapling-discovery] {url} status={status}, escalating to browser")
        except Exception as e:
            logger.info(f"[scrapling-discovery] {url} HTTP failed ({e!r})")

    # Escalate to browser if HTTP didn't work
    return await _stealth_fetch(url)


async def _stealth_fetch(url: str) -> Optional[Any]:
    """StealthyFetcher with circuit breaker."""
    if not (_USE_STEALTH and _STEALTH_AVAILABLE):
        return None
    if not _stealth_quota_available():
        logger.info(f"[stealth-discovery] {url} skipped (quota exhausted)")
        return None
    _stealth_quota_inc()
    try:
        from scrapling.fetchers import StealthyFetcher
        page = await StealthyFetcher.async_fetch(
            url,
            headless=True,
            network_idle=True,
        )
        status = getattr(page, "status", 0) or 0
        if status and status < 400:
            return page
        logger.info(f"[stealth-discovery] {url} status={status}")
    except Exception as e:
        logger.warning(f"[stealth-discovery] {url} failed: {e!r}")
    return None


async def scrape_yelp_listings(
    category: str,
    location: str,
    max_results: int = 20,
) -> list[dict]:
    """Scrape Yelp listing pages as a fallback when the Yelp API quota is hit.

    Yelp's HTML structure: each listing is a <div data-testid="serp-ia-card">
    or wrapped in <li class="...border-color--default__"> with the business
    name in a <h3><a> link.

    Returns a list of dicts shaped like:
        {business_name, website (yelp_url), category, address, city, state,
         phone, source, source_data: {...}}
    """
    from urllib.parse import quote_plus

    if not DISCOVERY_FALLBACK_ENABLED:
        logger.debug("Scrapling discovery fallback disabled (set SCRAPLING_DISCOVERY_FALLBACK=true)")
        return []

    # Yelp search URL pattern
    url = (
        f"https://www.yelp.com/search?find_desc={quote_plus(category)}"
        f"&find_loc={quote_plus(location)}"
    )
    logger.info(f"[scrapling-yelp] scraping {url}")

    # Yelp has fierce anti-bot; go straight to browser tier
    page = await fetch_page(url, use_browser=True, timeout=30.0)
    if page is None:
        return []

    leads = []
    try:
        # Selectors targeted at Yelp SERP layout (May 2026)
        cards = page.css('div[data-testid="serp-ia-card"]')
        for card in cards[:max_results]:
            name_el = card.css('h3 a::text').get() or card.css('h3 span::text').get()
            if not name_el:
                continue
            name = name_el.strip()
            yelp_link = card.css('h3 a::attr(href)').get() or ""
            if yelp_link and not yelp_link.startswith("http"):
                yelp_link = "https://www.yelp.com" + yelp_link
            # Category + neighborhood are usually small <p> tags below the name
            meta = card.css('p::text').getall()
            address = next((m.strip() for m in meta if any(d in m for d in ("Dr", "St", "Ave", "Blvd", "Rd"))), None)
            leads.append({
                "business_name": name,
                "category": category,
                "description": " · ".join(meta[:2]),
                "email": None,
                "phone": None,
                "website": yelp_link,
                "address": address,
                "city": location,
                "state": None,
                "source": "yelp_scrapling",
                "source_data": {"yelp_url": yelp_link, "raw_meta": meta},
            })
        logger.info(f"[scrapling-yelp] extracted {len(leads)} leads from {url}")
    except Exception as e:
        logger.warning(f"[scrapling-yelp] parse failed: {e!r}")

    return leads
