"""FastAPI router for generic CRUD on dynamic records."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.services.metadata_service import MetadataService
from app.services.dynamic_data_service import DynamicDataService
from app.schemas.metadata import (
    DynamicRecordCreate,
    DynamicRecordUpdate,
    DynamicRecordResponse,
    DynamicRecordListResponse,
)

router = APIRouter()


def _get_workspace_id(request: Request) -> Optional[str]:
    return getattr(request.state, "workspace_id", None)


async def get_dynamic_service(db: AsyncSession = Depends(get_db)) -> DynamicDataService:
    return DynamicDataService(db)


async def get_metadata_service(db: AsyncSession = Depends(get_db)) -> MetadataService:
    return MetadataService(db)


@router.get("/{object_name}", response_model=DynamicRecordListResponse)
async def list_records(
    object_name: str,
    request: Request,
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    meta_service: MetadataService = Depends(get_metadata_service),
    data_service: DynamicDataService = Depends(get_dynamic_service),
):
    """List records for any dynamic object."""
    obj = await meta_service.get_object_by_name(object_name, workspace_id=_get_workspace_id(request))
    if not obj:
        raise HTTPException(status_code=404, detail=f"Object '{object_name}' not found")
    if obj.target_table_name:
        raise HTTPException(
            status_code=400,
            detail=f"Object '{object_name}' uses a physical table — use /api/v1/{object_name} instead",
        )

    items, total = await data_service.list_records(
        obj, workspace_id=_get_workspace_id(request), search=search, limit=limit, offset=offset
    )
    return DynamicRecordListResponse(total=total, items=items)


@router.get("/{object_name}/{record_id}", response_model=DynamicRecordResponse)
async def get_record(
    object_name: str,
    record_id: str,
    request: Request,
    meta_service: MetadataService = Depends(get_metadata_service),
    data_service: DynamicDataService = Depends(get_dynamic_service),
):
    """Get a single dynamic record."""
    obj = await meta_service.get_object_by_name(object_name, workspace_id=_get_workspace_id(request))
    if not obj:
        raise HTTPException(status_code=404, detail=f"Object '{object_name}' not found")
    if obj.target_table_name:
        raise HTTPException(status_code=400, detail="Use legacy API for physical tables")

    record = await data_service.get_record(obj, record_id, workspace_id=_get_workspace_id(request))
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.post("/{object_name}", response_model=DynamicRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    object_name: str,
    payload: DynamicRecordCreate,
    request: Request,
    meta_service: MetadataService = Depends(get_metadata_service),
    data_service: DynamicDataService = Depends(get_dynamic_service),
):
    """Create a new record in a dynamic object."""
    obj = await meta_service.get_object_by_name(object_name, workspace_id=_get_workspace_id(request))
    if not obj:
        raise HTTPException(status_code=404, detail=f"Object '{object_name}' not found")
    if obj.target_table_name:
        raise HTTPException(status_code=400, detail="Use legacy API for physical tables")

    record = await data_service.create_record(obj, payload, workspace_id=_get_workspace_id(request))
    return record


@router.patch("/{object_name}/{record_id}", response_model=DynamicRecordResponse)
async def update_record(
    object_name: str,
    record_id: str,
    payload: DynamicRecordUpdate,
    request: Request,
    meta_service: MetadataService = Depends(get_metadata_service),
    data_service: DynamicDataService = Depends(get_dynamic_service),
):
    """Update a dynamic record."""
    obj = await meta_service.get_object_by_name(object_name, workspace_id=_get_workspace_id(request))
    if not obj:
        raise HTTPException(status_code=404, detail=f"Object '{object_name}' not found")
    if obj.target_table_name:
        raise HTTPException(status_code=400, detail="Use legacy API for physical tables")

    record = await data_service.get_record(obj, record_id, workspace_id=_get_workspace_id(request))
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    updated = await data_service.update_record(obj, record, payload)
    return updated


@router.delete("/{object_name}/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    object_name: str,
    record_id: str,
    request: Request,
    meta_service: MetadataService = Depends(get_metadata_service),
    data_service: DynamicDataService = Depends(get_dynamic_service),
):
    """Soft-delete a dynamic record."""
    obj = await meta_service.get_object_by_name(object_name, workspace_id=_get_workspace_id(request))
    if not obj:
        raise HTTPException(status_code=404, detail=f"Object '{object_name}' not found")
    if obj.target_table_name:
        raise HTTPException(status_code=400, detail="Use legacy API for physical tables")

    record = await data_service.get_record(obj, record_id, workspace_id=_get_workspace_id(request))
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    await data_service.delete_record(record)


@router.post("/{object_name}/{record_id}/enrich", response_model=DynamicRecordResponse)
async def enrich_record(
    object_name: str,
    record_id: str,
    request: Request,
    meta_service: MetadataService = Depends(get_metadata_service),
    data_service: DynamicDataService = Depends(get_dynamic_service),
):
    """Run metadata-aware research agent to enrich a dynamic record."""
    obj = await meta_service.get_object_by_name(object_name, workspace_id=_get_workspace_id(request))
    if not obj:
        raise HTTPException(status_code=404, detail=f"Object '{object_name}' not found")
    if obj.target_table_name:
        raise HTTPException(status_code=400, detail="Use legacy API for physical tables")

    record = await data_service.get_record(obj, record_id, workspace_id=_get_workspace_id(request))
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    from app.agents.research.metadata_aware_agent import MetadataAwareResearchAgent
    agent = MetadataAwareResearchAgent(db=meta_service.db)
    enriched_data = await agent.enrich(
        object_meta=obj,
        record_data={**record.data, "label": record.label},
        workspace_id=_get_workspace_id(request),
    )

    if enriched_data:
        merged = {**record.data, **enriched_data}
        from app.schemas.metadata import DynamicRecordUpdate
        payload = DynamicRecordUpdate(data=merged)
        record = await data_service.update_record(obj, record, payload)

    return record
