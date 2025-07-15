"""MCP Server Package

基于FastAPI和领域驱动设计的MCP服务器模块
"""
import logging

from fastmcp import FastMCP
from config.settings import settings
from mcp_server.infra.repo.mcp_repository import InMemoryMCPRepository
from mcp_server.infra.services.fastmcp_adapter import FastMCPAdapter

from mcp_server.domain.models.tool import MCPEntity
from mcp_server.domain.services.mcp_service import MCPDomainService
from mcp_server.domain.services.tool_factory import ToolRegistry


logger = logging.getLogger(__name__)

async def init_mcp(mcp_svc: MCPDomainService) -> MCPEntity:
    main_mcp = await mcp_svc.create_mcp(name="Main", description="Main MCP Server")
    
    for config in settings.MCP.LIST:
        logger.info(f"正在创建MCP工具：{config.NAME}")
        if config.ENABLED:
            sub_mcp = await mcp_svc.create_mcp(name=config.NAME, description=config.DESCRIPTION)
            
            for tool_name in config.TOOLS:
                logger.info(f"正在创建MCP工具：{config.NAME} - {tool_name}")
                tool = ToolRegistry.get_tool(tool_name)
                if not tool:
                    raise ValueError(f"未找到工具：{tool_name}")    
                sub_mcp.add_tool(tool)
                
            await mcp_svc.mount_sub_mcp(main_mcp.name, sub_mcp.name, sub_mcp)
            logger.info(f"已挂在 MCP: {config.NAME}")

    return main_mcp


async def init_fastmcp_app():
    logger.info("初始化MCP APP")
    
    main_mcp_entity = await init_mcp(MCPDomainService(InMemoryMCPRepository()))
    main_mcp: FastMCP = await FastMCPAdapter.create_from_entity(main_mcp_entity)
    mcp_app = main_mcp.http_app(path="/mcp")
    
    logger.info("MCP APP 初始化完成")
    return mcp_app
