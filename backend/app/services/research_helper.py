"""Pre-AI research helper using Scrapling.

Phase 4 of the Scrapling integration. Lets generators (landing page,
proposal, sales brief) augment their AI prompt with FRESH web data:
the lead's current website summary, competitor snippets, recent reviews,
etc. — fetched on the fly with Scrapling instead of relying solely on
whatever was scraped during initial lead enrichment.

Why a helper instead of MCP server: Eko AI's AI client layer is built on
subprocess kimi-cli + REST calls to OpenAI/Anthropic. Wiring those to
speak Model Context Protocol would require refactoring multiple call
sites. A pre-fetch helper that injects research into the prompt delivers
the SAME end-user benefit (AI uses fresh data) without that refactor.

A proper MCP server integration is still possible via `scrapling[ai]`
and kimi-cli's --mcp flag — left as v0.8 work.
"""
from __future__ import annotations

import logging
import os
import re
from typing import Optional

from app.services.scrapling_scraper import fetch_page

logger = logging.getLogger(__name__)


# Cap research context per request so we don't blow up the AI prompt size.
_MAX_PROMPT_CONTEXT_CHARS = int(
    os.environ.get("SCRAPLING_RESEARCH_MAX_CHARS", "3000")
)

# Hard global toggle. Default ON so generators automatically benefit.
RESEARCH_HELPER_ENABLED = os.environ.get(
    "SCRAPLING_RESEARCH_HELPER", "true"
).lower() in ("1", "true", "yes", "on")


def _strip_to_visible_text(html: str, max_chars: int) -> str:
    """Quick HTML→plain-text conversion for prompt injection."""
    if not html:
        return ""
    # Drop scripts/styles entirely
    html = re.sub(
        r"<(script|style|noscript)[^>]*>.*?</\1>",
        "",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # Strip tags
    text = re.sub(r"<[^>]+>", " ", html)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


async def fetch_business_summary(
    url: str,
    *,
    max_chars: int = None,
    timeout: float = 15.0,
) -> Optional[str]:
    """Fetch a business website and return a short plain-text summary
    suitable for inclusion in an AI prompt.

    Returns None on any failure (e.g. site dead, anti-bot blocks).
    Always safe to call — no exceptions surface to caller.
    """
    if not RESEARCH_HELPER_ENABLED:
        return None
    if not url:
        return None
    cap = max_chars or _MAX_PROMPT_CONTEXT_CHARS

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        page = await fetch_page(url, use_browser=False, timeout=timeout)
        if page is None:
            return None
        body = getattr(page, "body", b"")
        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="replace")
        if not body:
            return None
        summary = _strip_to_visible_text(body, cap)
        if len(summary) < 100:
            # too thin — escalate to browser-rendered fetch
            page = await fetch_page(url, use_browser=True, timeout=timeout)
            if page is None:
                return summary or None
            body = getattr(page, "body", b"")
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")
            summary = _strip_to_visible_text(body, cap) or summary
        logger.debug(f"[research] {url} -> {len(summary)} chars of context")
        return summary or None
    except Exception as e:
        logger.warning(f"[research] {url} failed: {e!r}")
        return None


async def build_landing_page_context(
    website: Optional[str],
    *,
    extra_urls: Optional[list[str]] = None,
) -> str:
    """Build a research-context block to inject into the landing-page
    generator prompt.

    Format (markdown-ish, AI-friendly):

        ## Research context (fresh fetch)
        ### {website}
        ...summary...

        ### Competitor: {competitor_url}
        ...summary...
    """
    if not RESEARCH_HELPER_ENABLED:
        return ""

    parts: list[str] = []
    if website:
        summary = await fetch_business_summary(website)
        if summary:
            parts.append(f"### Business site: {website}\n{summary}\n")

    for extra in (extra_urls or [])[:2]:  # cap at 2 competitors
        summary = await fetch_business_summary(extra)
        if summary:
            parts.append(f"### Reference: {extra}\n{summary}\n")

    if not parts:
        return ""
    return "## Research context (fresh fetch via Scrapling)\n\n" + "\n".join(parts)
