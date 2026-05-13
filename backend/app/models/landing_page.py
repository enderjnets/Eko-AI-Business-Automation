from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Boolean, DateTime, Integer, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LandingPage(Base):
    """Landing page variants managed via the dashboard."""

    __tablename__ = "landing_pages"

    __table_args__ = (
        Index("ix_landing_pages_workspace_id", "workspace_id"),
        Index("ix_landing_pages_is_active", "is_active"),
        Index("ix_landing_pages_is_random_pool", "is_random_pool"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workspace_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("workspaces.id"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    html_content: Mapped[str] = mapped_column(Text, nullable=False)
    css_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    js_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_random_pool: Mapped[bool] = mapped_column(Boolean, default=True)
    ai_model: Mapped[str] = mapped_column(String(50), default="kimi-k2.5")
    ai_provider: Mapped[str] = mapped_column(String(20), default="kimi")
    generation_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    analytics: Mapped[dict] = mapped_column(
        JSON,
        default=lambda: {
            "total_visits": 0,
            "unique_visits": 0,
            "form_fills": 0,
            "email_replies": 0,
            "calls_made": 0,
            "bookings_created": 0,
            "deals_closed": 0,
        },
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
