from typing import List
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AppConfig(BaseSettings):
    """应用配置"""
    NAME: str = Field("MCP Server with Chat", alias="name")
    VERSION: str = Field("1.0.0", alias="version")
    DESCRIPTION: str = Field("MCP Server 与 Chat API 的集成应用", alias="description")
    ENV: str = Field("dev", alias="env")
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class LogConfig(BaseSettings):
    """日志配置"""
    LEVEL: str = Field("INFO", alias="level")
    FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DIR: str = "./logs"
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class DatabaseConfig(BaseSettings):
    """数据库配置"""
    URL: str = "mysql+aiomysql://user:password@localhost:3306/dbname?charset=utf8mb4"
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    ECHO: int = 0
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class ServerConfig(BaseSettings):
    """服务器配置"""
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    CORS_ORIGINS: List[str] = ["*"]
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class LLMConfig(BaseSettings):
    """LLM相关配置"""
    MODEL: str = "gpt-3.5-turbo"
    API_KEY: str = "your-api-key"
    API_BASE: str = "https://api.openai.com/v1"
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class MCPItem(BaseSettings):
    """工具配置"""
    NAME: str = Field(alias="name")
    DESCRIPTION: str = ""
    ENABLED: bool = True
    TOOLS: List[str] = Field(default_factory=list)
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class MCPConfig(BaseSettings):
    """MCP服务配置"""
    URL: str = "http://localhost:8000"
    LIST: List[MCPItem] = Field(default_factory=List[MCPItem], alias="list")
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class ChatConfig(BaseSettings):
    """聊天配置"""
    MCP_SERVER_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class AuthConfig(BaseSettings):
    """认证配置"""
    SECRET_KEY: str = ''
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    EXCLUDE_PATHS_PREFIX : List[str] = []
    EXCLUDE_PATHS : List[str] = []
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class UsersConfig(BaseSettings):
    """用户服务配置"""
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 32
    USERNAME_MIN_LENGTH: int = 5
    USERNAME_MAX_LENGTH: int = 50

    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())


class MilvusConfig(BaseSettings):
    """Milvus 配置"""
    URI: str = "http://localhost:19530"
    TOKEN: str = "root:Milvus"
    DB_NAME:  str = "default"
    COLLECTION: str = "default"
    
    DIMENSION: int = 1536
    INDEX_FILE_SIZE: int = 1024
    METRIC_TYPE: str = "L2"
    INDEX_TYPE: str = "HNSW"


class Settings(BaseSettings):
    """应用程序配置"""
    APP: AppConfig = Field(default_factory=AppConfig, alias="app")
    LOG: LogConfig = Field(default_factory=LogConfig, alias="log")
    DB: DatabaseConfig = Field(default_factory=DatabaseConfig, alias="db")
    SERVER: ServerConfig = Field(default_factory=ServerConfig, alias="server")
    LLM: LLMConfig = Field(default_factory=LLMConfig, alias="llm")
    MCP: MCPConfig = Field(default_factory=MCPConfig, alias="mcp")
    AUTH: AuthConfig = Field(default_factory=AuthConfig, alias="auth")
    USERS: UsersConfig = Field(default_factory=UsersConfig, alias="users")
    CHAT: ChatConfig = Field(default_factory=ChatConfig, alias="chat")
    MILVUS: MilvusConfig = Field(default_factory=MilvusConfig, alias="milvus")
    
    model_config = SettingsConfigDict(alias_generator=lambda x: x.lower())
    
    @classmethod
    def load(cls):
        from config.loader import load_config
        cfg = load_config()
        return cls(**load_config())


settings = Settings.load()

del Settings
