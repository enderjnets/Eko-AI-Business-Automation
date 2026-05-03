"""ViewService — CRUD for declarative views."""

from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.view import View, ViewField, ViewFilter, ViewSort
from app.schemas.view import (
    ViewCreate,
    ViewUpdate,
    ViewFieldCreate,
    ViewFilterCreate,
    ViewSortCreate,
)


class ViewService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_views(
        self,
        object_metadata_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[View], int]:
        stmt = select(View)
        if object_metadata_id:
            stmt = stmt.where(View.object_metadata_id == object_metadata_id)
        if workspace_id is not None:
            stmt = stmt.where(
                (View.workspace_id == workspace_id) | (View.workspace_id.is_(None))
            )
        else:
            stmt = stmt.where(View.workspace_id.is_(None))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        stmt = stmt.order_by(View.position, View.name).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().unique().all()), total

    async def get_view_by_id(
        self, view_id: str, workspace_id: Optional[str] = None
    ) -> Optional[View]:
        stmt = select(View).where(View.id == view_id)
        if workspace_id is not None:
            stmt = stmt.where(
                (View.workspace_id == workspace_id) | (View.workspace_id.is_(None))
            )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_view(
        self, payload: ViewCreate, object_metadata_id: str, workspace_id: Optional[str] = None
    ) -> View:
        view = View(
            workspace_id=workspace_id,
            object_metadata_id=object_metadata_id,
            name=payload.name,
            type=payload.type,
            icon=payload.icon,
            position=payload.position,
            is_default=payload.is_default,
            is_compact=payload.is_compact,
            group_by_field_id=payload.group_by_field_id,
            calendar_field_id=payload.calendar_field_id,
            visibility=payload.visibility,
        )
        self.db.add(view)
        await self.db.flush()

        for vf in payload.view_fields or []:
            self.db.add(ViewField(
                view_id=view.id, field_metadata_id=vf.field_metadata_id,
                position=vf.position, is_visible=vf.is_visible, width=vf.width
            ))
        for vf in payload.view_filters or []:
            self.db.add(ViewFilter(
                view_id=view.id, field_metadata_id=vf.field_metadata_id,
                operator=vf.operator, value=vf.value, display_value=vf.display_value
            ))
        for vs in payload.view_sorts or []:
            self.db.add(ViewSort(
                view_id=view.id, field_metadata_id=vs.field_metadata_id,
                direction=vs.direction
            ))

        await self.db.commit()
        await self.db.refresh(view)
        return view

    async def update_view(self, view: View, payload: ViewUpdate) -> View:
        data = payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(view, k, v)
        await self.db.commit()
        await self.db.refresh(view)
        return view

    async def delete_view(self, view: View) -> None:
        await self.db.delete(view)
        await self.db.commit()
