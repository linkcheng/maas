import logging
from typing import Any, Dict

from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from common.errors import NOT_AUTHENTICATED_ERROR, ErrorCode

logger = logging.getLogger(__name__)




class MCPException(Exception):
    def __init__(self, error: ErrorCode, context: Dict[str, Any] = None):
        self.error = error
        self.context = context or {}
        
    def __str__(self) -> str:
        return f"{self.error.code}: {self.error.message}"


async def MCPExceptionHandle(request: Request, exc: MCPException) -> JSONResponse:
    # 构建详细的错误日志信息
    error_details = {
        "error_code": exc.error.code,
        "error_message": exc.error.message,
        "path": request.url.path,
        "method": request.method,
        "context": exc.context
    }
    
    logger.error(f"MCP Exception occurred: {error_details}")
    
    # 构建响应
    json_response = {
        "code": exc.error.code, 
        "err_msg": exc.error.message,
        "status": "failure",                
    }
    if exc.context:
        json_response["context"] = exc.context
    
    status_code = 401 if exc.error.code == NOT_AUTHENTICATED_ERROR else 400
    return JSONResponse(status_code=status_code, content=json_response)


async def HTTPExceptionHandle(request: Request, exc: HTTPException) -> JSONResponse:
    error_details = {
        "error_code": exc.error.code,
        "error_message": exc.error.message,
        "path": request.url.path,
        "method": request.method,
        "context": exc.context
    }
    
    logger.error(f"MCP Exception occurred: {error_details}")
    content = dict(code=exc.status_code, err_msg=exc.detail, status="failure")
    return JSONResponse(status_code=exc.status_code, content=content)


async def ResponseAllHandle(request: Request, exc: Exception) -> JSONResponse:
    error_details = {
        "error": str(exc),
        "path": request.url.path,
        "method": request.method
    }
    
    logger.error(f"MCP Exception occurred: {error_details}")
    
    content = {
        "code": 500,
        "err_msg": "Internal Server Error",
        "status": "failure",  
        "details": str(exc) if str(exc) else None
    }
    return JSONResponse(status_code=500, content=content)
