"""
应用层数据模型。
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(
        ...,
        description="用户名"
    )
    email: EmailStr = Field(default='', description="电子邮箱")


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(
        ...,
        description="用户名"
    )
    password: str = Field(
        ...,
        description="密码"
    )

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(
        ...,
        description="密码"
    )

class UserUpdate(BaseModel):
    """用户更新模型"""
    username: Optional[str] = Field(
        None,
        description="用户名"
    )
    email: Optional[EmailStr] = Field(None, description="电子邮箱")
    is_active: Optional[bool] = Field(None, description="是否激活")

class UserResponse(UserBase):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    is_active: bool = Field(..., description="是否激活")
    is_superuser: bool = Field(..., description="是否超级用户")

    class Config:
        """配置"""
        from_attributes = True

class Token(BaseModel):
    """令牌模型"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")

class PasswordChange(BaseModel):
    """密码修改模型"""
    old_password: str = Field(..., description="原密码")
    new_password: str = Field(
        ...,
        description="新密码"
    ) 