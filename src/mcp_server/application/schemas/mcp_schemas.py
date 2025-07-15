"""
MCP数据模型 - Pydantic模型用于数据验证和序列化
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from ...domain.models.tool import ToolEntity, MCPEntity


class ToolSchema(BaseModel):
    """工具数据模型"""
    name: str
    description: str = ""
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    
    @classmethod
    def from_entity(cls, entity: ToolEntity) -> 'ToolSchema':
        """从实体创建模型"""
        return cls(
            name=entity.name,
            description=entity.description,
            tags=entity.tags,
            metadata=entity.metadata,
            created_at=entity.created_at
        )


class MCPSchema(BaseModel):
    """MCP数据模型"""
    name: str
    description: str = ""
    tools: List[ToolSchema] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @classmethod
    def from_entity(cls, entity: MCPEntity) -> 'MCPSchema':
        """从实体创建模型"""
        return cls(
            name=entity.name,
            description=entity.description,
            tools=[ToolSchema.from_entity(tool) for tool in entity.tools.values()],
            metadata=entity.metadata
        )


class ToolCreate(BaseModel):
    """工具创建请求模型"""
    name: str
    description: str = ""
    tags: List[str] = Field(default_factory=list)


class MCPCreate(BaseModel):
    """MCP创建请求模型"""
    name: str
    description: str = ""


class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool
    error: Optional[str] = None


class ToolResponse(BaseResponse):
    """工具响应模型"""
    data: Optional[ToolSchema] = None


class MCPResponse(BaseResponse):
    """MCP响应模型"""
    data: Optional[MCPSchema] = None


class ToolListResponse(BaseResponse):
    """工具列表响应模型"""
    data: List[ToolSchema] = Field(default_factory=list)
    total: int = 0


class MCPListResponse(BaseResponse):
    """MCP列表响应模型"""
    data: List[MCPSchema] = Field(default_factory=list)
    total: int = 0


class ExecuteToolRequest(BaseModel):
    """执行工具请求模型"""
    mcp_name: str
    tool_name: str
    parameters: Dict[str, Any] = Field(default_factory=dict) 