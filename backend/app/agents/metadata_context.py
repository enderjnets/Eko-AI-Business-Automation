"""
Metadata-aware context for agents.

Provides a generic way for agents to:
1. Read object/field definitions from the metadata engine
2. Convert DynamicRecord JSONB data to typed dictionaries
3. Validate and normalize data against metadata schema
"""

import logging
from typing import Any, Optional, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.metadata_service import MetadataService
from app.services.dynamic_data_service import DynamicDataService
from app.models.object_metadata import ObjectMetadata
from app.models.field_metadata import FieldType

logger = logging.getLogger(__name__)


class MetadataContext:
    """Context object that agents receive to interact with metadata + dynamic data."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self._meta_service = MetadataService(db)
        self._data_service = DynamicDataService(db)
        self._object_cache: Dict[str, ObjectMetadata] = {}

    # ------------------------------------------------------------------
    # Object / field resolution
    # ------------------------------------------------------------------

    async def get_object(self, name: str, workspace_id: Optional[str] = None) -> Optional[ObjectMetadata]:
        """Get object metadata by singular name (cached per instance)."""
        cache_key = f"{name}:{workspace_id or ''}"
        if cache_key not in self._object_cache:
            obj = await self._meta_service.get_object_by_name(name, workspace_id=workspace_id)
            if obj:
                self._object_cache[cache_key] = obj
        return self._object_cache.get(cache_key)

    async def get_field_map(self, object_name: str, workspace_id: Optional[str] = None) -> Dict[str, Any]:
        """Return {field_name: FieldMetadata} for an object."""
        obj = await self.get_object(object_name, workspace_id)
        if not obj:
            return {}
        return {f.name: f for f in obj.fields}

    # ------------------------------------------------------------------
    # Data conversion helpers
    # ------------------------------------------------------------------

    @staticmethod
    def normalize_value(field_type: str, raw: Any) -> Any:
        """Coerce a raw value to the appropriate Python type for a field."""
        if raw is None:
            return None
        ft = field_type.upper()
        if ft in (FieldType.NUMBER, FieldType.CURRENCY):
            try:
                return float(raw)
            except (ValueError, TypeError):
                return None
        if ft == FieldType.BOOLEAN:
            if isinstance(raw, bool):
                return raw
            if isinstance(raw, str):
                return raw.lower() in ("true", "1", "yes", "si", "sí")
            return bool(raw)
        if ft in (FieldType.SELECT, FieldType.TEXT, FieldType.EMAIL, FieldType.PHONE, FieldType.URL):
            return str(raw) if raw is not None else None
        if ft == FieldType.MULTI_SELECT:
            if isinstance(raw, list):
                return [str(v) for v in raw]
            if isinstance(raw, str):
                return [v.strip() for v in raw.split(",") if v.strip()]
            return []
        if ft in (FieldType.DATE, FieldType.DATE_TIME):
            if isinstance(raw, str):
                return raw  # keep ISO string
            return str(raw) if raw is not None else None
        if ft == FieldType.JSON:
            return raw if isinstance(raw, dict) else {}
        return raw

    async def record_to_dict(
        self,
        object_name: str,
        record_data: Dict[str, Any],
        workspace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Normalize a raw data dict using the object's metadata schema."""
        field_map = await self.get_field_map(object_name, workspace_id)
        result: Dict[str, Any] = {}
        for name, field in field_map.items():
            raw = record_data.get(name)
            result[name] = self.normalize_value(field.type, raw)
        # Include any extra fields not in metadata (passthrough)
        for k, v in record_data.items():
            if k not in result:
                result[k] = v
        return result

    async def dict_to_record_data(
        self,
        object_name: str,
        data: Dict[str, Any],
        workspace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Prepare a dict for DynamicRecord creation, filtering out system/read-only fields."""
        field_map = await self.get_field_map(object_name, workspace_id)
        result: Dict[str, Any] = {}
        for name, field in field_map.items():
            if field.is_system or field.is_read_only:
                continue
            if name in data:
                result[name] = self.normalize_value(field.type, data[name])
        return result

    # ------------------------------------------------------------------
    # Dynamic data access (thin wrappers)
    # ------------------------------------------------------------------

    async def list_records(
        self,
        object_name: str,
        workspace_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> tuple[List[Any], int]:
        """List dynamic records for an object."""
        obj = await self.get_object(object_name, workspace_id)
        if not obj:
            return [], 0
        return await self._data_service.list_records(
            obj, workspace_id=workspace_id, limit=limit, offset=offset, search=search
        )

    async def create_record(
        self,
        object_name: str,
        label: str,
        data: Dict[str, Any],
        workspace_id: Optional[str] = None,
    ) -> Any:
        """Create a dynamic record."""
        obj = await self.get_object(object_name, workspace_id)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found in metadata")
        from app.schemas.metadata import DynamicRecordCreate
        payload = DynamicRecordCreate(label=label, data=data)
        return await self._data_service.create_record(obj, payload, workspace_id=workspace_id)

    async def update_record(
        self,
        object_name: str,
        record_id: str,
        data: Dict[str, Any],
        workspace_id: Optional[str] = None,
    ) -> Any:
        """Update a dynamic record."""
        obj = await self.get_object(object_name, workspace_id)
        if not obj:
            raise ValueError(f"Object '{object_name}' not found in metadata")
        from app.schemas.metadata import DynamicRecordUpdate
        # Fetch existing to merge
        existing = await self._data_service.get_record(obj, record_id, workspace_id=workspace_id)
        if not existing:
            raise ValueError(f"Record '{record_id}' not found")
        merged = {**existing.data, **data}
        payload = DynamicRecordUpdate(data=merged)
        return await self._data_service.update_record(obj, record_id, payload, workspace_id=workspace_id)
