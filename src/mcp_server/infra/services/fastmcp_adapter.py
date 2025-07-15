"""
FastMCP适配器 - 将领域对象适配到FastMCP库
"""
import asyncio
import logging
from typing import Dict, Any, List, Callable, Optional

from fastmcp import FastMCP

from ...domain.models.tool import ToolEntity, MCPEntity

logger = logging.getLogger(__name__)


class FastMCPAdapter:
    """FastMCP适配器类 - 将领域实体适配到FastMCP库"""
    
    @classmethod
    async def create_from_entity(cls, entity: MCPEntity, lifespan=None) -> FastMCP:
        """从MCP实体创建FastMCP实例"""
        mcp = FastMCP(name=entity.name, lifespan=lifespan)
        
        # 添加工具
        for tool_name, tool_entity in entity.tools.items():
            logger.info(f"添加工具: {tool_name=}")
            mcp.add_tool(
                fn=tool_entity.function,
                name=tool_name,
                description=tool_entity.description,
                tags=set(tool_entity.tags) if tool_entity.tags else set()
            )
        
        # 挂载子MCP
        for sub_name, sub_entity in entity.sub_mcps.items():
            logger.info(f"正在挂载子MCP: {sub_name}")
            sub_mcp = await cls.create_from_entity(sub_entity)
            mcp.mount(sub_name, sub_mcp)
        
        return mcp
    
    @classmethod
    def to_entity(cls, mcp: FastMCP) -> MCPEntity:
        """从FastMCP实例创建MCP实体"""
        entity = MCPEntity(name=mcp.name)
        
        # 转换工具
        tools = asyncio.run(mcp.get_tools())
        for name, tool in tools.items():
            tool_entity = ToolEntity(
                name=name,
                description=tool.description or "",
                function=tool.func,
                tags=list(tool.tags) if tool.tags else []
            )
            entity.add_tool(tool_entity)
        
        # 转换子MCP
        # 注意：FastMCP库可能没有直接访问子MCP的方法
        # 这里需要根据实际情况调整
        
        return entity
    
    @staticmethod
    async def _create_tool_wrapper(tool: ToolEntity) -> Callable:
        """创建工具函数包装器"""
        async def wrapper(*args, **kwargs):
            try:
                return await tool.execute(*args, **kwargs)
            except Exception as e:
                logger.error(f"执行工具 {tool.name} 失败: {e}")
                raise
        
        return wrapper
    
    @classmethod
    async def check_mcp(cls, mcp: FastMCP) -> None:
        """检查MCP内容"""
        tools = await mcp.get_tools()
        resources = await mcp.get_resources()
        templates = await mcp.get_resource_templates()
        
        logger.info(
            f"{len(tools)} 个工具: {', '.join([t.name for t in tools.values()])}"
        )
        logger.info(
            f"{len(resources)} 个资源: {', '.join([r.name for r in resources.values()])}"
        )
        logger.info(
            f"{len(templates)} 个资源模板: {', '.join([t.name for t in templates.values()])}"
        ) 