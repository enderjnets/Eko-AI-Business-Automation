"""FastAPI router for View CRUD."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.services.view_service import ViewService
from app.schemas.view import ViewCreate, ViewUpdate, ViewResponse, ViewListResponse

router = APIRouter()


def _get_workspace_id(request: Request) -> Optional[str]:
    return getattr(request.state, "workspace_id", None)


async def get_view_service(db: AsyncSession = Depends(get_db)) -> ViewService:
    return ViewService(db)


@router.get("", response_model=ViewListResponse)
async def list_views(
    request: Request,
    object_metadata_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: ViewService = Depends(get_view_service),
):
    items, total = await service.list_views(
        object_metadata_id=object_metadata_id,
        workspace_id=_get_workspace_id(request),
        limit=limit,
        offset=offset,
    )
    return ViewListResponse(total=total, items=items)


@router.get("/{view_id}", response_model=ViewResponse)
async def get_view(
    view_id: str,
    request: Request,
    service: ViewService = Depends(get_view_service),
):
    view = await service.get_view_by_id(view_id, workspace_id=_get_workspace_id(request))
    if not view:
        raise HTTPException(status_code=404, detail="View not found")
    return view


@router.post("", response_model=ViewResponse, status_code=status.HTTP_201_CREATED)
async def create_view(
    request: Request,
    object_metadata_id: str = Query(..., description="Object this view belongs to"),
    payload: ViewCreate = ...,
    service: ViewService = Depends(get_view_service),
):
    view = await service.create_view(payload, object_metadata_id, workspace_id=_get_workspace_id(request))
    return view


@router.patch("/{view_id}", response_model=ViewResponse)
async def update_view(
    view_id: str,
    payload: ViewUpdate,
    request: Request,
    service: ViewService = Depends(get_view_service),
):
    view = await service.get_view_by_id(view_id, workspace_id=_get_workspace_id(request))
    if not view:
        raise HTTPException(status_code=404, detail="View not found")
    updated = await service.update_view(view, payload)
    return updated


@router.delete("/{view_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_view(
    view_id: str,
    request: Request,
    service: ViewService = Depends(get_view_service),
):
    view = await service.get_view_by_id(view_id, workspace_id=_get_workspace_id(request))
    if not view:
        raise HTTPException(status_code=404, detail="View not found")
    await service.delete_view(view)
