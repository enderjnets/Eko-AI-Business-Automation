"""MetadataService — CRUD and query operations for ObjectMetadata and FieldMetadata."""

from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.object_metadata import ObjectMetadata
from app.models.field_metadata import FieldMetadata, FieldType
from app.schemas.metadata import (
    ObjectMetadataCreate,
    ObjectMetadataUpdate,
    FieldMetadataCreate,
    FieldMetadataUpdate,
)


class MetadataService:
    """Service layer for the metadata engine."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ------------------------------------------------------------------
    # ObjectMetadata
    # ------------------------------------------------------------------

    async def list_objects(
        self,
        workspace_id: Optional[str] = None,
        include_inactive: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[ObjectMetadata], int]:
        stmt = select(ObjectMetadata)
        if workspace_id is not None:
            stmt = stmt.where(
                (ObjectMetadata.workspace_id == workspace_id) |
                (ObjectMetadata.workspace_id.is_(None))
            )
        else:
            stmt = stmt.where(ObjectMetadata.workspace_id.is_(None))

        if not include_inactive:
            stmt = stmt.where(ObjectMetadata.is_active.is_(True))

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        # Paginate
        stmt = stmt.order_by(ObjectMetadata.position, ObjectMetadata.name_singular)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        items = result.scalars().unique().all()
        return list(items), total

    async def get_object_by_id(
        self, object_id: str, workspace_id: Optional[str] = None
    ) -> Optional[ObjectMetadata]:
        stmt = select(ObjectMetadata).where(ObjectMetadata.id == object_id)
        if workspace_id is not None:
            stmt = stmt.where(
                (ObjectMetadata.workspace_id == workspace_id) |
                (ObjectMetadata.workspace_id.is_(None))
            )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_object_by_name(
        self, name: str, workspace_id: Optional[str] = None
    ) -> Optional[ObjectMetadata]:
        stmt = select(ObjectMetadata).where(
            (ObjectMetadata.name_singular == name) |
            (ObjectMetadata.name_plural == name)
        )
        if workspace_id is not None:
            stmt = stmt.where(
                (ObjectMetadata.workspace_id == workspace_id) |
                (ObjectMetadata.workspace_id.is_(None))
            )
        else:
            stmt = stmt.where(ObjectMetadata.workspace_id.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_object(
        self, payload: ObjectMetadataCreate, workspace_id: Optional[str] = None
    ) -> ObjectMetadata:
        obj = ObjectMetadata(
            workspace_id=workspace_id,
            **payload.model_dump(exclude={"fields"}),
        )
        self.db.add(obj)
        await self.db.flush()  # flush to get the id

        # Create default system fields if no fields provided
        if not payload.fields:
            await self._create_default_fields(obj.id, workspace_id)
        else:
            for field_payload in payload.fields:
                field = FieldMetadata(
                    workspace_id=workspace_id,
                    object_metadata_id=obj.id,
                    **field_payload.model_dump(),
                )
                self.db.add(field)

        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update_object(
        self, obj: ObjectMetadata, payload: ObjectMetadataUpdate
    ) -> ObjectMetadata:
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete_object(self, obj: ObjectMetadata) -> None:
        await self.db.delete(obj)
        await self.db.commit()

    # ------------------------------------------------------------------
    # FieldMetadata
    # ------------------------------------------------------------------

    async def list_fields(
        self,
        object_metadata_id: str,
        workspace_id: Optional[str] = None,
        include_inactive: bool = False,
    ) -> List[FieldMetadata]:
        stmt = select(FieldMetadata).where(
            FieldMetadata.object_metadata_id == object_metadata_id
        )
        if workspace_id is not None:
            stmt = stmt.where(
                (FieldMetadata.workspace_id == workspace_id) |
                (FieldMetadata.workspace_id.is_(None))
            )
        if not include_inactive:
            stmt = stmt.where(FieldMetadata.is_active.is_(True))
        stmt = stmt.order_by(FieldMetadata.position, FieldMetadata.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_field_by_id(
        self, field_id: str, workspace_id: Optional[str] = None
    ) -> Optional[FieldMetadata]:
        stmt = select(FieldMetadata).where(FieldMetadata.id == field_id)
        if workspace_id is not None:
            stmt = stmt.where(
                (FieldMetadata.workspace_id == workspace_id) |
                (FieldMetadata.workspace_id.is_(None))
            )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_field(
        self, payload: FieldMetadataCreate, workspace_id: Optional[str] = None
    ) -> FieldMetadata:
        field = FieldMetadata(
            workspace_id=workspace_id,
            **payload.model_dump(),
        )
        self.db.add(field)
        await self.db.commit()
        await self.db.refresh(field)
        return field

    async def update_field(
        self, field: FieldMetadata, payload: FieldMetadataUpdate
    ) -> FieldMetadata:
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(field, key, value)
        await self.db.commit()
        await self.db.refresh(field)
        return field

    async def delete_field(self, field: FieldMetadata) -> None:
        await self.db.delete(field)
        await self.db.commit()

    # ------------------------------------------------------------------
    # Workspace seeding
    # ------------------------------------------------------------------

    async def seed_default_objects(self, workspace_id: str) -> None:
        """Clone global standard objects into a new workspace."""
        from app.db.seed_metadata import STANDARD_OBJECTS, OBJECT_FIELDS_MAP
        from sqlalchemy import select

        for obj_def in STANDARD_OBJECTS:
            # Check if workspace-specific version already exists
            stmt = select(ObjectMetadata).where(
                ObjectMetadata.name_singular == obj_def["name_singular"],
                ObjectMetadata.workspace_id == workspace_id,
            )
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()
            if existing:
                continue

            # Clone object for this workspace
            obj_data = {k: v for k, v in obj_def.items()}
            obj = ObjectMetadata(workspace_id=workspace_id, **obj_data)
            self.db.add(obj)
            await self.db.flush()

            # Clone fields
            field_defs = OBJECT_FIELDS_MAP.get(obj_def["name_singular"], [])
            for fdef in field_defs:
                field_data = {k: v for k, v in fdef.items()}
                field_data.pop("relation_target_object_id", None)
                field = FieldMetadata(
                    workspace_id=workspace_id,
                    object_metadata_id=obj.id,
                    is_system=True,
                    **field_data,
                )
                self.db.add(field)

            await self.db.flush()
        await self.db.commit()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _create_default_fields(
        self, object_metadata_id: str, workspace_id: Optional[str] = None
    ) -> None:
        """Create default system fields (id, created_at, updated_at) for a new object."""
        defaults = [
            FieldMetadataCreate(
                object_metadata_id=object_metadata_id,
                name="id",
                label="ID",
                type=FieldType.TEXT,
                is_system=True,
                is_nullable=False,
                is_read_only=True,
                position=0,
            ),
            FieldMetadataCreate(
                object_metadata_id=object_metadata_id,
                name="created_at",
                label="Created At",
                type=FieldType.DATE_TIME,
                is_system=True,
                is_nullable=False,
                is_read_only=True,
                position=9998,
            ),
            FieldMetadataCreate(
                object_metadata_id=object_metadata_id,
                name="updated_at",
                label="Updated At",
                type=FieldType.DATE_TIME,
                is_system=True,
                is_nullable=False,
                is_read_only=True,
                position=9999,
            ),
        ]
        for f in defaults:
            field_data = f.model_dump()
            field_data.pop("object_metadata_id", None)
            field = FieldMetadata(
                workspace_id=workspace_id,
                object_metadata_id=object_metadata_id,
                **field_data,
            )
            self.db.add(field)
        await self.db.flush()
