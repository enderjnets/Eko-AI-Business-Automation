"""FastAPI router for ObjectMetadata CRUD."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.services.metadata_service import MetadataService
from app.schemas.metadata import (
    ObjectMetadataCreate,
    ObjectMetadataUpdate,
    ObjectMetadataResponse,
    ObjectMetadataListResponse,
)

router = APIRouter()


async def get_metadata_service(db: AsyncSession = Depends(get_db)) -> MetadataService:
    return MetadataService(db)


def _get_workspace_id(request: Request) -> Optional[str]:
    return getattr(request.state, "workspace_id", None)


@router.get("", response_model=ObjectMetadataListResponse)
async def list_objects(
    request: Request,
    include_inactive: bool = Query(False),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: MetadataService = Depends(get_metadata_service),
):
    """List all object metadata definitions."""
    workspace_id = _get_workspace_id(request)
    items, total = await service.list_objects(
        workspace_id=workspace_id,
        include_inactive=include_inactive,
        limit=limit,
        offset=offset,
    )
    return ObjectMetadataListResponse(total=total, items=items)


@router.get("/{object_id}", response_model=ObjectMetadataResponse)
async def get_object(
    object_id: str,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Get a single object metadata definition by ID."""
    workspace_id = _get_workspace_id(request)
    obj = await service.get_object_by_id(object_id, workspace_id=workspace_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj


@router.get("/by-name/{name}", response_model=ObjectMetadataResponse)
async def get_object_by_name(
    name: str,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Get a single object metadata definition by name (singular or plural)."""
    workspace_id = _get_workspace_id(request)
    obj = await service.get_object_by_name(name, workspace_id=workspace_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj


@router.post("", response_model=ObjectMetadataResponse, status_code=status.HTTP_201_CREATED)
async def create_object(
    payload: ObjectMetadataCreate,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Create a new object metadata definition."""
    workspace_id = _get_workspace_id(request)
    existing = await service.get_object_by_name(
        payload.name_singular, workspace_id=workspace_id
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Object '{payload.name_singular}' already exists",
        )
    obj = await service.create_object(payload, workspace_id=workspace_id)
    return obj


@router.patch("/{object_id}", response_model=ObjectMetadataResponse)
async def update_object(
    object_id: str,
    payload: ObjectMetadataUpdate,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Update an object metadata definition."""
    workspace_id = _get_workspace_id(request)
    obj = await service.get_object_by_id(object_id, workspace_id=workspace_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    updated = await service.update_object(obj, payload)
    return updated


@router.delete("/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_object(
    object_id: str,
    request: Request,
    service: MetadataService = Depends(get_metadata_service),
):
    """Delete an object metadata definition (cascades to fields)."""
    workspace_id = _get_workspace_id(request)
    obj = await service.get_object_by_id(object_id, workspace_id=workspace_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    await service.delete_object(obj)
