# """
# Chat Module for MCP Server

# 这是一个使用FastAPI和SQLAlchemy实现的聊天模块，基于领域驱动设计(DDD)的思想构建。
# """

# __version__ = "1.0.0"

# # 导出领域模型
# from .domain.models.chat import (
#     SourceEntity,
#     PromptEntity,
#     ToolEntity,
#     ChatEntity,
#     ChatDataEntity,
#     ChatToolEntity
# )
# from .domain.models.enums import SourceType, PromptType, Role, ContentType

# # 导出应用层模型
# from .application.schemas import (
#     Source, SourceCreate, SourceUpdate,
#     Prompt, PromptCreate, PromptUpdate,
#     Tool, ToolCreate, ToolUpdate,
#     Chat, ChatCreate, ChatUpdate,
#     ChatData, ChatDataCreate,
#     ChatTool, ChatToolCreate,
#     StreamResponse
# )

# # 导出API路由
# from .interfaces.api.router import router as chat_router

# __all__ = [
#     # 领域实体
#     'SourceEntity',
#     'PromptEntity',
#     'ToolEntity',
#     'ChatEntity',
#     'ChatDataEntity',
#     'ChatToolEntity',
#     # 枚举
#     'SourceType',
#     'PromptType',
#     'Role',
#     'ContentType',
#     # 应用模型
#     'Source',
#     'SourceCreate',
#     'SourceUpdate',
#     'Prompt',
#     'PromptCreate',
#     'PromptUpdate',
#     'Tool',
#     'ToolCreate',
#     'ToolUpdate',
#     'Chat',
#     'ChatCreate',
#     'ChatUpdate',
#     'ChatData',
#     'ChatDataCreate',
#     'ChatTool',
#     'ChatToolCreate',
#     'StreamResponse',
#     # 路由
#     'chat_router'
# ]
