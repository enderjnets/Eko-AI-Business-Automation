"""Control plane admin API — register products/instances, observe health, run
audited remote actions. Mounted at /api/v1/control-plane, superuser-only.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.core.security import get_current_superadmin
from app.core.crypto import encrypt
from app.models.user import User
from app.models.control_plane import (
    Product, ProductInstance, InstanceHealthCheck, InstanceActionLog,
    InstanceStatus, ActionStatus,
)
from app.schemas.control_plane import (
    ProductCreate, ProductUpdate, ProductResponse,
    InstanceCreate, InstanceUpdate, InstanceResponse, InstanceDetailResponse,
    HealthCheckResponse, ActionLogResponse, ActionTriggerResponse,
    LogsResponse, FleetStats,
)
from app.services import control_plane_client

router = APIRouter()

VALID_ACTIONS = {"restart", "migrate", "redeploy"}


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------

def _instance_to_response(inst: ProductInstance) -> InstanceResponse:
    return InstanceResponse(
        id=inst.id,
        product_id=inst.product_id,
        product_key=inst.product.key if inst.product else None,
        product_name=inst.product.name if inst.product else None,
        client_name=inst.client_name,
        base_url=inst.base_url,
        agent_url=inst.agent_url,
        host=inst.host,
        plan=inst.plan,
        notes=inst.notes,
        status=inst.status,
        last_health=inst.last_health,
        last_seen_at=inst.last_seen_at,
        has_service_key=bool(inst.service_key_enc),
        has_agent_key=bool(inst.agent_key_enc),
        created_at=inst.created_at,
        updated_at=inst.updated_at,
    )


async def _get_instance_or_404(instance_id: int, db: AsyncSession) -> ProductInstance:
    result = await db.execute(select(ProductInstance).where(ProductInstance.id == instance_id))
    inst = result.scalar_one_or_none()
    if not inst:
        raise HTTPException(status_code=404, detail="Instance not found")
    return inst


# ---------------------------------------------------------------------------
# Fleet overview
# ---------------------------------------------------------------------------

@router.get("/stats", response_model=FleetStats)
async def fleet_stats(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    products = (await db.execute(select(func.count(Product.id)))).scalar() or 0
    total = (await db.execute(select(func.count(ProductInstance.id)))).scalar() or 0
    active = (await db.execute(
        select(func.count(ProductInstance.id)).where(ProductInstance.status == InstanceStatus.ACTIVE)
    )).scalar() or 0
    down = (await db.execute(
        select(func.count(ProductInstance.id)).where(ProductInstance.status == InstanceStatus.ERROR)
    )).scalar() or 0
    since = datetime.utcnow() - timedelta(hours=24)
    incidents = (await db.execute(
        select(func.count(InstanceHealthCheck.id))
        .where(InstanceHealthCheck.ok == False)  # noqa: E712
        .where(InstanceHealthCheck.checked_at >= since)
    )).scalar() or 0
    return FleetStats(
        products=products, instances_total=total, instances_active=active,
        instances_down=down, incidents_24h=incidents,
    )


# ---------------------------------------------------------------------------
# Products CRUD
# ---------------------------------------------------------------------------

@router.get("/products", response_model=list[ProductResponse])
async def list_products(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    result = await db.execute(select(Product).order_by(Product.name))
    products = result.scalars().all()
    out = []
    for p in products:
        count = (await db.execute(
            select(func.count(ProductInstance.id)).where(ProductInstance.product_id == p.id)
        )).scalar() or 0
        out.append(ProductResponse(
            id=p.id, key=p.key, name=p.name, description=p.description,
            default_ports=p.default_ports, created_at=p.created_at, instance_count=count,
        ))
    return out


@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    existing = (await db.execute(select(Product).where(Product.key == data.key))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail=f"Product key '{data.key}' already exists")
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return ProductResponse(
        id=product.id, key=product.key, name=product.name, description=product.description,
        default_ports=product.default_ports, created_at=product.created_at, instance_count=0,
    )


@router.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    product = (await db.execute(select(Product).where(Product.id == product_id))).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    count = (await db.execute(
        select(func.count(ProductInstance.id)).where(ProductInstance.product_id == product.id)
    )).scalar() or 0
    return ProductResponse(
        id=product.id, key=product.key, name=product.name, description=product.description,
        default_ports=product.default_ports, created_at=product.created_at, instance_count=count,
    )


@router.delete("/products/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    product = (await db.execute(select(Product).where(Product.id == product_id))).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(product)
    await db.commit()


# ---------------------------------------------------------------------------
# Instances CRUD
# ---------------------------------------------------------------------------

@router.get("/instances", response_model=list[InstanceResponse])
async def list_instances(
    product_id: Optional[int] = None,
    status: Optional[InstanceStatus] = None,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    query = select(ProductInstance)
    if product_id:
        query = query.where(ProductInstance.product_id == product_id)
    if status:
        query = query.where(ProductInstance.status == status)
    query = query.order_by(ProductInstance.client_name)
    result = await db.execute(query)
    return [_instance_to_response(i) for i in result.scalars().all()]


@router.post("/instances", response_model=InstanceResponse, status_code=201)
async def create_instance(
    data: InstanceCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    product = (await db.execute(select(Product).where(Product.id == data.product_id))).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    inst = ProductInstance(
        product_id=data.product_id,
        client_name=data.client_name,
        base_url=data.base_url,
        agent_url=data.agent_url,
        host=data.host,
        plan=data.plan,
        notes=data.notes,
        status=data.status,
        service_key_enc=encrypt(data.service_key),
        agent_key_enc=encrypt(data.agent_key),
    )
    db.add(inst)
    await db.commit()
    await db.refresh(inst, attribute_names=["product"])
    return _instance_to_response(inst)


@router.get("/instances/{instance_id}", response_model=InstanceDetailResponse)
async def get_instance(
    instance_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    inst = await _get_instance_or_404(instance_id, db)
    base = _instance_to_response(inst)
    recent = (await db.execute(
        select(InstanceHealthCheck)
        .where(InstanceHealthCheck.instance_id == instance_id)
        .order_by(desc(InstanceHealthCheck.checked_at))
        .limit(50)
    )).scalars().all()
    return InstanceDetailResponse(
        **base.model_dump(),
        recent_health=[HealthCheckResponse.model_validate(h) for h in recent],
        metrics=(inst.last_health or {}).get("metrics") if inst.last_health else None,
    )


@router.patch("/instances/{instance_id}", response_model=InstanceResponse)
async def update_instance(
    instance_id: int,
    data: InstanceUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    inst = await _get_instance_or_404(instance_id, db)
    payload = data.model_dump(exclude_unset=True)
    # Re-encrypt keys only when explicitly provided.
    if "service_key" in payload:
        inst.service_key_enc = encrypt(payload.pop("service_key"))
    if "agent_key" in payload:
        inst.agent_key_enc = encrypt(payload.pop("agent_key"))
    for field, value in payload.items():
        setattr(inst, field, value)
    await db.commit()
    await db.refresh(inst, attribute_names=["product"])
    return _instance_to_response(inst)


@router.delete("/instances/{instance_id}", status_code=204)
async def delete_instance(
    instance_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    inst = await _get_instance_or_404(instance_id, db)
    await db.delete(inst)
    await db.commit()


# ---------------------------------------------------------------------------
# Observability
# ---------------------------------------------------------------------------

@router.get("/instances/{instance_id}/health")
async def poll_health(
    instance_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    """Force an on-demand health poll and persist the result."""
    inst = await _get_instance_or_404(instance_id, db)
    result = await control_plane_client.fetch_status(inst)
    check = InstanceHealthCheck(
        instance_id=inst.id,
        ok=result.get("ok", False),
        latency_ms=result.get("latency_ms"),
        payload=result.get("payload") if result.get("ok") else {"error": result.get("error")},
    )
    db.add(check)
    inst.last_health = check.payload
    inst.last_seen_at = datetime.utcnow()
    inst.status = InstanceStatus.ACTIVE if result.get("ok") else InstanceStatus.ERROR
    await db.commit()
    return {"ok": result.get("ok", False), "latency_ms": result.get("latency_ms"),
            "payload": check.payload}


@router.get("/instances/{instance_id}/metrics")
async def instance_metrics(
    instance_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    inst = await _get_instance_or_404(instance_id, db)
    analytics = await control_plane_client.fetch_analytics(inst)
    return {"instance_id": instance_id, "metrics": analytics}


@router.get("/instances/{instance_id}/logs", response_model=LogsResponse)
async def instance_logs(
    instance_id: int,
    service: Optional[str] = None,
    lines: int = Query(200, ge=1, le=2000),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    inst = await _get_instance_or_404(instance_id, db)
    result = await control_plane_client.agent_logs(inst, service=service, lines=lines)
    return LogsResponse(
        instance_id=instance_id, service=service, lines=lines,
        output=result.get("output", ""),
        error=None if result.get("ok") else result.get("error", "agent unreachable"),
    )


# ---------------------------------------------------------------------------
# Remote actions (audited, async via Celery)
# ---------------------------------------------------------------------------

@router.post("/instances/{instance_id}/actions/{action}", response_model=ActionTriggerResponse, status_code=202)
async def trigger_action(
    instance_id: int,
    action: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superadmin),
):
    if action not in VALID_ACTIONS:
        raise HTTPException(status_code=400, detail=f"Unknown action '{action}'")
    inst = await _get_instance_or_404(instance_id, db)
    log = InstanceActionLog(
        instance_id=inst.id,
        actor_user_id=current_user.id,
        action=action,
        status=ActionStatus.PENDING,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)

    # Dispatch to Celery so migrate/redeploy never block the request.
    from app.tasks.control_plane import run_instance_action
    run_instance_action.delay(log.id, inst.id, action)

    return ActionTriggerResponse(action_id=log.id, status=log.status)


@router.get("/instances/{instance_id}/actions", response_model=list[ActionLogResponse])
async def list_actions(
    instance_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    await _get_instance_or_404(instance_id, db)
    result = await db.execute(
        select(InstanceActionLog)
        .where(InstanceActionLog.instance_id == instance_id)
        .order_by(desc(InstanceActionLog.created_at))
        .limit(limit)
    )
    return list(result.scalars().all())
