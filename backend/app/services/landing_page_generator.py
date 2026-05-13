import logging
import re
from typing import Optional

from app.utils.ai_client import generate_completion

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are an expert web designer. Generate ONE compact, complete landing page as a single self-contained HTML file with inline CSS in a <style> block.

REQUIREMENTS:
- EXACTLY 4 sections: (1) Hero with inline lead form, (2) Features/Benefits (3-4 cards max), (3) Social proof (1-2 short testimonials), (4) Footer with CTA
- Hero form fields: name, email, phone, website, city, state. POST to /api/v1/leads/public with hidden field: <input type="hidden" name="source" value="landing_page" />
- Dark mode with blue (#0B4FD8) and cyan (#22D3EE) accents
- Minimal CSS: use simple selectors, avoid nested rules, no verbose comments
- CRITICAL: Use ONLY CSS @keyframes with animation-fill-mode:forwards. NEVER use classes that require JS to add .visible. All content visible immediately.
- Tracking pixel: <img src="/api/v1/landing-pages/track?lp_id={landing_page_id}" width="1" height="1" style="position:absolute;visibility:hidden;" />
- Mobile-first responsive. No external JS.
- Real content, no placeholders.

BUSINESS CONTEXT:
- Service: Eko AI — 24/7 AI agent for local businesses (calls, WhatsApp, emails, bookings, follow-ups)
- Target: Local business owners (restaurants, clinics, spas, gyms, retail, professionals)
- Main CTA: "Get My Free AI Analysis"
- Cal.com link: {cal_com_link}

COMPACT CODE: Use efficient CSS, avoid verbose comments and unnecessary whitespace. The complete HTML must fit within 7000 tokens.

OUTPUT FORMAT:
Return ONLY raw HTML. No markdown fences, no explanations, no comments outside HTML. Start with <!DOCTYPE html> and end with </html>."""

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

# Elements that must appear at the END (completeness check)
_CLOSING_ELEMENTS = ["</body>", "</html>"]


class LandingPageGenerator:
    """Generate landing page HTML using AI."""

    async def generate(
        self,
        custom_prompt: str,
        landing_page_id: int,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        cal_com_link: Optional[str] = None,
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
        system = system.replace("{cal_com_link}", cal_com_link or "https://cal.com/ender-ocando-lfxtkn/15min")

        # First generation attempt
        raw_html = await self._generate_html(system, user_prompt)
        html = self._extract_html(raw_html)

        # Validate structure
        validation_errors = self._validate_html(html)

        # If truncated, attempt continuation
        continuation_attempts = 0
        max_continuations = 2
        while any("incomplete html" in e.lower() for e in validation_errors) and continuation_attempts < max_continuations:
            continuation_attempts += 1
            logger.warning(f"[LP-{landing_page_id}] HTML incomplete ({validation_errors}), attempting continuation #{continuation_attempts}")
            try:
                tail = html[-2000:] if len(html) > 2000 else html
                cont_prompt = f"Continue this HTML from exactly where it was cut off. Do not repeat any already-generated content. Output ONLY the continuation, ending with </html>.\n\nLAST 2000 CHARS:\n{tail}"
                cont_raw = await generate_completion(
                    system_prompt="You are a code completion assistant. Continue the HTML exactly from where it was cut off. Output ONLY raw HTML continuation, no explanations.",
                    user_prompt=cont_prompt,
                    model=None,
                    temperature=0.3,
                    max_tokens=8192,
                    json_mode=False,
                )
                cont_html = self._extract_html(cont_raw)
                logger.info(f"[LP-{landing_page_id}] Continuation #{continuation_attempts} received {len(cont_html)} chars")
                # Remove duplicate overlap
                html = self._merge_continuation(html, cont_html)
                validation_errors = self._validate_html(html)
                logger.info(f"[LP-{landing_page_id}] After merge: {len(html)} chars, errors: {validation_errors}")
            except Exception as e:
                logger.error(f"[LP-{landing_page_id}] Continuation attempt {continuation_attempts} failed: {e}")
                break

        if validation_errors:
            logger.warning(f"Generated HTML validation issues: {validation_errors}")

        # Split into HTML/CSS/JS parts
        parts = self._split_parts(html)

        metadata = {
            "raw_tokens_estimate": len(raw_html) // 4,
            "validation_errors": validation_errors,
            "has_form": "<form" in html.lower(),
            "has_tracking_pixel": "landing-pages/track" in html,
            "continuation_attempts": continuation_attempts,
        }

        return {
            "html_content": parts["html"],
            "css_content": parts.get("css"),
            "js_content": parts.get("js"),
            "metadata": metadata,
        }

    async def _generate_html(self, system: str, user_prompt: str) -> str:
        """Generate HTML from AI with error handling."""
        try:
            raw_html = await generate_completion(
                system_prompt=system,
                user_prompt=user_prompt,
                model=None,
                temperature=0.7,
                max_tokens=8192,
                json_mode=False,
            )
            return raw_html
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            raise RuntimeError(f"AI generation failed: {e}")

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

    def _merge_continuation(self, original: str, continuation: str) -> str:
        """Merge continuation HTML with original, removing duplicate overlap."""
        original = original.strip()
        continuation = continuation.strip()
        # If continuation already contains the full HTML, use it
        if continuation.lower().startswith(("<!doctype", "<html")):
            # Find where original ends in continuation
            orig_tail = original[-500:].lower()
            cont_lower = continuation.lower()
            idx = cont_lower.find(orig_tail)
            if idx != -1:
                return original + continuation[idx + len(orig_tail):]
            return continuation
        # Continuation is just the tail — append directly
        return original + "\n" + continuation

    def _validate_html(self, html: str) -> list:
        """Check for required elements and completeness."""
        errors = []
        lower = html.lower()
        for elem in _REQUIRED_ELEMENTS:
            if elem.lower() not in lower:
                errors.append(f"Missing: {elem}")
        # Check HTML is complete (not truncated)
        for closing in _CLOSING_ELEMENTS:
            if not lower.rstrip().endswith(closing):
                # Also allow trailing whitespace after the closing tag
                stripped = lower.rstrip()
                if not any(stripped.endswith(c) for c in _CLOSING_ELEMENTS):
                    errors.append(f"Incomplete HTML: does not end with {closing}")
                    break
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
