"""Pydantic schemas for the View Engine."""

import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# ViewField schemas
# ---------------------------------------------------------------------------

class ViewFieldBase(BaseModel):
    field_metadata_id: str
    position: float = 0
    is_visible: bool = True
    width: Optional[int] = None


class ViewFieldCreate(ViewFieldBase):
    pass


class ViewFieldUpdate(BaseModel):
    position: Optional[float] = None
    is_visible: Optional[bool] = None
    width: Optional[int] = None


class ViewFieldResponse(ViewFieldBase):
    id: str
    view_id: str

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# ViewFilter schemas
# ---------------------------------------------------------------------------

class ViewFilterBase(BaseModel):
    field_metadata_id: str
    operator: str
    value: Optional[dict] = None
    display_value: Optional[str] = None


class ViewFilterCreate(ViewFilterBase):
    pass


class ViewFilterUpdate(BaseModel):
    operator: Optional[str] = None
    value: Optional[dict] = None
    display_value: Optional[str] = None


class ViewFilterResponse(ViewFilterBase):
    id: str
    view_id: str

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# ViewSort schemas
# ---------------------------------------------------------------------------

class ViewSortBase(BaseModel):
    field_metadata_id: str
    direction: str = "asc"


class ViewSortCreate(ViewSortBase):
    pass


class ViewSortUpdate(BaseModel):
    direction: Optional[str] = None


class ViewSortResponse(ViewSortBase):
    id: str
    view_id: str

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# View schemas
# ---------------------------------------------------------------------------

class ViewBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(default="table")
    icon: str = Field(default="IconList")
    position: float = 0
    is_default: bool = False
    is_compact: bool = False
    group_by_field_id: Optional[str] = None
    calendar_field_id: Optional[str] = None
    visibility: str = Field(default="workspace")


class ViewCreate(ViewBase):
    view_fields: Optional[List[ViewFieldCreate]] = []
    view_filters: Optional[List[ViewFilterCreate]] = []
    view_sorts: Optional[List[ViewSortCreate]] = []


class ViewUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    icon: Optional[str] = None
    position: Optional[float] = None
    is_default: Optional[bool] = None
    is_compact: Optional[bool] = None
    group_by_field_id: Optional[str] = None
    calendar_field_id: Optional[str] = None
    visibility: Optional[str] = None


class ViewResponse(ViewBase):
    id: str
    workspace_id: Optional[str] = None
    object_metadata_id: str
    is_system: bool
    created_by_user_id: Optional[int] = None
    view_fields: List[ViewFieldResponse] = []
    view_filters: List[ViewFilterResponse] = []
    view_sorts: List[ViewSortResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ViewListResponse(BaseModel):
    total: int
    items: List[ViewResponse]
