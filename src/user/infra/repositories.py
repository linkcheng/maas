"""
仓储实现模块。
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from user.domain.entities import User
from user.domain.repositories import IUserRepository
from .models import UserModel


class UserRepository(IUserRepository):
    """用户仓储实现"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """创建用户"""
        db_user = UserModel(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            secret_key=user.secret_key,
            is_superuser=user.is_superuser,
            last_login=user.last_login
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)

    async def get_by_id(self, id: int) -> Optional[User]:
        """通过ID获取用户"""
        stmt = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def get_by_user_id(self, user_id: UUID) -> Optional[User]:
        """通过ID获取用户"""
        stmt = select(UserModel).where(UserModel.user_id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def get_by_username(self, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def update(self, user: User) -> User:
        """更新用户"""
        stmt = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                secret_key=user.secret_key,
                secret_key_updated_at=user.sk_updated_at,
                last_login=user.last_login
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()
        
        db_user = await self.session.get(UserModel, user.id)
        await self.session.refresh(db_user)
        return self._to_entity(db_user)

    async def delete(self, user_id: UUID) -> bool:
        """删除用户"""
        stmt = delete(UserModel).where(UserModel.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """列出用户"""
        stmt = select(UserModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [self._to_entity(db_user) for db_user in db_users]

    def _to_entity(self, db_user: UserModel) -> User:
        """将数据库模型转换为实体"""
        return User(
            id=db_user.id,
            user_id=db_user.user_id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active,
            is_superuser=db_user.is_superuser,
            secret_key=db_user.secret_key,
            sk_updated_at=db_user.secret_key_updated_at,
            last_login=db_user.last_login
        )
