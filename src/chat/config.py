"""
Chat模块的配置。
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from ..config.settings import settings


class ChatModelConfig(BaseModel):
    """聊天模型配置"""
    name: str
    api_key: str
    api_base: str = "https://api.openai.com/v1"
    parameters: Optional[Dict[str, Any]] = None


class ChatServiceConfig(BaseModel):
    """聊天服务配置"""
    default_model: str = "gpt-3.5-turbo"
    available_models: List[ChatModelConfig] = []
    max_history_length: int = 20
    max_tokens: int = 4096
    temperature: float = 0.7
    api_timeout: int = 60
    mcp_server_url: str = "http://localhost:8000"


# 聊天模块的默认配置
chat_config = ChatServiceConfig(
    default_model = settings.LLM.MODEL,
    available_models = [
        ChatModelConfig(
            name = settings.LLM.MODEL,
            api_key = settings.LLM.API_KEY,
            api_base = settings.LLM.API_BASE,
            parameters = {
                "temperature": 0.7,
                "max_tokens": 4096
            }
        )
    ],
    mcp_server_url = settings.MCP.SERVER_URL
)


def get_chat_config() -> ChatServiceConfig:
    """获取聊天配置"""
    return chat_config


def configure_chat(config: Dict[str, Any]) -> None:
    """
    配置聊天服务
    
    Args:
        config: 配置字典
    """
    global chat_config
    
    # 更新基本配置
    for key, value in config.items():
        if key != 'available_models' and hasattr(chat_config, key):
            setattr(chat_config, key, value)
    
    # 更新模型配置
    if 'available_models' in config:
        models = []
        for model_config in config['available_models']:
            models.append(ChatModelConfig(**model_config))
        chat_config.available_models = models 