"""FastAPI router for FieldMetadata CRUD."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.services.metadata_service import MetadataService
from app.schemas.metadata import (
    FieldMetadataCreate,
    FieldMetadataUpdate,
    FieldMetadataResponse,
)

router = APIRouter()


async def get_metadata_service(db: AsyncSession = Depends(get_db)) -> MetadataService:
    return MetadataService(db)


def _get_workspace_id(request: Request) -> Optional[str]:
    return getattr(request.state, "workspace_id", None)


@router.get("", response_model=list[FieldMetadataResponse])
async def list_fields(
    request: Request,
    object_metadata_id: str = Query(..., description="Parent object ID"),
    include_inactive: bool = Query(False),
    service: MetadataService = Depends(get_metadata_service),
):
    """List all fields for a given object."""
    fields = await service.list_fields(
        object_metadata_id=object_metadata_id,
        workspace_id=_get_workspace_id(request),
        include_inactive=include_inactive,
    )
    return fields


@router.get("/{field_id}", response_model=FieldMetadataResponse)
async def get_field(
    field_id: str,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Get a single field metadata definition."""
    field = await service.get_field_by_id(field_id, workspace_id=_get_workspace_id(request))
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


@router.post("", response_model=FieldMetadataResponse, status_code=status.HTTP_201_CREATED)
async def create_field(
    payload: FieldMetadataCreate,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Create a new field metadata definition."""
    workspace_id = _get_workspace_id(request)
    obj = await service.get_object_by_id(payload.object_metadata_id, workspace_id=workspace_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Parent object not found")
    field = await service.create_field(payload, workspace_id=workspace_id)
    return field


@router.patch("/{field_id}", response_model=FieldMetadataResponse)
async def update_field(
    field_id: str,
    payload: FieldMetadataUpdate,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Update a field metadata definition."""
    field = await service.get_field_by_id(field_id, workspace_id=_get_workspace_id(request))
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    updated = await service.update_field(field, payload)
    return updated


@router.delete("/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(
    field_id: str,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Delete a field metadata definition."""
    field = await service.get_field_by_id(field_id, workspace_id=_get_workspace_id(request))
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    await service.delete_field(field)
