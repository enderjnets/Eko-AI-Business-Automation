from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LandingPageVisit(Base):
    """Time-series tracking of visits to public landing pages."""

    __tablename__ = "landing_page_visits"

    __table_args__ = (
        Index("ix_landing_page_visits_lp_id_created", "landing_page_id", "created_at"),
        Index("ix_landing_page_visits_session", "session_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    landing_page_id: Mapped[int] = mapped_column(
        ForeignKey("landing_pages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    ip_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    referrer: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    converted_to_lead: Mapped[bool] = mapped_column(Boolean, default=False)
    lead_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("leads.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
