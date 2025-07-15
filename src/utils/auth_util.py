from datetime import datetime, timedelta

from fastapi import Request
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError

from common.exceptions  import MCPException
from common.errors import *
from config.settings import settings

from infra.database import get_db
from user.infra.models import UserModel
from user.domain.entities import User


class AuthUtil:
    
    @classmethod
    def create(cls, user: User) -> str:
        """创建访问令牌"""
        auth = settings.AUTH
        expire = datetime.now() + timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user.id),
            "exp": int(expire.timestamp()),
            "username": user.username,
            "is_superuser": user.is_superuser,
            "key_version": user.secret_key,
        }
        return jwt.encode( to_encode, auth.SECRET_KEY, algorithm=auth.ALGORITHM)

    @classmethod
    async def verify(cls, token: str, request: Request) -> tuple[User, dict]:
        """验证 token"""
        auth = settings.AUTH
        try:
            # 从数据库获取用户的密钥
            async with get_db() as session:
                # 先使用基础密钥解码获取用户ID
                payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
                user_id = payload.get("sub")
                
                # 获取用户信息
                user = await session.get(UserModel, user_id)
                if not user:
                    raise MCPException(INVALID_TOKEN_ERROR)
                
                # 检查是否过期
                exp = payload.get("exp")
                if exp and datetime.fromtimestamp(exp) < datetime.now():
                    raise MCPException(TOKEN_EXPIRED_ERROR)
                
                # 验证 token 是否使用当前密钥生成
                if payload.get("key_version") != user.secret_key:
                    raise MCPException(INVALID_TOKEN_ERROR)
                
                if not user.is_active:
                    raise MCPException(USER_NOT_ACTIVE_ERROR)
                
                return user, payload
        
        except ExpiredSignatureError:
            raise MCPException(TOKEN_EXPIRED_ERROR)
        except JWTError:
            raise MCPException(INVALID_TOKEN_ERROR)
