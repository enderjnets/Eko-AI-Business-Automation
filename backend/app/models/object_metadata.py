"""Dynamic object metadata model — defines custom objects and their structure."""

import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Text, DateTime, Boolean, Integer, JSON, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ObjectMetadata(Base):
    """Metadata definition for a business object (e.g. lead, deal, custom_property)."""

    __tablename__ = "object_metadata"
    __table_args__ = (
        UniqueConstraint("name_singular", "workspace_id", name="uq_object_name_singular_workspace"),
        UniqueConstraint("name_plural", "workspace_id", name="uq_object_name_plural_workspace"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    # Workspace isolation (prepared for multi-tenancy; null = default workspace)
    workspace_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True, index=True, default=None
    )

    # Naming
    name_singular: Mapped[str] = mapped_column(String(255), nullable=False)
    name_plural: Mapped[str] = mapped_column(String(255), nullable=False)
    label_singular: Mapped[str] = mapped_column(String(255), nullable=False)
    label_plural: Mapped[str] = mapped_column(String(255), nullable=False)

    # Presentation
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Physical table name for standard objects (e.g. "leads", "deals").
    # Null means the object uses dynamic_records JSONB storage.
    target_table_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Flags
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)   # Eko AI built-in objects
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_searchable: Mapped[bool] = mapped_column(Boolean, default=True)

    # Position for menu ordering
    position: Mapped[int] = mapped_column(Integer, default=0)

    # Duplicate detection criteria (JSON array of field names)
    duplicate_criteria: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    fields: Mapped[List["FieldMetadata"]] = relationship(
        "FieldMetadata",
        back_populates="object",
        cascade="all, delete-orphan",
        lazy="selectin",
        foreign_keys="FieldMetadata.object_metadata_id",
    )
