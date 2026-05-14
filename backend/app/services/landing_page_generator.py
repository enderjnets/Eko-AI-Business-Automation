import logging
import json
import re
from typing import Optional

from app.utils.ai_client import generate_completion
from app.services.landing_page_template import SYSTEM_PROMPT_TEMPLATE, render_template

logger = logging.getLogger(__name__)

# Regex to extract JSON from markdown fences or raw text
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


class LandingPageGenerator:
    """Generate landing page HTML using a fixed template + AI-generated copy."""

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

        system_prompt = SYSTEM_PROMPT_TEMPLATE
        user_prompt = custom_prompt

        # Generate copy from AI
        raw_response = await self._generate_copy(system_prompt, user_prompt, provider)

        # Parse JSON
        copy = self._parse_json(raw_response)

        # Render template
        year = datetime.now().year
        html = render_template(copy, landing_page_id, year)

        metadata = {
            "raw_tokens_estimate": len(raw_response) // 4,
            "copy_keys": list(copy.keys()),
            "has_form": "<form" in html.lower(),
            "has_tracking_pixel": "landing-pages/track" in html,
        }

        return {
            "html_content": html,
            "css_content": None,
            "js_content": None,
            "metadata": metadata,
        }

    async def _generate_copy(self, system: str, user_prompt: str, provider: Optional[str] = None) -> str:
        """Generate copy JSON from AI with error handling."""
        try:
            raw = await generate_completion(
                system_prompt=system,
                user_prompt=user_prompt,
                model=None,
                temperature=0.7,
                max_tokens=4000,
                json_mode=False,
                provider=provider,
            )
            return raw
        except Exception as e:
            logger.error(f"AI copy generation failed: {e}")
            raise RuntimeError(f"AI copy generation failed: {e}")

    def _parse_json(self, raw: str) -> dict:
        """Extract and parse JSON from AI response."""
        raw = raw.strip()

        # Try to extract from markdown fences
        match = _JSON_FENCE_RE.search(raw)
        if match:
            raw = match.group(1).strip()

        # If wrapped in quotes, unwrap
        if raw.startswith('"') and raw.endswith('"'):
            raw = raw[1:-1]

        # Try to find JSON object boundaries
        start_idx = raw.find("{")
        end_idx = raw.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            raw = raw[start_idx:end_idx + 1]

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse failed: {e}. Raw: {raw[:500]}")
            # Return empty dict — template will use defaults
            return {}
