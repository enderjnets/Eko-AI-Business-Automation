"""Tenant context for workspace-scoped multi-tenancy."""

import contextvars
from typing import Optional

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.core.security import decode_token, security_scheme
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember

# Context variable to hold workspace_id across async calls
workspace_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("workspace_id", default=None)


def get_workspace_id() -> Optional[str]:
    """Get current workspace_id from context variable."""
    return workspace_ctx.get()


def set_workspace_id(workspace_id: Optional[str]) -> None:
    """Set workspace_id in context variable."""
    workspace_ctx.set(workspace_id)


class TenantContext:
    """Resolved tenant context for the current request."""

    def __init__(self, workspace_id: Optional[str], user: Optional[User] = None):
        self.workspace_id = workspace_id
        self.user = user

    def apply_filter(self, query, model):
        """Apply workspace_id filter to a SQLAlchemy query if the model supports it."""
        if self.workspace_id and hasattr(model, "workspace_id"):
            return query.where(model.workspace_id == self.workspace_id)
        return query


async def resolve_tenant(
    request: Request,
    credentials: Optional[HTTPBearer] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> TenantContext:
    """Resolve tenant from request: header > JWT claim > query param."""
    workspace_id: Optional[str] = None

    # 1. Try header X-Workspace-ID
    workspace_id = request.headers.get("x-workspace-id")

    # 2. Try JWT claim
    if not workspace_id and credentials:
        token = credentials.credentials
        payload = decode_token(token)
        if payload:
            workspace_id = payload.get("workspace_id")

    # 3. Try query param (legacy fallback)
    if not workspace_id:
        workspace_id = request.query_params.get("workspace_id")

    if not workspace_id:
        return TenantContext(workspace_id=None)

    # Validate that workspace exists and user has access (if authenticated)
    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id, Workspace.is_active == True))
    workspace = result.scalar_one_or_none()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    user: Optional[User] = None
    if credentials:
        token = credentials.credentials
        payload = decode_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                result = await db.execute(select(User).where(User.id == int(user_id)))
                user = result.scalar_one_or_none()

    # If user is present, validate membership
    if user and not user.is_superuser:
        result = await db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user.id,
                WorkspaceMember.is_active == True,
            )
        )
        member = result.scalar_one_or_none()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this workspace",
            )

    return TenantContext(workspace_id=workspace_id, user=user)


async def get_tenant_context(tenant: TenantContext = Depends(resolve_tenant)) -> TenantContext:
    """FastAPI dependency that returns a validated TenantContext."""
    if not tenant.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace ID is required. Pass it via X-Workspace-ID header or workspace_id query param.",
        )
    # Set context variable for downstream use (Celery, raw SQL, etc.)
    set_workspace_id(tenant.workspace_id)
    return tenant


async def get_tenant_context_optional(tenant: TenantContext = Depends(resolve_tenant)) -> TenantContext:
    """FastAPI dependency that returns TenantContext without requiring workspace_id."""
    set_workspace_id(tenant.workspace_id)
    return tenant
