"""Control plane Celery tasks: periodic health poller + async remote actions.

Sync Celery tasks wrap async coroutines via asyncio.run(), using
AsyncSessionLocal for DB access — the same pattern as app.tasks.scheduled.
"""
import asyncio
import logging
from datetime import datetime

from sqlalchemy import select

from app.tasks.celery_app import celery_app
from app.db.base import AsyncSessionLocal
from app.config import get_settings
from app.models.user import User  # noqa: F401 - needed for InstanceActionLog FK mapper
from app.models.control_plane import (
    ProductInstance, InstanceHealthCheck, InstanceActionLog,
    InstanceStatus, ActionStatus,
)
from app.services import control_plane_client
from app.services.eko_rog_notifier import notify_eko_rog

settings = get_settings()
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Poller
# ---------------------------------------------------------------------------

async def _poll_instances_async() -> dict:
    polled = 0
    transitions_down = 0
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(ProductInstance)
            .where(ProductInstance.status.in_([InstanceStatus.ACTIVE, InstanceStatus.ERROR, InstanceStatus.UNKNOWN]))
        )
        instances = result.scalars().all()

        for inst in instances:
            prev_status = inst.status
            status_result = await control_plane_client.fetch_status(inst)
            ok = status_result.get("ok", False)
            payload = status_result.get("payload") if ok else {"error": status_result.get("error")}

            # Enrich with funnel metrics when reachable.
            if ok:
                analytics = await control_plane_client.fetch_analytics(inst)
                if analytics is not None:
                    payload = {**(payload or {}), "metrics": analytics}

            db.add(InstanceHealthCheck(
                instance_id=inst.id,
                ok=ok,
                latency_ms=status_result.get("latency_ms"),
                payload=payload,
            ))
            inst.last_health = payload
            inst.last_seen_at = datetime.utcnow()
            inst.status = InstanceStatus.ACTIVE if ok else InstanceStatus.ERROR
            polled += 1

            # Alert only on the healthy -> down transition (avoid repeat spam).
            if not ok and prev_status != InstanceStatus.ERROR:
                transitions_down += 1
                await notify_eko_rog(
                    f"<b>🔴 Instance down</b>\n\n"
                    f"<b>Client:</b> {inst.client_name}\n"
                    f"<b>Product:</b> {inst.product.key if inst.product else inst.product_id}\n"
                    f"<b>URL:</b> {inst.base_url}\n"
                    f"<b>Error:</b> {status_result.get('error', 'unreachable')}"
                )

        await db.commit()
    return {"polled": polled, "transitions_down": transitions_down}


@celery_app.task
def poll_instances():
    """Periodic task: poll health + metrics for all monitored instances."""
    if not settings.CONTROL_PLANE_ENABLED:
        logger.info("[ControlPlane] polling disabled, skipping")
        return {"skipped": True}
    logger.info("[ControlPlane] polling instances...")
    try:
        result = asyncio.run(_poll_instances_async())
        logger.info(f"[ControlPlane] poll complete: {result}")
        return result
    except Exception as e:
        logger.error(f"[ControlPlane] poll failed: {e}")
        raise


# ---------------------------------------------------------------------------
# Remote actions
# ---------------------------------------------------------------------------

async def _run_action_async(action_id: int, instance_id: int, action: str) -> dict:
    async with AsyncSessionLocal() as db:
        log = (await db.execute(
            select(InstanceActionLog).where(InstanceActionLog.id == action_id)
        )).scalar_one_or_none()
        inst = (await db.execute(
            select(ProductInstance).where(ProductInstance.id == instance_id)
        )).scalar_one_or_none()
        if not log or not inst:
            logger.error(f"[ControlPlane] action {action_id}/instance {instance_id} not found")
            return {"ok": False, "error": "not found"}

        log.status = ActionStatus.RUNNING
        await db.commit()

        result = await control_plane_client.agent_action(inst, action)

        ok = result.get("ok", False)
        log.status = ActionStatus.SUCCESS if ok else ActionStatus.ERROR
        if ok:
            exit_code = result.get("exit_code")
            log.output = (
                f"exit_code={exit_code}\n"
                f"--- stdout ---\n{result.get('stdout', '')}\n"
                f"--- stderr ---\n{result.get('stderr', '')}"
            )
            # A non-zero exit code from the agent still means the action failed.
            if exit_code not in (0, None):
                log.status = ActionStatus.ERROR
        else:
            log.output = result.get("error", "agent unreachable")
            if result.get("detail"):
                log.output += f"\n{result['detail']}"
        await db.commit()
        return {"ok": log.status == ActionStatus.SUCCESS, "action_id": action_id}


@celery_app.task
def run_instance_action(action_id: int, instance_id: int, action: str):
    """Execute a remote action via the host agent and record the audited result."""
    logger.info(f"[ControlPlane] running action '{action}' on instance {instance_id} (log {action_id})")
    try:
        return asyncio.run(_run_action_async(action_id, instance_id, action))
    except Exception as e:
        logger.error(f"[ControlPlane] action {action_id} failed: {e}")
        raise
