import logging
import re
from typing import Optional

from app.utils.ai_client import generate_completion

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are an expert web designer and conversion copywriter specializing in landing pages for local businesses.

Your task is to generate ONE complete, modern, responsive landing page in a single HTML file with inline CSS (Tailwind-like utility classes inside a <style> block).

CRITICAL RULES:
1. The HTML must be a SINGLE self-contained file (inline CSS in <style>)
2. Must include: hero section, features/benefits, social proof, lead capture form (name, email, phone, website, city, state), CTA, optional FAQ
3. Modern aesthetic: dark mode with blue (#0B4FD8) and cyan (#22D3EE) accents, clean typography
4. Subtle CSS animations (fade-in, slide-up on scroll)
5. The form must POST to /api/v1/leads/public with fields: business_name, email, phone, website, city, state
6. Include hidden field: <input type="hidden" name="source" value="landing_page" />
7. Include tracking pixel: <img src="/api/v1/landing-pages/track?lp_id={landing_page_id}" width="1" height="1" style="position:absolute;visibility:hidden;" />
8. Responsive: mobile-first
9. NO external JavaScript (only inline if necessary)
10. The HTML must be ready to serve directly (real content, no placeholders)

BUSINESS CONTEXT:
- Service: Eko AI — AI agent for local businesses (answers calls, WhatsApp, emails, books appointments, follow-ups)
- Target: Local business owners (restaurants, clinics, spas, gyms, retail, professionals)
- Value prop: Never lose a customer to a missed call. Your AI works 24/7.
- Main CTA: "Get My Free AI Analysis"
- Cal.com link: https://cal.com/ender-ocando-lfxtkn/15min

OUTPUT FORMAT:
Return ONLY the raw HTML code. No markdown fences, no explanations, no comments outside the HTML. Start directly with <!DOCTYPE html>."""

# Prompt template for user input
_USER_PROMPT_TEMPLATE = """Generate a high-converting landing page for Eko AI with the following custom instructions:

{custom_prompt}

Additional requirements:
- Business name in hero: "Eko AI"
- Tagline should emphasize 24/7 automation
- Form title: "Get Your Free AI Analysis"
- Include 3-5 industry-specific benefits
- Footer with contact email: contact@biz.ekoaiautomation.com
- Current year: {year}
"""

# Regex to extract HTML from markdown fences
_HTML_FENCE_RE = re.compile(r"```(?:html)?\s*(.*?)\s*```", re.DOTALL)

# Elements to validate
_REQUIRED_ELEMENTS = [
    "<form",
    "business_name",
    "email",
    "phone",
    "city",
    "state",
    "</form>",
    "<button",
    "</button>",
    "<!DOCTYPE html",
    "</html>",
]


class LandingPageGenerator:
    """Generate landing page HTML using AI."""

    async def generate(
        self,
        custom_prompt: str,
        landing_page_id: int,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> dict:
        """Generate a landing page from a user prompt.

        Returns:
            dict with keys: html_content, css_content, js_content, metadata
        """
        from datetime import datetime

        user_prompt = _USER_PROMPT_TEMPLATE.format(
            custom_prompt=custom_prompt,
            year=datetime.now().year,
        )

        system = _SYSTEM_PROMPT.replace("{landing_page_id}", str(landing_page_id))

        try:
            raw_html = await generate_completion(
                system_prompt=system,
                user_prompt=user_prompt,
                model=model,
                temperature=0.7,
                max_tokens=8000,
                json_mode=False,
            )
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            raise RuntimeError(f"AI generation failed: {e}")

        # Extract HTML from markdown fences if present
        html = self._extract_html(raw_html)

        # Validate structure
        validation_errors = self._validate_html(html)
        if validation_errors:
            logger.warning(f"Generated HTML validation issues: {validation_errors}")

        # Split into HTML/CSS/JS parts
        parts = self._split_parts(html)

        metadata = {
            "raw_tokens_estimate": len(raw_html) // 4,
            "validation_errors": validation_errors,
            "has_form": "<form" in html.lower(),
            "has_tracking_pixel": "landing-pages/track" in html,
        }

        return {
            "html_content": parts["html"],
            "css_content": parts.get("css"),
            "js_content": parts.get("js"),
            "metadata": metadata,
        }

    def _extract_html(self, raw: str) -> str:
        """Extract HTML from markdown fences or return raw if no fences."""
        raw = raw.strip()
        match = _HTML_FENCE_RE.search(raw)
        if match:
            return match.group(1).strip()
        # If raw starts with <!DOCTYPE or <html, use it directly
        if raw.lower().startswith(("<!doctype", "<html")):
            return raw
        # Otherwise wrap in html if it looks like body content
        if "<body" not in raw.lower() and "<div" in raw.lower():
            return f"<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"/><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/><title>Eko AI</title></head>\n<body>\n{raw}\n</body>\n</html>"
        return raw

    def _validate_html(self, html: str) -> list:
        """Check for required elements."""
        errors = []
        lower = html.lower()
        for elem in _REQUIRED_ELEMENTS:
            if elem.lower() not in lower:
                errors.append(f"Missing: {elem}")
        return errors

    def _split_parts(self, html: str) -> dict:
        """Split combined HTML into html/css/js parts."""
        result = {"html": html}

        # Extract CSS from <style> blocks
        css_blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
        if css_blocks:
            result["css"] = "\n\n".join(css_blocks)
            # Remove style blocks from html (keep them inline for now)
            # We'll keep the original html intact since the frontend may want the full file
            pass

        # Extract JS from <script> blocks
        js_blocks = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL | re.IGNORECASE)
        if js_blocks:
            result["js"] = "\n\n".join(js_blocks)

        return result
