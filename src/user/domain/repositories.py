from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from .entities import User

class IUserRepository(ABC):
    """用户仓储接口"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """创建用户"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """通过ID获取用户"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[User]:
        """通过USER_ID获取用户"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """更新用户"""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """删除用户"""
        pass

    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """列出用户"""
        pass 