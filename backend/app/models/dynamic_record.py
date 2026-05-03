"""Dynamic record storage for custom objects without dedicated tables."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, Boolean, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DynamicRecord(Base):
    """Generic JSONB storage for records of custom objects.

    Objects with target_table_name=None store their data here.
    Each row belongs to an object_metadata definition and stores
    all its fields in the ``data`` JSONB column.
    """

    __tablename__ = "dynamic_records"
    __table_args__ = (
        Index("ix_dynamic_records_object_id", "object_metadata_id"),
        Index("ix_dynamic_records_workspace_id", "workspace_id"),
        Index("ix_dynamic_records_label", "label"),
        Index("ix_dynamic_records_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    workspace_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True, index=True, default=None
    )

    object_metadata_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("object_metadata.id", ondelete="CASCADE"), nullable=False
    )

    # Human-readable label / title (denormalized for quick listing)
    label: Mapped[str] = mapped_column(String(500), nullable=False, default="")

    # All field values stored as JSONB
    data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    # Search vector for full-text search (populated by trigger or service)
    search_vector: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Soft delete
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
