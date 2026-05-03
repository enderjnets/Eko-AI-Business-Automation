"""DynamicDataService — generic CRUD for dynamic records (custom objects)."""

from typing import Optional, List, Any
import uuid
from datetime import datetime

from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import JSONB

from app.models.object_metadata import ObjectMetadata
from app.models.field_metadata import FieldMetadata, FieldType
from app.models.dynamic_record import DynamicRecord
from app.services.metadata_service import MetadataService
from app.schemas.metadata import DynamicRecordCreate, DynamicRecordUpdate


class DynamicDataService:
    """Service for CRUD operations on dynamic records."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.metadata = MetadataService(db)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    async def validate_record(
        self,
        obj: ObjectMetadata,
        data: dict,
        existing_record: Optional[DynamicRecord] = None,
    ) -> dict:
        """Validate record data against object metadata."""
        fields = await self.metadata.list_fields(obj.id)
        field_map = {f.name: f for f in fields}
        errors = {}
        validated = {}

        for field in fields:
            if field.is_system and field.name in ("id", "created_at", "updated_at"):
                continue  # Skip system fields

            value = data.get(field.name)

            # Required check
            if not field.is_nullable and value is None and not existing_record:
                errors[field.name] = "required"
                continue

            if value is None:
                if field.default_value is not None:
                    validated[field.name] = field.default_value
                continue

            # Type validation
            validated_value = self._validate_field_type(field, value)
            if validated_value is None and value is not None:
                errors[field.name] = f"invalid type for {field.type}"
                continue

            validated[field.name] = validated_value

        if errors:
            raise ValueError(errors)

        return validated

    def _validate_field_type(self, field: FieldMetadata, value: Any) -> Any:
        """Validate and coerce a single field value."""
        try:
            if field.type == FieldType.TEXT:
                return str(value)
            elif field.type == FieldType.NUMBER:
                return float(value)
            elif field.type == FieldType.EMAIL:
                v = str(value)
                if "@" not in v:
                    return None
                return v
            elif field.type == FieldType.PHONE:
                return str(value)
            elif field.type == FieldType.URL:
                v = str(value)
                if not v.startswith(("http://", "https://")):
                    return None
                return v
            elif field.type == FieldType.BOOLEAN:
                return bool(value)
            elif field.type == FieldType.SELECT:
                v = str(value)
                if field.options and v not in [o.get("value") for o in field.options]:
                    return None
                return v
            elif field.type == FieldType.MULTI_SELECT:
                if not isinstance(value, list):
                    return None
                if field.options:
                    valid = [o.get("value") for o in field.options]
                    return [v for v in value if v in valid]
                return list(value)
            elif field.type == FieldType.JSON:
                return dict(value) if not isinstance(value, dict) else value
            elif field.type == FieldType.DATE:
                if isinstance(value, str):
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                return value
            elif field.type == FieldType.DATE_TIME:
                if isinstance(value, str):
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                return value
            elif field.type == FieldType.CURRENCY:
                return float(value)
            elif field.type == FieldType.RELATION:
                return str(value)
            elif field.type == FieldType.RICH_TEXT:
                return str(value)
            elif field.type == FieldType.VECTOR:
                if not isinstance(value, list):
                    return None
                return [float(v) for v in value]
            else:
                return value
        except (ValueError, TypeError):
            return None

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def list_records(
        self,
        obj: ObjectMetadata,
        workspace_id: Optional[str] = None,
        filters: Optional[List[dict]] = None,
        sorts: Optional[List[dict]] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[List[DynamicRecord], int]:
        """List dynamic records for an object with optional filtering and sorting."""
        stmt = select(DynamicRecord).where(
            DynamicRecord.object_metadata_id == obj.id,
            DynamicRecord.deleted_at.is_(None),
        )
        if workspace_id is not None:
            stmt = stmt.where(
                (DynamicRecord.workspace_id == workspace_id) |
                (DynamicRecord.workspace_id.is_(None))
            )
        else:
            stmt = stmt.where(DynamicRecord.workspace_id.is_(None))

        # Search
        if search:
            stmt = stmt.where(
                or_(
                    DynamicRecord.label.ilike(f"%{search}%"),
                    DynamicRecord.search_vector.ilike(f"%{search}%"),
                )
            )

        # Filters (basic JSONB path matching)
        if filters:
            for f in filters:
                field_name = f.get("field")
                operator = f.get("operator", "eq")
                value = f.get("value")
                if field_name and value is not None:
                    stmt = self._apply_filter(stmt, field_name, operator, value)

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        # Sorts
        if sorts:
            for s in sorts:
                field_name = s.get("field")
                direction = s.get("direction", "asc")
                if field_name:
                    stmt = self._apply_sort(stmt, field_name, direction)
        else:
            stmt = stmt.order_by(DynamicRecord.created_at.desc())

        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    def _apply_filter(self, stmt, field_name: str, operator: str, value: Any):
        """Apply a JSONB filter to the query."""
        path = text(f"data->>'{field_name}'")
        if operator == "eq":
            return stmt.where(path == str(value))
        elif operator == "neq":
            return stmt.where(path != str(value))
        elif operator == "contains":
            return stmt.where(path.ilike(f"%{value}%"))
        elif operator == "gt":
            return stmt.where(text(f"(data->>'{field_name}')::float > {float(value)}"))
        elif operator == "lt":
            return stmt.where(text(f"(data->>'{field_name}')::float < {float(value)}"))
        elif operator == "is_empty":
            return stmt.where(
                or_(
                    text(f"data->>'{field_name}' IS NULL"),
                    text(f"data->>'{field_name}' = ''"),
                )
            )
        elif operator == "is_not_empty":
            return stmt.where(
                and_(
                    text(f"data->>'{field_name}' IS NOT NULL"),
                    text(f"data->>'{field_name}' != ''"),
                )
            )
        return stmt

    def _apply_sort(self, stmt, field_name: str, direction: str):
        """Apply JSONB sorting."""
        if direction == "asc":
            return stmt.order_by(text(f"data->>'{field_name}' ASC NULLS LAST"))
        else:
            return stmt.order_by(text(f"data->>'{field_name}' DESC NULLS LAST"))

    async def get_record(
        self,
        obj: ObjectMetadata,
        record_id: str,
        workspace_id: Optional[str] = None,
    ) -> Optional[DynamicRecord]:
        stmt = select(DynamicRecord).where(
            DynamicRecord.id == record_id,
            DynamicRecord.object_metadata_id == obj.id,
            DynamicRecord.deleted_at.is_(None),
        )
        if workspace_id is not None:
            stmt = stmt.where(
                (DynamicRecord.workspace_id == workspace_id) |
                (DynamicRecord.workspace_id.is_(None))
            )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_record(
        self,
        obj: ObjectMetadata,
        payload: DynamicRecordCreate,
        workspace_id: Optional[str] = None,
    ) -> DynamicRecord:
        validated_data = await self.validate_record(obj, payload.data)
        record = DynamicRecord(
            workspace_id=workspace_id,
            object_metadata_id=obj.id,
            label=payload.label,
            data=validated_data,
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def update_record(
        self,
        obj: ObjectMetadata,
        record: DynamicRecord,
        payload: DynamicRecordUpdate,
    ) -> DynamicRecord:
        if payload.label is not None:
            record.label = payload.label
        if payload.data is not None:
            # Merge existing data with updates
            merged = {**record.data, **payload.data}
            validated_data = await self.validate_record(obj, merged, existing_record=record)
            record.data = validated_data
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def delete_record(self, record: DynamicRecord) -> None:
        record.deleted_at = datetime.utcnow()
        await self.db.commit()
