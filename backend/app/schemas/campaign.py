from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.campaign import CampaignStatus, CampaignType


class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    campaign_type: CampaignType = CampaignType.OUTREACH
    target_city: Optional[str] = None
    target_state: Optional[str] = None
    target_categories: Optional[list] = None
    target_radius_miles: Optional[int] = Field(25, ge=1, le=100)
    min_urgency_score: Optional[float] = Field(0.0, ge=0, le=100)
    max_leads: Optional[int] = Field(None, ge=1)
    email_subject_template: Optional[str] = None
    email_body_template: Optional[str] = None
    follow_up_delay_hours: int = Field(72, ge=1)
    max_follow_ups: int = Field(3, ge=0, le=10)


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    email_subject_template: Optional[str] = None
    email_body_template: Optional[str] = None
    follow_up_delay_hours: Optional[int] = None
    max_follow_ups: Optional[int] = None


class CampaignResponse(CampaignBase):
    id: int
    status: CampaignStatus
    leads_total: int
    leads_contacted: int
    leads_responded: int
    leads_converted: int
    created_by: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CampaignLaunchRequest(BaseModel):
    campaign_id: int
    auto_enrich: bool = True
    auto_contact: bool = False
