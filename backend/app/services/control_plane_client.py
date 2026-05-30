"""Outbound HTTP client for talking to product instances and their host agents.

Follows the httpx async pattern of ``app.services.vapi_client``: short timeouts
for status polls, longer for remote actions, and never raising — callers get a
structured dict so the control plane degrades gracefully when an instance (or
its not-yet-built status endpoint / agent) is unreachable.
"""
import logging
import time
from typing import Any, Optional

import httpx

from app.core.crypto import decrypt
from app.models.control_plane import ProductInstance

logger = logging.getLogger(__name__)

STATUS_TIMEOUT = 5.0      # seconds — health / analytics polls
ACTION_TIMEOUT = 600.0    # seconds — migrate / redeploy can take minutes
LOGS_TIMEOUT = 30.0


def _service_headers(instance: ProductInstance) -> dict:
    key = decrypt(instance.service_key_enc) or ""
    return {"X-Control-Key": key, "Content-Type": "application/json"}


def _agent_headers(instance: ProductInstance) -> dict:
    key = decrypt(instance.agent_key_enc) or ""
    return {"X-Agent-Key": key, "Content-Type": "application/json"}


async def fetch_status(instance: ProductInstance) -> dict:
    """GET {base_url}/api/v1/admin/status. Returns {ok, latency_ms, payload|error}."""
    url = f"{instance.base_url.rstrip('/')}/api/v1/admin/status"
    started = time.monotonic()
    async with httpx.AsyncClient(timeout=STATUS_TIMEOUT) as client:
        try:
            response = await client.get(url, headers=_service_headers(instance))
            latency_ms = (time.monotonic() - started) * 1000
            response.raise_for_status()
            return {"ok": True, "latency_ms": latency_ms, "payload": response.json()}
        except httpx.HTTPStatusError as e:
            latency_ms = (time.monotonic() - started) * 1000
            return {
                "ok": False,
                "latency_ms": latency_ms,
                "error": f"HTTP {e.response.status_code}",
                "detail": e.response.text[:500],
            }
        except Exception as e:
            latency_ms = (time.monotonic() - started) * 1000
            return {"ok": False, "latency_ms": latency_ms, "error": str(e)}


async def fetch_analytics(instance: ProductInstance) -> Optional[dict]:
    """GET {base_url}/api/v1/analytics. Returns the JSON body or None on failure."""
    url = f"{instance.base_url.rstrip('/')}/api/v1/analytics"
    async with httpx.AsyncClient(timeout=STATUS_TIMEOUT) as client:
        try:
            response = await client.get(url, headers=_service_headers(instance))
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.info(f"analytics fetch failed for instance {instance.id}: {e}")
            return None


async def agent_action(instance: ProductInstance, action: str, params: Optional[dict] = None) -> dict:
    """POST {agent_url}/agent/{action}. Returns {ok, exit_code, stdout, stderr|error}."""
    if not instance.agent_url:
        return {"ok": False, "error": "instance has no agent_url configured"}
    url = f"{instance.agent_url.rstrip('/')}/agent/{action}"
    async with httpx.AsyncClient(timeout=ACTION_TIMEOUT) as client:
        try:
            response = await client.post(url, headers=_agent_headers(instance), json=params or {})
            response.raise_for_status()
            data = response.json()
            return {"ok": True, **data}
        except httpx.HTTPStatusError as e:
            return {"ok": False, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:1000]}
        except Exception as e:
            return {"ok": False, "error": str(e)}


async def agent_logs(instance: ProductInstance, service: Optional[str] = None, lines: int = 200) -> dict:
    """GET {agent_url}/agent/logs?service=&lines=. Returns {ok, output|error}."""
    if not instance.agent_url:
        return {"ok": False, "error": "instance has no agent_url configured"}
    url = f"{instance.agent_url.rstrip('/')}/agent/logs"
    params: dict[str, Any] = {"lines": lines}
    if service:
        params["service"] = service
    async with httpx.AsyncClient(timeout=LOGS_TIMEOUT) as client:
        try:
            response = await client.get(url, headers=_agent_headers(instance), params=params)
            response.raise_for_status()
            data = response.json()
            return {"ok": True, **data}
        except httpx.HTTPStatusError as e:
            return {"ok": False, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:1000]}
        except Exception as e:
            return {"ok": False, "error": str(e)}
