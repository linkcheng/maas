"""
MCP仓储实现 - 实现MCP仓储接口
"""
from typing import List, Optional, Dict

from ...domain.models.tool import ToolEntity, MCPEntity
from ...domain.repositories.tool_repository import MCPRepositoryInterface


class InMemoryMCPRepository(MCPRepositoryInterface):
    """内存MCP仓储实现"""
    
    def __init__(self):
        self.mcps: Dict[str, MCPEntity] = {}
    
    async def get_mcp(self, name: str) -> Optional[MCPEntity]:
        """根据名称获取MCP实体"""
        return self.mcps.get(name)
    
    async def create_mcp(self, mcp: MCPEntity) -> MCPEntity:
        """创建MCP实体"""
        self.mcps[mcp.name] = mcp
        return mcp
    
    async def mount_sub_mcp(self, parent_name: str, name: str, sub_mcp: MCPEntity) -> bool:
        """挂载子MCP"""
        parent = self.mcps.get(parent_name)
        if not parent:
            return False
        
        parent.mount(name, sub_mcp)
        return True
    
    async def list_tools_from_mcp(self, mcp_name: str) -> List[ToolEntity]:
        """列出MCP中的所有工具"""
        mcp = self.mcps.get(mcp_name)
        if not mcp:
            return []
        
        return list(mcp.tools.values()) 