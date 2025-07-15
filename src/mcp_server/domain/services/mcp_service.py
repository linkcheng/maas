"""
MCP领域服务 - 提供MCP核心业务逻辑
"""
from typing import List, Dict, Any, Optional


from mcp_server.domain.models.tool import ToolEntity, MCPEntity
from mcp_server.domain.repositories.tool_repository import MCPRepositoryInterface


class MCPDomainService:
    """MCP领域服务类"""
    
    def __init__(self, mcp_repository: MCPRepositoryInterface):
        self.mcp_repository = mcp_repository
    
    async def create_mcp(self, name: str, description: str = "") -> MCPEntity:
        """创建一个新的MCP实体"""
        mcp = MCPEntity(name=name, description=description)
        return await self.mcp_repository.create_mcp(mcp)
    
    async def mount_sub_mcp(self, parent_name: str, name: str, sub_mcp: MCPEntity) -> bool:
        """将子MCP挂载到父MCP"""
        return await self.mcp_repository.mount_sub_mcp(parent_name, name, sub_mcp)
    
    async def add_tool_to_mcp(self, mcp_name: str, tool: ToolEntity) -> Optional[MCPEntity]:
        """向MCP添加工具"""
        mcp = await self.mcp_repository.get_mcp(mcp_name)
        if not mcp:
            return None
        
        mcp.add_tool(tool)
        return mcp
    
    async def execute_tool(self, mcp_name: str, tool_name: str, **kwargs) -> Any:
        """执行MCP中的工具"""
        mcp = await self.mcp_repository.get_mcp(mcp_name)
        if not mcp:
            raise ValueError(f"MCP {mcp_name} 不存在")
            
        if tool_name not in mcp.tools:
            raise ValueError(f"工具 {tool_name} 在MCP {mcp_name} 中不存在")
            
        tool = mcp.tools[tool_name]
        return await tool.execute(**kwargs) 