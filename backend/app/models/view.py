"""View engine models — declarative views for objects (table, kanban, calendar)."""

import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Text, DateTime, Boolean, Float, ForeignKey, Index, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ViewType:
    TABLE = "table"
    KANBAN = "kanban"
    CALENDAR = "calendar"
    GALLERY = "gallery"

    ALL = [TABLE, KANBAN, CALENDAR, GALLERY]


class ViewVisibility:
    WORKSPACE = "workspace"
    PRIVATE = "private"

    ALL = [WORKSPACE, PRIVATE]


class View(Base):
    """A declarative view configuration for an object."""

    __tablename__ = "views"
    __table_args__ = (
        Index("ix_views_workspace_object", "workspace_id", "object_metadata_id"),
        Index("ix_views_visibility", "visibility"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    workspace_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True, index=True
    )

    object_metadata_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("object_metadata.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    type: Mapped[str] = mapped_column(String(50), nullable=False, default=ViewType.TABLE)
    icon: Mapped[str] = mapped_column(String(100), nullable=False, default="IconList")
    position: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_compact: Mapped[bool] = mapped_column(Boolean, default=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)

    # Kanban config
    group_by_field_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("field_metadata.id", ondelete="SET NULL"), nullable=True
    )

    # Calendar config
    calendar_field_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("field_metadata.id", ondelete="SET NULL"), nullable=True
    )

    # Visibility
    visibility: Mapped[str] = mapped_column(String(50), nullable=False, default=ViewVisibility.WORKSPACE)
    created_by_user_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    object: Mapped["ObjectMetadata"] = relationship("ObjectMetadata", lazy="joined")
    view_fields: Mapped[List["ViewField"]] = relationship(
        "ViewField", back_populates="view", cascade="all, delete-orphan", lazy="selectin"
    )
    view_filters: Mapped[List["ViewFilter"]] = relationship(
        "ViewFilter", back_populates="view", cascade="all, delete-orphan", lazy="selectin"
    )
    view_sorts: Mapped[List["ViewSort"]] = relationship(
        "ViewSort", back_populates="view", cascade="all, delete-orphan", lazy="selectin"
    )


class ViewField(Base):
    """A field visible within a view (column in table, card field in kanban)."""

    __tablename__ = "view_fields"
    __table_args__ = (
        UniqueConstraint("view_id", "field_metadata_id", name="uq_view_field"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    view_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("views.id", ondelete="CASCADE"), nullable=False
    )
    field_metadata_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("field_metadata.id", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[float] = mapped_column(Float, default=0)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    width: Mapped[Optional[int]] = mapped_column(nullable=True)  # px width for table columns

    view: Mapped["View"] = relationship("View", back_populates="view_fields")
    field: Mapped["FieldMetadata"] = relationship("FieldMetadata", lazy="joined")


class ViewFilter(Base):
    """A filter applied to a view."""

    __tablename__ = "view_filters"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    view_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("views.id", ondelete="CASCADE"), nullable=False
    )
    field_metadata_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("field_metadata.id", ondelete="CASCADE"), nullable=False
    )
    operator: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    display_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    view: Mapped["View"] = relationship("View", back_populates="view_filters")
    field: Mapped["FieldMetadata"] = relationship("FieldMetadata", lazy="joined")


class ViewSort(Base):
    """A sort applied to a view."""

    __tablename__ = "view_sorts"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    view_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("views.id", ondelete="CASCADE"), nullable=False
    )
    field_metadata_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("field_metadata.id", ondelete="CASCADE"), nullable=False
    )
    direction: Mapped[str] = mapped_column(String(10), nullable=False, default="asc")

    view: Mapped["View"] = relationship("View", back_populates="view_sorts")
    field: Mapped["FieldMetadata"] = relationship("FieldMetadata", lazy="joined")
