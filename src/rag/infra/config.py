from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "rag_db"
    
    # Milvus配置
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: str = "19530"
    
    # 向量嵌入配置
    EMBEDDING_MODEL: str = "text-embedding-3-small"  # OpenAI的嵌入模型
    VECTOR_DIMENSION: int = 1536  # text-embedding-3-small的维度
    
    # OpenAI配置
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    
    # 分块配置
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings() 