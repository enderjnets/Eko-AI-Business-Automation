from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, List
from sqlalchemy import String, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, PyEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    AGENT = "agent"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))

    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.AGENT)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    leads: Mapped[List["Lead"]] = relationship(
        "Lead", back_populates="owner", lazy="selectin"
    )
