"""Pydantic schemas for the metadata engine (ObjectMetadata + FieldMetadata)."""

import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator

from app.models.field_metadata import FieldType


# ---------------------------------------------------------------------------
# FieldMetadata schemas
# ---------------------------------------------------------------------------

class FieldMetadataBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    label: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = None
    default_value: Optional[dict] = None
    options: Optional[list] = None
    settings: Optional[dict] = None
    is_custom: bool = False
    is_system: bool = False
    is_active: bool = True
    is_nullable: bool = True
    is_unique: bool = False
    is_read_only: bool = False
    is_label_field: bool = False
    position: int = 0
    relation_target_object_id: Optional[str] = None
    relation_target_field_id: Optional[str] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v.upper() not in FieldType.ALL:
            raise ValueError(f"Invalid field type: {v}. Must be one of {FieldType.ALL}")
        return v.upper()


class FieldMetadataCreate(FieldMetadataBase):
    object_metadata_id: str


class FieldMetadataUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    default_value: Optional[dict] = None
    options: Optional[list] = None
    settings: Optional[dict] = None
    is_active: Optional[bool] = None
    is_nullable: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_read_only: Optional[bool] = None
    is_label_field: Optional[bool] = None
    position: Optional[int] = None
    relation_target_object_id: Optional[str] = None
    relation_target_field_id: Optional[str] = None


class FieldMetadataResponse(FieldMetadataBase):
    id: str
    object_metadata_id: str
    workspace_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# ObjectMetadata schemas
# ---------------------------------------------------------------------------

class ObjectMetadataBase(BaseModel):
    name_singular: str = Field(..., min_length=1, max_length=255)
    name_plural: str = Field(..., min_length=1, max_length=255)
    label_singular: str = Field(..., min_length=1, max_length=255)
    label_plural: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    target_table_name: Optional[str] = None
    is_custom: bool = False
    is_system: bool = False
    is_active: bool = True
    is_searchable: bool = True
    position: int = 0
    duplicate_criteria: Optional[list] = None


class ObjectMetadataCreate(ObjectMetadataBase):
    fields: Optional[List[FieldMetadataCreate]] = []


class ObjectMetadataUpdate(BaseModel):
    label_singular: Optional[str] = None
    label_plural: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None
    is_searchable: Optional[bool] = None
    position: Optional[int] = None
    duplicate_criteria: Optional[list] = None


class ObjectMetadataResponse(ObjectMetadataBase):
    id: str
    workspace_id: Optional[str] = None
    fields: List[FieldMetadataResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ObjectMetadataListResponse(BaseModel):
    total: int
    items: List[ObjectMetadataResponse]


# ---------------------------------------------------------------------------
# DynamicRecord schemas
# ---------------------------------------------------------------------------

class DynamicRecordCreate(BaseModel):
    label: str = Field(..., min_length=1, max_length=500)
    data: dict = Field(default_factory=dict)


class DynamicRecordUpdate(BaseModel):
    label: Optional[str] = None
    data: Optional[dict] = None


class DynamicRecordResponse(BaseModel):
    id: str
    workspace_id: Optional[str] = None
    object_metadata_id: str
    label: str
    data: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DynamicRecordListResponse(BaseModel):
    total: int
    items: List[DynamicRecordResponse]
