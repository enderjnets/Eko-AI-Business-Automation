from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Enum, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CampaignStatus(str, PyEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CampaignType(str, PyEnum):
    DISCOVERY = "discovery"
    OUTREACH = "outreach"
    FOLLOW_UP = "follow_up"
    REACTIVATION = "reactivation"
    REFERRAL = "referral"


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    campaign_type: Mapped[CampaignType] = mapped_column(Enum(CampaignType), default=CampaignType.OUTREACH)
    status: Mapped[CampaignStatus] = mapped_column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Targeting
    target_city: Mapped[Optional[str]] = mapped_column(String(100))
    target_state: Mapped[Optional[str]] = mapped_column(String(50))
    target_categories: Mapped[Optional[list]] = mapped_column(JSON)
    target_radius_miles: Mapped[Optional[int]] = mapped_column(Integer, default=25)
    
    # Filters
    min_urgency_score: Mapped[Optional[float]] = mapped_column(default=0.0)
    max_leads: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Content / Sequence
    email_subject_template: Mapped[Optional[str]] = mapped_column(String(500))
    email_body_template: Mapped[Optional[str]] = mapped_column(Text)
    follow_up_delay_hours: Mapped[int] = mapped_column(Integer, default=72)
    max_follow_ups: Mapped[int] = mapped_column(Integer, default=3)
    
    # Stats
    leads_total: Mapped[int] = mapped_column(Integer, default=0)
    leads_contacted: Mapped[int] = mapped_column(Integer, default=0)
    leads_responded: Mapped[int] = mapped_column(Integer, default=0)
    leads_converted: Mapped[int] = mapped_column(Integer, default=0)
    
    # Metadata
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    meta: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Timestamps
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    leads: Mapped[List["Lead"]] = relationship(
        "Lead", secondary="campaign_leads", back_populates="campaigns"
    )


class CampaignLead(Base):
    __tablename__ = "campaign_leads"
    
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id"), primary_key=True
    )
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id"), primary_key=True
    )
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, sent, responded, converted
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    follow_up_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
