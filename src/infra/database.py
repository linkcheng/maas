"""
数据库配置模块。
提供统一的数据库连接和会话管理功能。
"""
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from contextlib import asynccontextmanager

from config.settings import settings

logger = logging.getLogger(__name__)

# 创建元数据
metadata = MetaData()

# 创建基类
class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    metadata = metadata

# 创建异步引擎
engine: AsyncEngine = create_async_engine(
    settings.DB.URL,
    echo=settings.DB.ECHO,
    pool_size=settings.DB.POOL_SIZE,
    max_overflow=settings.DB.MAX_OVERFLOW,
    pool_timeout=settings.DB.POOL_TIMEOUT,
    pool_recycle=settings.DB.POOL_RECYCLE
)

# 创建异步会话工厂
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话
    
    Yields:
        AsyncSession: 数据库会话
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

@asynccontextmanager
async def get_db():
    """上下文管理器，用于在异步上下文中获取数据库会话"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

# 工作单元模式(Unit of Work)实现
class UnitOfWork:
    """工作单元模式，管理事务和仓储"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        """进入异步上下文，创建会话"""
        self.session = async_session_factory()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """离开异步上下文，提交或回滚事务，关闭会话"""
        if exc_type is not None:
            await self.rollback()
        await self.session.close()
    
    async def commit(self):
        """提交事务"""
        await self.session.commit()
    
    async def rollback(self):
        """回滚事务"""
        await self.session.rollback()

async def init_db() -> None:
    """初始化数据库"""
    logger.info("创建数据库表...")
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    logger.info("数据库表创建完成!")

async def close_db() -> None:
    """关闭数据库连接"""
    logger.info("关闭服务...")
    await engine.dispose()
    logger.info("数据库引擎已关闭!")
