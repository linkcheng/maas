"""
工具仓储接口 - 定义工具实体的存储和检索接口
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from ..models.tool import ToolEntity, MCPEntity


class ToolRepositoryInterface(ABC):
    """工具仓储接口"""
    
    @abstractmethod
    async def list_tools(self) -> List[ToolEntity]:
        """获取所有工具列表"""
        pass
    
    @abstractmethod
    async def get_tool(self, name: str) -> Optional[ToolEntity]:
        """根据名称获取工具"""
        pass
    
    @abstractmethod
    async def add_tool(self, tool: ToolEntity) -> ToolEntity:
        """添加工具"""
        pass
    
    @abstractmethod
    async def remove_tool(self, name: str) -> bool:
        """删除工具"""
        pass


class MCPRepositoryInterface(ABC):
    """MCP仓储接口"""
    
    @abstractmethod
    async def get_mcp(self, name: str) -> Optional[MCPEntity]:
        """根据名称获取MCP实体"""
        pass
    
    @abstractmethod
    async def create_mcp(self, mcp: MCPEntity) -> MCPEntity:
        """创建MCP实体"""
        pass
    
    @abstractmethod
    async def mount_sub_mcp(self, parent_name: str, name: str, sub_mcp: MCPEntity) -> bool:
        """挂载子MCP"""
        pass
    
    @abstractmethod
    async def list_tools_from_mcp(self, mcp_name: str) -> List[ToolEntity]:
        """列出MCP中的所有工具"""
        pass 