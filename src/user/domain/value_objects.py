from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext


class Password(BaseModel):
    """密码值对象"""
    value: str

    def verify(self, hashed_password: str) -> bool:
        """验证密码"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(self.value, hashed_password)

    @staticmethod
    def hash(password: str) -> str:
        """哈希密码"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)


class UserCredentials(BaseModel):
    """用户认证信息值对象"""
    username: str
    password: str

class UserProfile(BaseModel):
    """用户档案值对象"""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool 