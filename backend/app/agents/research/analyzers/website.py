import os
import re
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Tuple

import httpx
from bs4 import BeautifulSoup
from langdetect import detect

import logging

logger = logging.getLogger(__name__)


# Phase 1 of Scrapling integration: AsyncFetcher with TLS impersonation
# replaces raw httpx for the network layer. Parsing stays on BeautifulSoup
# so this is a drop-in change with zero behavior diff on the parsing side.
# Toggle with USE_SCRAPLING=true env var. Default ON so we A/B in prod.
_USE_SCRAPLING = os.environ.get("USE_SCRAPLING", "true").lower() in ("1", "true", "yes", "on")

# Phase 2: also try a browser-rendered fetch (StealthyFetcher) when the
# HTTP path returns very thin content (JS-rendered page) or hard 4xx/5xx.
# Toggle with USE_STEALTH=true. Default ON because chromium ships in Docker.
_USE_STEALTH = os.environ.get("USE_STEALTH", "true").lower() in ("1", "true", "yes", "on")

# Threshold below which we suspect a JS-rendered page (raw HTML body is
# mostly empty <div>s before hydration). Tuned at 1500 chars of <body> text.
_THIN_BODY_THRESHOLD = int(os.environ.get("STEALTH_THIN_THRESHOLD", "1500"))

try:
    from scrapling.fetchers import AsyncFetcher as _ScraplingAsyncFetcher
    _SCRAPLING_AVAILABLE = True
    # Silence Scrapling's chatty per-request INFO logs in production paths
    # (we already log at our own debug level inside _fetch_html).
    logging.getLogger("scrapling").setLevel(logging.WARNING)
except Exception as _e:  # pragma: no cover
    _ScraplingAsyncFetcher = None
    _SCRAPLING_AVAILABLE = False
    logger.warning(f"Scrapling unavailable, falling back to httpx-only: {_e}")

try:
    from scrapling.fetchers import StealthyFetcher as _ScraplingStealthy
    _STEALTH_AVAILABLE = True
except Exception as _e:  # pragma: no cover
    _ScraplingStealthy = None
    _STEALTH_AVAILABLE = False
    logger.warning(f"StealthyFetcher unavailable (will skip browser tier): {_e}")


# ── Phase 2 circuit breaker ────────────────────────────────────────────
# Browser-rendered fetches are slow (~10-30s each) and memory-hungry
# (~200MB per chrome instance). We MUST cap usage so a flood of bad URLs
# can't pin the worker. Pattern lifted from v0.7.15 Resend quota breaker.
#
# Two limits:
#   1. Per-minute cap (rolling counter in Redis): max 10 browser fetches/min
#   2. Daily cap: max 200 browser fetches/day (resets at UTC midnight)
# If either trips, browser tier short-circuits; httpx-only path is used.

_BROWSER_PER_MIN_KEY = "scraping:stealth:per_minute"
_BROWSER_DAILY_KEY = "scraping:stealth:daily"
_BROWSER_PER_MIN_CAP = int(os.environ.get("STEALTH_PER_MIN_CAP", "10"))
_BROWSER_DAILY_CAP = int(os.environ.get("STEALTH_DAILY_CAP", "200"))


def _redis_client():
    try:
        import redis as _redis
        url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
        return _redis.from_url(url, socket_timeout=2, socket_connect_timeout=2)
    except Exception:
        return None


def _stealth_quota_available() -> bool:
    """Return True if we can fire another browser fetch right now."""
    r = _redis_client()
    if r is None:
        return True  # fail-open if redis is down — better to attempt than block
    try:
        per_min = int(r.get(_BROWSER_PER_MIN_KEY) or 0)
        daily = int(r.get(_BROWSER_DAILY_KEY) or 0)
        if per_min >= _BROWSER_PER_MIN_CAP:
            logger.info(f"[stealth] per-minute cap {per_min}/{_BROWSER_PER_MIN_CAP} reached")
            return False
        if daily >= _BROWSER_DAILY_CAP:
            logger.warning(f"[stealth] daily cap {daily}/{_BROWSER_DAILY_CAP} reached")
            return False
        return True
    except Exception:
        return True


def _stealth_quota_inc() -> None:
    """Increment per-minute (TTL 60s) and daily (TTL until UTC midnight) counters."""
    r = _redis_client()
    if r is None:
        return
    try:
        # per-minute: simple key with TTL 60
        pipe = r.pipeline()
        pipe.incr(_BROWSER_PER_MIN_KEY)
        pipe.expire(_BROWSER_PER_MIN_KEY, 60, nx=True)  # set TTL only if missing
        # daily: TTL = seconds until next UTC midnight
        now = datetime.now(timezone.utc)
        from datetime import timedelta as _td
        next_midnight = (now + _td(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        ttl = max(60, int((next_midnight - now).total_seconds()))
        pipe.incr(_BROWSER_DAILY_KEY)
        pipe.expire(_BROWSER_DAILY_KEY, ttl, nx=True)
        pipe.execute()
    except Exception as e:
        logger.warning(f"[stealth] failed to increment quota: {e}")


def _looks_thin(text: str) -> bool:
    """Detect a JS-rendered page by counting visible text in <body>."""
    if not text:
        return True
    # Quick & cheap: count <p>+<h*>+<li> blocks. <500 chars of <body> after
    # stripping tags is the usual signature of a Wix/Squarespace shell.
    body_match = re.search(r"<body[^>]*>(.*?)</body>", text, re.DOTALL | re.IGNORECASE)
    if not body_match:
        return True
    body_html = body_match.group(1)
    # strip tags + scripts/styles
    body_text = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", "", body_html, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r"<[^>]+>", " ", body_text)
    body_text = re.sub(r"\s+", " ", body_text).strip()
    return len(body_text) < _THIN_BODY_THRESHOLD


class WebsiteAnalyzer:
    """Analyze a business website to extract insights."""

    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=15.0,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )
        # Track which fetcher served each request — used in audit logs.
        self._last_fetcher = "init"

    async def _fetch_html(self, url: str, timeout: float = 15.0) -> Tuple[str, int]:
        """Fetch HTML returning (text, status_code).

        Layered chain (each tier tries only if the previous fails):
          1. Scrapling AsyncFetcher (TLS impersonation, stealth headers) — fast HTTP
          2. httpx with browser UA — historic default
          3. httpx without UA — legacy 403 fallback
          4. Scrapling StealthyFetcher (Phase 2) — browser-rendered, anti-bot,
             only invoked when prior tiers returned 4xx or a "thin" body
             (suggests JS-rendered page). Gated by Redis circuit breaker.
        """
        t0 = time.monotonic()
        text = ""
        status = 0
        http_failed = False

        # Step 1: Scrapling HTTP fetcher
        if _USE_SCRAPLING and _SCRAPLING_AVAILABLE:
            try:
                page = await _ScraplingAsyncFetcher.get(
                    url,
                    timeout=timeout,
                    stealthy_headers=True,
                    impersonate="chrome",
                    follow_redirects=True,
                )
                status = getattr(page, "status", 0) or 0
                body = getattr(page, "body", b"")
                if isinstance(body, bytes):
                    text = body.decode("utf-8", errors="replace")
                else:
                    text = body
                if status and status < 400:
                    self._last_fetcher = "scrapling"
                    logger.debug(
                        f"[scrapling] {url} status={status} bytes={len(text)} t={time.monotonic()-t0:.2f}s"
                    )
                    # Phase 2 escalation: even on 200, if body is thin (JS-rendered),
                    # try browser to get real content. Otherwise return as-is.
                    if not (_USE_STEALTH and _STEALTH_AVAILABLE and _looks_thin(text)):
                        return text, status
                    logger.info(f"[scrapling] {url} thin body ({len(text)} chars), trying stealth")
                else:
                    logger.info(f"[scrapling] {url} returned {status}, falling back to httpx")
            except Exception as e:
                logger.info(f"[scrapling] {url} failed ({e!r}), falling back to httpx")
                http_failed = True

        # Step 2 + 3: httpx with browser UA, then without UA
        if status == 0 or status >= 400 or http_failed:
            try:
                resp = await self.client.get(url, timeout=timeout)
                if resp.status_code == 403:
                    logger.info(f"[httpx] {url} got 403, retrying without User-Agent")
                    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as temp:
                        resp = await temp.get(url)
                self._last_fetcher = "httpx"
                text = resp.text
                status = resp.status_code
                logger.debug(
                    f"[httpx] {url} status={status} bytes={len(text)} t={time.monotonic()-t0:.2f}s"
                )
            except Exception as e:
                self._last_fetcher = "error"
                http_failed = True
                logger.warning(f"[httpx-fail] {url}: {e!r}")
                # don't raise yet — give stealth a chance below

        # Step 4: Scrapling StealthyFetcher (browser-rendered, anti-bot).
        # Only when prior tiers returned 4xx OR a thin body.
        should_try_stealth = (
            _USE_STEALTH and _STEALTH_AVAILABLE and (
                http_failed
                or status >= 400
                or _looks_thin(text)
            )
        )
        if should_try_stealth:
            if not _stealth_quota_available():
                logger.info(f"[stealth] {url} skipped (quota exhausted)")
            else:
                _stealth_quota_inc()
                try:
                    t1 = time.monotonic()
                    page = await _ScraplingStealthy.async_fetch(
                        url,
                        headless=True,
                        network_idle=True,
                    )
                    s_status = getattr(page, "status", 0) or 0
                    s_body = getattr(page, "body", b"")
                    if isinstance(s_body, bytes):
                        s_text = s_body.decode("utf-8", errors="replace")
                    else:
                        s_text = s_body
                    logger.info(
                        f"[stealth] {url} status={s_status} bytes={len(s_text)} "
                        f"t={time.monotonic()-t1:.1f}s (total={time.monotonic()-t0:.1f}s)"
                    )
                    if s_status and s_status < 400 and len(s_text) > len(text):
                        self._last_fetcher = "stealth"
                        return s_text, s_status
                except Exception as e:
                    logger.warning(f"[stealth-fail] {url}: {e!r}")

        if http_failed and not text:
            raise RuntimeError(f"all fetch tiers failed for {url}")

        return text, status

    def _clean_text_for_matching(self, html_text: str) -> str:
        """Strip <style>, <script>, inline styles, and HTML comments to avoid false positives."""
        # Remove <style> blocks
        text = re.sub(r'<style[^>]*>.*?</style>', '', html_text, flags=re.DOTALL)
        # Remove <script> blocks
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        # Remove <noscript> blocks
        text = re.sub(r'<noscript[^>]*>.*?</noscript>', '', text, flags=re.DOTALL)
        # Remove HTML comments (often contain CSS/JS)
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        # Remove inline style attributes
        text = re.sub(r'\s+style="[^"]*"', '', text)
        # Remove other inline style-like attributes (e.g. style='...')
        text = re.sub(r"\s+style='[^']*'", '', text)
        return text

    async def close(self):
        await self.client.aclose()

    async def analyze(self, url: str) -> Dict:
        """
        Fetch and analyze a website.

        Returns:
            Dict with: title, description, technologies_detected, has_chatbot,
            has_booking, has_contact_form, social_links, email_found,
            services, pricing_info, hours, about_text, team_names,
            has_ecommerce, has_blog, has_newsletter
        """
        if not url.startswith("http"):
            url = f"https://{url}"

        url_lower = url.lower()

        # Skip PDFs entirely
        if url_lower.endswith(".pdf") or ".pdf?" in url_lower or ".pdf#" in url_lower:
            logger.warning(f"Skipping PDF URL: {url}")
            return {"error": "PDF documents are not supported", "url": url}

        # Skip government domains
        domain = url.split("/")[2].lower().replace("www.", "")
        if domain.endswith(".gov") or domain.endswith(".mil") or ".gov." in domain:
            logger.warning(f"Skipping government URL: {url}")
            return {"error": "Government websites are not supported", "url": url}

        try:
            response_text, status_code = await self._fetch_html(url)
            if status_code and status_code >= 400:
                logger.warning(f"Failed to fetch {url}: HTTP {status_code}")
                return {"error": f"HTTP {status_code}", "url": url}
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return {"error": str(e), "url": url}

        soup = BeautifulSoup(response_text, "html.parser")
        html_text = response_text.lower()
        clean_text = self._clean_text_for_matching(html_text)

        # Extract basic info
        title = soup.title.string.strip() if soup.title else ""

        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else ""

        if not description:
            og_desc = soup.find("meta", attrs={"property": "og:description"})
            description = og_desc["content"] if og_desc else ""

        # Detect language (after title/description are extracted)
        detected_language = "en"
        try:
            # First check <html lang> attribute
            html_tag = soup.find("html")
            if html_tag and html_tag.get("lang"):
                lang_attr = html_tag.get("lang").lower()[:2]
                if lang_attr and len(lang_attr) == 2:
                    detected_language = lang_attr
                    logger.info(f"Language from <html lang>: {detected_language}")
            # Fallback: detect from title + description + about text sample
            if detected_language == "en":
                sample_text = " ".join(filter(None, [
                    title,
                    description,
                    soup.get_text(separator=" ", strip=True)[:500],
                ]))
                if sample_text and len(sample_text) > 20:
                    detected_language = detect(sample_text)
                    logger.info(f"Language detected from text: {detected_language}")
        except Exception as e:
            logger.warning(f"Language detection failed, defaulting to en: {e}")

        # Detect technologies
        technologies = []
        tech_indicators = {
            "WordPress": "wp-content",
            "Shopify": "myshopify",
            "Squarespace": "squarespace",
            "Wix": "wix",
            "React": "react",
            "Vue": "vue",
            "Angular": "angular",
            "Stripe": "stripe",
            "PayPal": "paypal",
            "Calendly": "calendly",
            "HubSpot": "hubspot",
            "Mailchimp": "mailchimp",
            "Google Analytics": "google-analytics",
            "Facebook Pixel": "fbevents",
            "Intercom": "intercom",
            "Zendesk": "zendesk",
            "Drift": "drift",
            "Tidio": "tidio",
            "Tawk.to": "tawk",
            "Crisp": "crisp",
            "LiveChat": "livechat",
            "OpenTable": "opentable",
            "Square": "squareup",
            "Toast": "toasttab",
            "MindBody": "mindbodyonline",
        }

        for tech, indicator in tech_indicators.items():
            if indicator in clean_text:
                technologies.append(tech)

        # Detect features (use clean_text to avoid false positives from CSS/JS)
        has_chatbot = any(
            indicator in clean_text
            for indicator in ["chatbot", "livechat", "intercom", "drift", "tawk", "crisp", "tidio"]
        )

        has_booking = any(
            indicator in clean_text
            for indicator in ["book now", "schedule", "appointment", "reservation", "calendly", "autoops", "book online", "schedule service", "request appointment", "service scheduler"]
        )

        has_contact_form = bool(soup.find("form")) or "contact" in clean_text

        # Extract social links
        social_links = {}
        social_domains = {
            "facebook": "facebook.com",
            "instagram": "instagram.com",
            "twitter": "twitter.com",
            "linkedin": "linkedin.com",
            "youtube": "youtube.com",
            "tiktok": "tiktok.com",
        }

        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            for platform, domain in social_domains.items():
                if domain in href and platform not in social_links:
                    social_links[platform] = a["href"]

        # Try to find email on page
        email_found = self._extract_emails(response_text, soup)

        # If no email found, try contact page
        if not email_found:
            email_found = await self._try_contact_page(url)

        # Try to find phone on page
        phone_found = self._extract_phone(response_text, soup)

        # If no phone found, try contact page
        if not phone_found:
            phone_found = await self._try_contact_page_for_phone(url)

        # Extract services offered
        services = self._extract_services(soup)

        # Extract pricing mentions
        pricing_info = self._extract_pricing(soup, clean_text)

        # Extract business hours
        hours = self._extract_hours(soup, clean_text)

        # Extract about text
        about_text = self._extract_about(soup)

        # Extract team/owner names
        team_names = self._extract_team(soup)

        # Detect additional features
        has_ecommerce = any(
            indicator in clean_text
            for indicator in ["cart", "checkout", "shop", "product", "buy now", "add to cart"]
        )
        has_blog = any(
            indicator in clean_text
            for indicator in ["/blog", "blog.", "latest posts", "articles"]
        )
        has_newsletter = any(
            indicator in clean_text
            for indicator in ["newsletter", "subscribe", "join our list", "email list"]
        )

        # Check for online ordering / delivery
        has_online_ordering = any(
            indicator in clean_text
            for indicator in ["order online", "online ordering", "delivery", "pickup"]
        )

        return {
            "url": url,
            "title": title,
            "description": description,
            "technologies_detected": technologies,
            "has_chatbot": has_chatbot,
            "has_booking": has_booking,
            "has_contact_form": has_contact_form,
            "social_links": social_links,
            "email_found": email_found,
            "phone_found": phone_found,
            "services": services,
            "pricing_info": pricing_info,
            "hours": hours,
            "about_text": about_text,
            "team_names": team_names,
            "has_ecommerce": has_ecommerce,
            "has_blog": has_blog,
            "has_newsletter": has_newsletter,
            "has_online_ordering": has_online_ordering,
            "detected_language": detected_language,
        }

    def _extract_emails(self, text: str, soup: BeautifulSoup = None) -> Optional[str]:
        """Extract the most likely business email from page text, mailto links, and schema.org."""
        all_emails = []

        # 1. Regex from raw HTML
        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        all_emails.extend(email_pattern.findall(text))

        # 2. mailto: links
        if soup:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("mailto:"):
                    email = href.replace("mailto:", "").split("?")[0].strip()
                    if email and "@" in email:
                        all_emails.append(email)

            # 3. Schema.org JSON-LD
            import json as _json
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = _json.loads(script.string or "{}")
                    def find_emails(obj):
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                if k == "email" and isinstance(v, str) and "@" in v:
                                    all_emails.append(v)
                                elif isinstance(v, (dict, list)):
                                    find_emails(v)
                        elif isinstance(obj, list):
                            for item in obj:
                                find_emails(item)
                    find_emails(data)
                except Exception:
                    pass

        if all_emails:
            # Filter out platform / fake emails
            blocked_domains = [
                "example.com", "test.com", "domain.com", "email.com",
                "sentry.io", "sentry.com", "sentry-next.wixpress.com",
                "wixpress.com", "wix.com", "editorx.com",
                "squarespace.com", "squarespace-mail.com",
                "shopify.com", "myshopify.com",
                "weebly.com", "webflow.io", "webflow.com",
                "wordpress.com", "wp.com", "wpengine.com",
                "godaddy.com", "hostgator.com", "bluehost.com",
                "google.com", "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
                "facebook.com", "instagram.com", "twitter.com", "x.com",
                "linkedin.com", "youtube.com", "tiktok.com",
            ]
            blocked_patterns = [
                "noreply", "no-reply", "donotreply", "do-not-reply",
                "support@shopify", "support@wix", "admin@wordpress",
                "info@wordpress", "help@wordpress", "test@",
                "example@", "user@", "admin@", "postmaster@",
                "abuse@", "webmaster@", "hostmaster@",
            ]

            filtered = []
            for e in all_emails:
                e_lower = e.lower()
                if e.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
                    continue
                if any(bd in e_lower for bd in blocked_domains):
                    continue
                if any(bp in e_lower for bp in blocked_patterns):
                    continue
                filtered.append(e)

            if filtered:
                preferred_prefixes = ["info@", "contact@", "hello@", "admin@", "support@", "sales@", "booking@", "appointments@"]
                preferred = [e for e in filtered if any(e.lower().startswith(p) for p in preferred_prefixes)]
                return preferred[0] if preferred else filtered[0]
        return None

    async def _try_contact_page(self, base_url: str) -> Optional[str]:
        """Try to find email on /contact or /about pages."""
        for path in ["/contact", "/contact-us", "/about", "/about-us"]:
            try:
                url = base_url.rstrip("/") + path
                text, status = await self._fetch_html(url, timeout=10.0)
                if status == 200:
                    soup = BeautifulSoup(text, "html.parser")
                    email = self._extract_emails(text, soup)
                    if email:
                        return email
            except Exception:
                continue
        return None

    def _extract_phone(self, text: str, soup: BeautifulSoup = None) -> Optional[str]:
        """Extract the most likely business phone from page text, tel: links, and schema.org."""
        # 1. tel: links (most reliable)
        if soup:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("tel:"):
                    phone = href.replace("tel:", "").strip().replace("-", "").replace(".", "").replace("(", "").replace(")", "").replace(" ", "")
                    if len(phone) >= 10:
                        return phone

            # 2. Schema.org JSON-LD
            import json as _json
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    ld = _json.loads(script.string or "{}")
                    phones = []
                    def _find_phones(obj):
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                if k.lower() in ("telephone", "phone", "fax") and isinstance(v, str) and len(v) >= 10:
                                    phones.append(v)
                                elif isinstance(v, (dict, list)):
                                    _find_phones(v)
                        elif isinstance(obj, list):
                            for item in obj:
                                _find_phones(item)
                    _find_phones(ld)
                    if phones:
                        return phones[0].replace("-", "").replace(".", "").replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
                except Exception:
                    pass

        # 3. Regex patterns for US phone numbers
        patterns = [
            r"\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})",
            r"([0-9]{3})[.-]([0-9]{3})[.-]([0-9]{4})",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                digits = "".join(matches[0])
                if len(digits) == 10:
                    return digits
        return None

    async def _try_contact_page_for_phone(self, base_url: str) -> Optional[str]:
        """Try common contact page URLs to find a phone number."""
        from urllib.parse import urljoin
        contact_paths = ["/contact", "/contact-us", "/about", "/about-us"]
        for path in contact_paths:
            try:
                url = urljoin(base_url, path)
                text, status = await self._fetch_html(url, timeout=10.0)
                if status == 200:
                    soup = BeautifulSoup(text, "html.parser")
                    phone = self._extract_phone(text, soup)
                    if phone:
                        return phone
            except Exception:
                continue
        return None

    def _extract_services(self, soup: BeautifulSoup) -> list:
        """Try to extract list of services from common sections."""
        services = []
        # Common section headings for services
        service_keywords = ["services", "what we offer", "our services", "treatments", "menu", "pricing", "specialties"]

        for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
            text = heading.get_text(strip=True).lower()
            if any(kw in text for kw in service_keywords):
                # Look at next sibling lists or paragraphs
                next_elem = heading.find_next_sibling()
                for _ in range(5):  # Check next 5 siblings
                    if next_elem is None:
                        break
                    if next_elem.name in ["ul", "ol"]:
                        for li in next_elem.find_all("li"):
                            svc = li.get_text(strip=True)
                            if svc and len(svc) > 2:
                                services.append(svc)
                    elif next_elem.name == "div":
                        # Maybe a grid of services
                        for item in next_elem.find_all(["h3", "h4", "p", "span"]):
                            svc = item.get_text(strip=True)
                            if svc and len(svc) > 2 and len(svc) < 100:
                                services.append(svc)
                    next_elem = next_elem.find_next_sibling()

        # Deduplicate and limit
        seen = set()
        unique = []
        for s in services:
            key = s.lower()
            if key not in seen:
                seen.add(key)
                unique.append(s)
        return unique[:15]

    def _extract_pricing(self, soup: BeautifulSoup, html_text: str) -> Optional[str]:
        """Extract pricing mentions."""
        price_indicators = ["$", "price", "pricing", "cost", "rate", "from ", "starting at"]
        # Look for pricing sections
        for heading in soup.find_all(["h1", "h2", "h3"]):
            text = heading.get_text(strip=True).lower()
            if "price" in text or "menu" in text or "rates" in text:
                section_text = ""
                next_elem = heading.find_next_sibling()
                for _ in range(3):
                    if next_elem is None:
                        break
                    section_text += next_elem.get_text(separator=" ", strip=True) + " "
                    next_elem = next_elem.find_next_sibling()
                if section_text:
                    return section_text[:500].strip()
        return None

    def _extract_hours(self, soup: BeautifulSoup, html_text: str) -> Optional[str]:
        """Extract business hours if available."""
        for heading in soup.find_all(["h2", "h3", "h4", "strong", "b"]):
            text = heading.get_text(strip=True).lower()
            if "hours" in text or "open" in text or "schedule" in text:
                next_elem = heading.find_next_sibling()
                if next_elem:
                    hours_text = next_elem.get_text(separator=" ", strip=True)
                    if hours_text and len(hours_text) > 5:
                        return hours_text[:300]
        # Also check for schema.org OpeningHoursSpecification
        hours_meta = soup.find("div", class_=re.compile(r"hours|open", re.I))
        if hours_meta:
            return hours_meta.get_text(separator=" ", strip=True)[:300]
        return None

    def _extract_about(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract about us / story text."""
        for heading in soup.find_all(["h1", "h2", "h3"]):
            text = heading.get_text(strip=True).lower()
            if any(kw in text for kw in ["about us", "our story", "who we are", "about", "meet the team"]):
                section_text = ""
                next_elem = heading.find_next_sibling()
                for _ in range(4):
                    if next_elem is None:
                        break
                    section_text += next_elem.get_text(separator=" ", strip=True) + " "
                    next_elem = next_elem.find_next_sibling()
                if section_text:
                    return section_text[:800].strip()
        return None

    def _extract_team(self, soup: BeautifulSoup) -> list:
        """Extract team member or owner names."""
        names = []
        for heading in soup.find_all(["h2", "h3", "h4"]):
            text = heading.get_text(strip=True).lower()
            if any(kw in text for kw in ["team", "staff", "our people", "meet", "owner", "founder"]):
                next_elem = heading.find_next_sibling()
                for _ in range(5):
                    if next_elem is None:
                        break
                    # Look for strong/b tags with names
                    for name_tag in next_elem.find_all(["strong", "b", "h3", "h4"]):
                        name = name_tag.get_text(strip=True)
                        if name and 2 < len(name) < 40 and not any(x in name.lower() for x in ["team", "staff", "meet", "our"]):
                            names.append(name)
                    next_elem = next_elem.find_next_sibling()
        # Deduplicate
        seen = set()
        unique = []
        for n in names:
            key = n.lower()
            if key not in seen:
                seen.add(key)
                unique.append(n)
        return unique[:5]

    async def close(self):
        await self.client.aclose()
