import logging
import json
import re
import asyncio
from typing import Optional

from app.utils.ai_client import generate_completion
from app.services.landing_page_template import SYSTEM_PROMPT_TEMPLATE, render_template

logger = logging.getLogger(__name__)

# Regex to extract JSON from markdown fences or raw text
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)

# Regex to extract text from Kimi CLI --quiet output
_RESUME_SESSION_RE = re.compile(r"To resume this session:.*", re.IGNORECASE)


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
        if provider == "kimi":
            return await self._generate_copy_kimi(system, user_prompt)

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

    async def _generate_copy_kimi(self, system: str, user_prompt: str) -> str:
        """Generate copy using Kimi CLI via subprocess."""
        import shutil

        kimi_bin = shutil.which("kimi") or "/root/.local/bin/kimi"

        # Combine system prompt and user prompt into a single prompt for Kimi CLI
        full_prompt = f"""{system}

USER REQUEST:
{user_prompt}

IMPORTANT: Respond with ONLY a valid JSON object. No markdown fences, no explanations, no comments. Just pure JSON starting with {{ and ending with }}."""

        cmd = [
            kimi_bin,
            "--quiet",
            "--yolo",
            "--max-steps-per-turn", "1",
            "--prompt", full_prompt,
        ]

        logger.info(f"Running Kimi CLI: {' '.join(cmd)}")

        try:
            import os
            env = os.environ.copy()
            env["PATH"] = "/root/.local/bin:/home/enderj/.local/bin:" + env.get("PATH", "/usr/local/bin:/usr/bin:/bin")
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
        except asyncio.TimeoutError:
            logger.error("Kimi CLI timed out after 120 seconds")
            if proc.returncode is None:
                proc.kill()
            raise RuntimeError("Kimi CLI timed out after 120 seconds")
        except Exception as e:
            logger.error(f"Kimi CLI subprocess failed: {e}")
            raise RuntimeError(f"Kimi CLI subprocess failed: {e}")

        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="ignore")[:500]
            logger.error(f"Kimi CLI exited with code {proc.returncode}: {err}")
            raise RuntimeError(f"Kimi CLI failed (exit {proc.returncode}): {err}")

        output = stdout.decode("utf-8", errors="ignore")

        # Clean up output — remove "To resume this session" line
        output = _RESUME_SESSION_RE.sub("", output).strip()

        logger.info(f"Kimi CLI output length: {len(output)} chars")
        logger.debug(f"Kimi CLI raw output: {output[:500]}")

        return output

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
