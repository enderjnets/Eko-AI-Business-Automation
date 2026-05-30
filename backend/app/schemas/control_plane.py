"""Pydantic schemas for the control plane API.

Response models intentionally never expose the encrypted key columns
(``service_key_enc`` / ``agent_key_enc``). Keys are write-only.
"""
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field

from app.models.control_plane import InstanceStatus, ActionStatus


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

class ProductBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    default_ports: Optional[dict] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    default_ports: Optional[dict] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    instance_count: int = 0

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Instances
# ---------------------------------------------------------------------------

class InstanceBase(BaseModel):
    client_name: str = Field(..., min_length=1, max_length=255)
    base_url: str = Field(..., min_length=1, max_length=500)
    agent_url: Optional[str] = None
    host: Optional[str] = None
    plan: Optional[str] = None
    notes: Optional[str] = None


class InstanceCreate(InstanceBase):
    product_id: int
    # Plaintext keys on write only — encrypted before storage, never echoed back.
    service_key: Optional[str] = None
    agent_key: Optional[str] = None
    status: InstanceStatus = InstanceStatus.ACTIVE


class InstanceUpdate(BaseModel):
    client_name: Optional[str] = None
    base_url: Optional[str] = None
    agent_url: Optional[str] = None
    host: Optional[str] = None
    plan: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[InstanceStatus] = None
    service_key: Optional[str] = None
    agent_key: Optional[str] = None


class InstanceResponse(InstanceBase):
    id: int
    product_id: int
    product_key: Optional[str] = None
    product_name: Optional[str] = None
    status: InstanceStatus
    last_health: Optional[dict] = None
    last_seen_at: Optional[datetime] = None
    has_service_key: bool = False
    has_agent_key: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    id: int
    ok: bool
    latency_ms: Optional[float] = None
    payload: Optional[dict] = None
    checked_at: datetime

    class Config:
        from_attributes = True


class InstanceDetailResponse(InstanceResponse):
    recent_health: list[HealthCheckResponse] = []
    metrics: Optional[dict] = None


class ActionLogResponse(BaseModel):
    id: int
    instance_id: int
    actor_user_id: Optional[int] = None
    action: str
    status: ActionStatus
    output: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionTriggerResponse(BaseModel):
    action_id: int
    status: ActionStatus


class LogsResponse(BaseModel):
    instance_id: int
    service: Optional[str] = None
    lines: int
    output: str
    error: Optional[str] = None


class FleetStats(BaseModel):
    products: int
    instances_total: int
    instances_active: int
    instances_down: int
    incidents_24h: int
