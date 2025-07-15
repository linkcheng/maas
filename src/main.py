import logging
from contextlib import AsyncExitStack, asynccontextmanager

import anyio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from common.exceptions import (
    HTTPExceptionHandle,
    MCPException, 
    MCPExceptionHandle, 
    ResponseAllHandle
)
from common.middleware import OAuthMiddleware
from config.logger import setup_logging
from config.settings import settings
from infra.database import init_db, close_db
from mcp_server import init_fastmcp_app
from rag.infra.vector_store_service import VectorStoreService

# from chat.api.router import router as chat_router
from chat.api.router import router as chat_router
from user.api.router import router as user_router
from rag.api.routes import router as rag_router

# 配置日志
setup_logging()

logger = logging.getLogger(__name__)

# 创建向量存储服务实例
vector_store_service = VectorStoreService()

# 应用程序生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用程序启动和关闭事件"""
    try:
        # 初始化数据库
        await init_db()
        
        # 初始化向量存储服务
        await vector_store_service.initialize()
        
        yield
        
        # 关闭向量存储服务
        await vector_store_service.close()
        
        # 关闭数据库连接
        await close_db()
    except Exception as e:
        logger.error(f"应用程序生命周期管理错误: {str(e)}")
        raise


def register_exceptions(app: FastAPI):

    app.add_exception_handler(MCPException, MCPExceptionHandle)
    app.add_exception_handler(HTTPException, HTTPExceptionHandle)
    app.add_exception_handler(Exception, ResponseAllHandle)


def register_routers(app: FastAPI):

    app.include_router(user_router, prefix="/api/v1", tags=["user"])
    app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
    app.include_router(rag_router, prefix="/api/v1/rag", tags=["rag"])
    

def register_middleware(app: FastAPI):
    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.SERVER.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(OAuthMiddleware)


def create_app():

    mcp_app = anyio.run(init_fastmcp_app)
    
    @asynccontextmanager
    async def nested_lifespans(app: FastAPI):
        async with AsyncExitStack() as stack:
            await stack.enter_async_context(lifespan(app))
            await stack.enter_async_context(mcp_app.lifespan(app))
            yield

    app = FastAPI(
        title=settings.APP.NAME,
        description=settings.APP.DESCRIPTION,
        version=settings.APP.VERSION,
        lifespan=nested_lifespans
    )
    app.mount("/api/v1/server", mcp_app)

    register_exceptions(app)

    register_middleware(app)

    register_routers(app)
    
    # 根路由
    @app.get("/")
    async def root():
        return {
            "status": "running",
            "version": settings.APP.VERSION,
            "description": settings.APP.DESCRIPTION
        }
    
    # 健康检查
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    return app


if __name__ == "__main__":
    import uvicorn
    import uvloop
    # 导入配置
    from config.settings import settings
    
    # 从配置中获取服务器参数
    host = settings.SERVER.HOST
    port = settings.SERVER.PORT
    reload = settings.SERVER.RELOAD
    
    # 启动服务
    app = create_app()
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level=settings.LOG.LEVEL.lower(),
        loop='uvloop',
    )
    uvicorn.Server(config).run()
    
