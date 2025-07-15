"""
工具领域模型 - 定义MCP服务中的工具实体
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Callable, List, Optional
from mcp.types import (
    AnyFunction,
    EmbeddedResource,
    GetPromptResult,
    ImageContent,
    TextContent,
    ToolAnnotations,
)

@dataclass
class ToolEntity:
    """工具实体类，代表MCP中的工具"""
    name: str
    description: str = ""
    function: AnyFunction = None
    tags: List[str] = field(default_factory=list)
    annotations: ToolAnnotations | dict[str, Any] | None = None,
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    async def execute(self, **kwargs) -> Any:
        """执行工具函数"""
        if not self.function:
            raise ValueError(f"工具 {self.name} 没有关联的函数实现")
        return self.function(**kwargs)


@dataclass
class MCPEntity:
    """MCP实体类，代表一个MCP服务单元"""
    name: str
    description: str = ""
    tools: Dict[str, ToolEntity] = field(default_factory=dict)
    sub_mcps: Dict[str, 'MCPEntity'] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_tool(self, tool: ToolEntity) -> None:
        """添加工具到MCP"""
        self.tools[tool.name] = tool
    
    def mount(self, name: str, sub_mcp: 'MCPEntity') -> None:
        """挂载子MCP"""
        self.sub_mcps[name] = sub_mcp 