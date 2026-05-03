"""Pydantic schemas for Workspace and WorkspaceMember."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class WorkspaceMemberBase(BaseModel):
    role: str = "member"
    is_active: bool = True


class WorkspaceMemberCreate(WorkspaceMemberBase):
    user_id: int


class WorkspaceMemberResponse(WorkspaceMemberBase):
    id: int
    workspace_id: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    plan: str = "free"
    settings: dict = Field(default_factory=dict)
    is_active: bool = True


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    plan: Optional[str] = None
    settings: Optional[dict] = None
    is_active: Optional[bool] = None
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None


class WorkspaceResponse(WorkspaceBase):
    id: str
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    members: List[WorkspaceMemberResponse] = []

    class Config:
        from_attributes = True


class WorkspaceListResponse(BaseModel):
    total: int
    items: List[WorkspaceResponse]


class WorkspaceInviteRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    role: str = "member"
