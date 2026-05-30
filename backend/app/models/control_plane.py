"""Control plane models — register and monitor deployed product instances.

Eko AI Automation acts as a control plane over heterogeneous products (the first
being Eko AI Realtors). Each product is single-tenant-per-deployment, so a
"client" here is one deployed instance, not a tenant row inside a running app.

The schema is created by ``Base.metadata.create_all`` on startup (see
``app.db.base.init_db``); this module is imported in ``app.main`` so the tables
are registered. No Alembic.
"""
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, List

from sqlalchemy import String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InstanceStatus(str, PyEnum):
    ACTIVE = "active"          # registered and polled
    SUSPENDED = "suspended"    # registered but excluded from polling
    PROVISIONING = "provisioning"  # reserved for future auto-provisioning
    ERROR = "error"            # last poll failed / unreachable
    UNKNOWN = "unknown"        # never polled yet


class ActionStatus(str, PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


class Product(Base):
    """A product line managed by the control plane (e.g. realtors)."""
    __tablename__ = "cp_products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    default_ports: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Children are removed at the DB level (ondelete CASCADE); passive_deletes
    # avoids loading the whole collection during an async delete.
    instances: Mapped[List["ProductInstance"]] = relationship(
        "ProductInstance", back_populates="product",
        cascade="all, delete-orphan", passive_deletes=True,
    )


class ProductInstance(Base):
    """A single deployed instance of a product for one client."""
    __tablename__ = "cp_instances"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("cp_products.id", ondelete="CASCADE"), index=True)
    client_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Connectivity (over Tailscale)
    base_url: Mapped[str] = mapped_column(String(500), nullable=False)
    agent_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    host: Mapped[Optional[str]] = mapped_column(String(255))

    # Service-to-service credentials, encrypted at rest (Fernet). Never returned by the API.
    service_key_enc: Mapped[Optional[str]] = mapped_column(Text)
    agent_key_enc: Mapped[Optional[str]] = mapped_column(Text)

    # Billing hooks (left for a future phase — not enforced this stage)
    plan: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[InstanceStatus] = mapped_column(
        Enum(InstanceStatus), default=InstanceStatus.UNKNOWN, index=True
    )

    # Latest observability snapshot
    last_health: Mapped[Optional[dict]] = mapped_column(JSON)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # product is eager-loaded (selectin) so it is always available for
    # serialization in async routes without per-access lazy loads.
    product: Mapped["Product"] = relationship(
        "Product", back_populates="instances", lazy="selectin",
    )
    # Histories are read via explicit queries; load lazily, delete at DB level.
    health_checks: Mapped[List["InstanceHealthCheck"]] = relationship(
        "InstanceHealthCheck", back_populates="instance",
        cascade="all, delete-orphan", passive_deletes=True,
    )
    action_logs: Mapped[List["InstanceActionLog"]] = relationship(
        "InstanceActionLog", back_populates="instance",
        cascade="all, delete-orphan", passive_deletes=True,
    )


class InstanceHealthCheck(Base):
    """Historical health poll result — used for up/down timeline and SLA."""
    __tablename__ = "cp_health_checks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    instance_id: Mapped[int] = mapped_column(
        ForeignKey("cp_instances.id", ondelete="CASCADE"), index=True
    )
    ok: Mapped[bool] = mapped_column(Boolean, default=False)
    latency_ms: Mapped[Optional[float]] = mapped_column(Float)
    payload: Mapped[Optional[dict]] = mapped_column(JSON)
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )

    instance: Mapped["ProductInstance"] = relationship("ProductInstance", back_populates="health_checks")


class InstanceActionLog(Base):
    """Audit trail for remote (destructive) actions. Mandatory for every action."""
    __tablename__ = "cp_action_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    instance_id: Mapped[int] = mapped_column(
        ForeignKey("cp_instances.id", ondelete="CASCADE"), index=True
    )
    actor_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    action: Mapped[str] = mapped_column(String(50))  # restart / migrate / redeploy / logs
    status: Mapped[ActionStatus] = mapped_column(Enum(ActionStatus), default=ActionStatus.PENDING)
    output: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    instance: Mapped["ProductInstance"] = relationship("ProductInstance", back_populates="action_logs")
