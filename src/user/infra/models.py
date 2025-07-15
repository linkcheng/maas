"""
ORM 模型模块。
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from secrets import token_urlsafe
from sqlalchemy import String, Boolean, DateTime, Uuid, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infra.database import Base


class UserModel(Base):
    """用户模型"""
    __tablename__ = "users"

    # 默认主键
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    # 业务标识符
    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        unique=True,
        default=uuid4
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    secret_key: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default=lambda: token_urlsafe(32)
    )
    secret_key_updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    ) 