"""
应用服务模块。
"""
from typing import Tuple

from user.domain.entities import User
from user.domain.value_objects import UserProfile
from user.domain.services import UserDomainService
from config.settings import UsersConfig
from common.exceptions import MCPException
from common.errors import *


class UserService:
    """用户应用服务"""
    
    def __init__(self, user_domain_svc: UserDomainService, config: UsersConfig):
        self.user_domain_svc = user_domain_svc
        self.config = config

    async def create_user(self, username: str, email: str, password: str) -> User:
        """创建用户"""
        # 验证用户名长度
        if len(username) < self.config.USERNAME_MIN_LENGTH:
            raise MCPException(USERNAME_MIN_LENGTH_ERROR)
        if len(username) > self.config.USERNAME_MAX_LENGTH:
            raise MCPException(USERNAME_MAX_LENGTH_ERROR)

        # 验证密码长度
        if len(password) < self.config.PASSWORD_MIN_LENGTH:
            raise MCPException(PASSWORD_MIN_LENGTH_ERROR)
        if len(password) > self.config.PASSWORD_MAX_LENGTH:
            raise MCPException(PASSWORD_MAX_LENGTH_ERROR)

        return await self.user_domain_svc.create_user(username, email, password)

    async def authenticate_user(self, username: str, password: str) -> Tuple[User, str]:
        """用户认证"""
        user = await self.user_domain_svc.authenticate_user(username, password)
        from utils.auth_util import AuthUtil

        # 生成访问令牌
        access_token = AuthUtil.create(user)
        return user, access_token

    async def change_password(self, user_id: int, old_password: str, new_password: str) -> User:
        """修改密码"""
        # 验证新密码长度
        if len(new_password) < self.config.password_min_length:
            raise MCPException(PASSWORD_MIN_LENGTH_ERROR)
        if len(new_password) > self.config.password_max_length:
            raise MCPException(PASSWORD_MAX_LENGTH_ERROR)

        return await self.user_domain_svc.change_password(user_id, old_password, new_password)

    async def get_user_profile(self, user_id: int) -> UserProfile:
        """获取用户档案"""
        user = await self.user_domain_svc.get_user(user_id)

        return UserProfile(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
