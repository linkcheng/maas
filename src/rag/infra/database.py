from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://user:password@localhost/rag_db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    """获取数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 