from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class LandingPageAnalytics(BaseModel):
    total_visits: int = 0
    unique_visits: int = 0
    form_fills: int = 0
    email_replies: int = 0
    calls_made: int = 0
    bookings_created: int = 0
    deals_closed: int = 0
    conversion_rate: float = 0.0


class LandingPageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)
    prompt: Optional[str] = None
    html_content: str = Field(..., min_length=1)
    css_content: Optional[str] = None
    js_content: Optional[str] = None
    is_active: bool = False
    is_random_pool: bool = True
    ai_model: str = "kimi-k2.5"
    ai_provider: str = "kimi"


class LandingPageCreate(LandingPageBase):
    pass


class LandingPageUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    prompt: Optional[str] = None
    html_content: Optional[str] = None
    css_content: Optional[str] = None
    js_content: Optional[str] = None
    is_active: Optional[bool] = None
    is_random_pool: Optional[bool] = None
    ai_model: Optional[str] = None
    ai_provider: Optional[str] = None


class LandingPageResponse(LandingPageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analytics: dict
    generation_metadata: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None


class LandingPageListResponse(BaseModel):
    items: List[LandingPageResponse]
    total: int


class LandingPageGenerateRequest(BaseModel):
    prompt: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None


class LandingPagePreviewRequest(BaseModel):
    html_content: str
    css_content: Optional[str] = None
    js_content: Optional[str] = None


class LandingPageAnalyticsResponse(BaseModel):
    landing_page_id: int
    name: str
    slug: str
    analytics: LandingPageAnalytics
    time_series: List[dict]  # [{"date": "2026-05-01", "visits": 10, "form_fills": 2}, ...]
    leads: List[dict]  # [{"id": 1, "business_name": "...", "status": "...", "score": 85}, ...]
