"""
API 路由模块。
"""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from user.application.services import UserService
from user.application.schemas import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    Token,
    PasswordChange
)
from infra.database import get_session
from user.infra.repositories import UserRepository
from user.domain.services import UserDomainService
from config.settings import settings
from common.response import ResponseModel, ResponseBuilder

router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger(__name__)

async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    """获取用户服务"""
    repository = UserRepository(session)
    domain_service = UserDomainService(repository)
    return UserService(domain_service, settings.USERS)

@router.post("/", response_model=ResponseModel)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """创建用户"""
    user = await user_service.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    return ResponseBuilder.success(data=UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    ))

@router.post("/token", response_model=ResponseModel)
async def login(
    form_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """用户登录"""
    _, access_token = await user_service.authenticate_user(
        username=form_data.username,
        password=form_data.password
    )
    return  ResponseBuilder.success(data=Token(access_token=access_token))

@router.get("/me", response_model=ResponseModel)
async def read_users_me(request: Request):
    """获取当前用户信息"""
    user = request.state.user

    return ResponseBuilder.success(data=UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    ))

@router.put("/me/password", response_model=ResponseModel)
async def change_password(
    request: Request,
    password_data: PasswordChange,
    user_service: UserService = Depends(get_user_service)
):
    """修改密码"""
    user = await user_service.change_password(
        request.state.user.id,
        password_data.old_password,
        password_data.new_password
    )
    return ResponseBuilder.success(data=UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    ))

@router.get("/{user_id}", response_model=ResponseModel)
async def get_user_profile(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """获取用户信息"""
    user = await user_service.get_user_profile(user_id)
    return ResponseBuilder.success(data=user)
