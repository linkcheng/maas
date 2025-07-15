"""
应用服务模块。
"""
from user.domain.entities import User
from user.domain.value_objects import Password
from user.domain.repositories import IUserRepository
from common.exceptions import MCPException
from common.errors import *


class UserDomainService:
    """用户服务"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    async def create_user(self, username: str, email: str, password: str) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        if await self.user_repository.get_by_username(username):
            raise MCPException(USERNAME_EXISTS_ERROR)

        # 创建用户
        hashed_password = Password.hash(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        return await self.user_repository.create(user)

    async def authenticate_user(self, username: str, password: str) -> User:
        """用户认证"""
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise MCPException(USERNAME_PASSWORD_ERROR)

        if not Password(value=password).verify(user.hashed_password):
            raise MCPException(PASSWORD_ERROR)

        if not user.is_active:
            raise MCPException(USER_FORBIDDEN_ERROR)

        # 更新最后登录时间
        user.update_last_login()
        return await self.user_repository.update(user)

    async def change_password(self, user_id: int, old_password: str, new_password: str) -> User:
        """修改密码"""

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise MCPException(USER_NOT_FOUND_ERROR)

        if not Password(value=old_password).verify(user.hashed_password):
            raise MCPException(PASSWORD_ERROR)

        user.update_password(Password.hash(new_password))
        return await self.user_repository.update(user)

    async def get_user(self, user_id: int) -> User:
        """获取用户档案"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise MCPException(USER_NOT_FOUND_ERROR)
        return user

    async def refresh_secret_key(self, user_id: int) -> User:
        """刷新用户密钥"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise MCPException(USER_NOT_FOUND_ERROR)
        user.update_secret_key()
        return await self.user_repository.update(user)