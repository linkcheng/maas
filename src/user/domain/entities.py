from datetime import datetime
from secrets import token_urlsafe
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4

class User(BaseModel):
    """用户实体"""
    id: int = 0
    user_id: UUID = uuid4()
    username: str
    email: EmailStr = ''
    hashed_password: str
    is_active: bool = True
    secret_key: str = token_urlsafe(32)
    sk_updated_at: Optional[datetime] = None
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"

    def update_password(self, new_hashed_password: str) -> None:
        """更新密码"""
        self.hashed_password = new_hashed_password

    def update_last_login(self) -> None:
        """更新最后登录时间"""
        self.last_login = datetime.now()

    def deactivate(self) -> None:
        """停用用户"""
        self.is_active = False

    def activate(self) -> None:
        """激活用户"""
        self.is_active = True

    def update_secret_key(self) -> None:
        """更新密钥"""
        self.secret_key = token_urlsafe(32)
        self.sk_updated_at = datetime.now()
