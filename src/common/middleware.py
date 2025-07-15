import logging
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from common.exceptions  import MCPException
from common.errors import *
from config.settings import settings
from utils.auth_util import AuthUtil

logger = logging.getLogger(__name__)


class OAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # 预编译排除路径集合，提高检查效率
        self._excluded_paths = set(settings.AUTH.EXCLUDE_PATHS or [])
        self._excluded_prefixes = tuple(settings.AUTH.EXCLUDE_PATHS_PREFIX or [])

    async def dispatch(self, request: Request, call_next):
        try:
            if self._is_excluded_path(request.url.path):
                return await call_next(request)
            print(f"========================{request.url.path}")
            token = await self._get_token(request)
            # 验证token并获取用户信息
            user_info, _ = await AuthUtil.verify(token, request)
            
            # 将用户信息存储在请求状态中供后续使用
            request.state.user = user_info
            logger.info(f"User authenticated: {user_info}")
            
            # 继续处理请求
            response = await call_next(request)
            return response
        except MCPException as e:
            data = {"code": e.error.code, "err_msg": e.error.message, "status": "failure"}
            return JSONResponse(content=data)

    def _is_excluded_path(self, path: str) -> bool:
        path = path.rstrip("/")
        ret =  (
            path in self._excluded_paths or 
            any(path.startswith(excluded) for excluded in self._excluded_prefixes)
        )
        return ret
    
    async def _get_token(self, request: Request) -> str:
        """从请求头中获取 token，增加更多错误细节"""
        authorization = request.headers.get("Authorization")
        if not authorization:
            logger.info("Missing Authorization header")
            raise MCPException(NOT_AUTHENTICATED_ERROR)
        
        try:
            scheme, token = authorization.split(" ")
            if not token:
                logger.info("Empty token")
                raise MCPException(INVALID_AUTH_SCHEMA_ERROR)
                
            if scheme.lower() != "bearer":
                logger.info(f"Invalid scheme: {scheme}")
                raise MCPException(INVALID_AUTH_SCHEMA_ERROR)
                
            return token
        except ValueError:
            logger.info("Malformed Authorization header")
            raise MCPException(INVALID_AUTH_SCHEMA_ERROR)