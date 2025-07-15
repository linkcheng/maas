"""
MCP应用服务 - 协调领域对象，提供应用功能
"""
import logging
from typing import List, Dict, Any, Optional, Callable

from ...domain.models.tool import ToolEntity, MCPEntity
from ...domain.services.mcp_service import MCPDomainService
from ..schemas.mcp_schemas import ToolSchema, MCPSchema, ToolResponse, MCPResponse

logger = logging.getLogger(__name__)

class MCPApplicationService:
    """MCP应用服务类"""
    
    def __init__(self, mcp_domain_service: MCPDomainService):
        self.mcp_domain_service = mcp_domain_service
    
    async def create_mcp(self, name: str, description: str = "") -> MCPResponse:
        """创建MCP实例"""
        try:
            mcp_entity = await self.mcp_domain_service.create_mcp(name, description)
            return MCPResponse(
                success=True,
                data=MCPSchema.from_entity(mcp_entity)
            )
        except Exception as e:
            logger.error(f"创建MCP失败: {e}")
            return MCPResponse(
                success=False,
                error=f"创建MCP失败: {str(e)}"
            )
    
    async def add_tool(self, mcp_name: str, name: str, function: Callable,
                       description: str = "", tags: List[str] = None) -> ToolResponse:
        """添加工具到MCP"""
        try:
            # 创建工具实体
            tool_entity = ToolEntity(
                name=name,
                description=description,
                function=function,
                tags=tags or []
            )
            
            # 添加到MCP
            mcp = await self.mcp_domain_service.add_tool_to_mcp(mcp_name, tool_entity)
            if not mcp:
                return ToolResponse(
                    success=False,
                    error=f"MCP {mcp_name} 不存在"
                )
            
            return ToolResponse(
                success=True,
                data=ToolSchema.from_entity(tool_entity)
            )
        except Exception as e:
            logger.error(f"添加工具失败: {e}")
            return ToolResponse(
                success=False,
                error=f"添加工具失败: {str(e)}"
            )
    
    async def mount_sub_mcp(self, parent_name: str, name: str, sub_mcp: MCPEntity) -> MCPResponse:
        """挂载子MCP"""
        try:
            success = await self.mcp_domain_service.mount_sub_mcp(parent_name, name, sub_mcp)
            if not success:
                return MCPResponse(
                    success=False,
                    error=f"挂载子MCP失败，父MCP {parent_name} 可能不存在"
                )
                
            return MCPResponse(
                success=True,
                data=MCPSchema.from_entity(sub_mcp)
            )
        except Exception as e:
            logger.error(f"挂载子MCP失败: {e}")
            return MCPResponse(
                success=False,
                error=f"挂载子MCP失败: {str(e)}"
            )
    
    async def execute_tool(self, mcp_name: str, tool_name: str, **kwargs) -> Dict[str, Any]:
        """执行工具"""
        try:
            result = await self.mcp_domain_service.execute_tool(mcp_name, tool_name, **kwargs)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            logger.error(f"执行工具失败: {e}")
            return {
                "success": False,
                "error": f"执行工具失败: {str(e)}"
            } 