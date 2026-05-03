"""Dynamic field metadata model — defines fields within an object."""

import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Text, DateTime, Boolean, Integer, JSON, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FieldType:
    """Supported field types for dynamic objects."""

    TEXT = "TEXT"
    NUMBER = "NUMBER"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    URL = "URL"
    DATE = "DATE"
    DATE_TIME = "DATE_TIME"
    BOOLEAN = "BOOLEAN"
    SELECT = "SELECT"
    MULTI_SELECT = "MULTI_SELECT"
    JSON = "JSON"
    RICH_TEXT = "RICH_TEXT"
    CURRENCY = "CURRENCY"
    RELATION = "RELATION"
    VECTOR = "VECTOR"          # pgvector embedding field

    ALL = [
        TEXT, NUMBER, EMAIL, PHONE, URL, DATE, DATE_TIME,
        BOOLEAN, SELECT, MULTI_SELECT, JSON, RICH_TEXT,
        CURRENCY, RELATION, VECTOR,
    ]


class FieldMetadata(Base):
    """Metadata definition for a field within an object."""

    __tablename__ = "field_metadata"
    __table_args__ = (
        UniqueConstraint(
            "object_metadata_id", "name", "workspace_id",
            name="uq_field_name_object_workspace"
        ),
        Index("ix_field_metadata_object_id", "object_metadata_id"),
        Index("ix_field_metadata_workspace_id", "workspace_id"),
        Index("ix_field_metadata_type", "type"),
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

    # Field identity
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Configuration
    default_value: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    options: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)       # for SELECT / MULTI_SELECT
    settings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)      # e.g. {decimals: 2, currency: "USD"}

    # Constraints
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_nullable: Mapped[bool] = mapped_column(Boolean, default=True)
    is_unique: Mapped[bool] = mapped_column(Boolean, default=False)
    is_read_only: Mapped[bool] = mapped_column(Boolean, default=False)
    is_label_field: Mapped[bool] = mapped_column(Boolean, default=False)       # used as display name

    # Position for form/table ordering
    position: Mapped[int] = mapped_column(Integer, default=0)

    # Relation configuration (for RELATION type)
    relation_target_object_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("object_metadata.id", ondelete="SET NULL"), nullable=True
    )
    relation_target_field_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    object: Mapped["ObjectMetadata"] = relationship(
        "ObjectMetadata",
        back_populates="fields",
        lazy="joined",
        foreign_keys=[object_metadata_id],
    )
    target_object: Mapped[Optional["ObjectMetadata"]] = relationship(
        "ObjectMetadata",
        foreign_keys=[relation_target_object_id],
        lazy="joined",
    )
