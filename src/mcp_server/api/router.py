"""
MCP API路由 - FastAPI路由定义
"""
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException

from mcp_server.application.services.mcp_application_service import MCPApplicationService
from mcp_server.application.schemas.mcp_schemas import (
    ToolSchema, MCPSchema, ToolResponse, MCPResponse,
    ToolListResponse, MCPListResponse, ExecuteToolRequest
)
from mcp_server.domain.services.mcp_service import MCPDomainService
from mcp_server.infra.repo.mcp_repository import InMemoryMCPRepository

# 创建路由
router = APIRouter()

# 依赖注入
async def get_mcp_service():
    """获取MCP应用服务实例"""
    mcp_repo = InMemoryMCPRepository()
    domain_service = MCPDomainService(mcp_repo)
    return MCPApplicationService(domain_service)

# API路由
@router.get("/", response_model=Dict[str, Any])
async def root():
    """API根路由"""
    return {
        "message": "MCP Server API",
        "version": "1.0.0"
    }

@router.post("/mcps", response_model=MCPResponse)
async def create_mcp(
    mcp_data: Dict[str, Any],
    service: MCPApplicationService = Depends(get_mcp_service)
):
    """创建MCP"""
    return await service.create_mcp(
        name=mcp_data.get("name", ""),
        description=mcp_data.get("description", "")
    )

@router.post("/mcps/{mcp_name}/tools", response_model=ToolResponse)
async def add_tool(
    mcp_name: str,
    tool_data: Dict[str, Any],
    service: MCPApplicationService = Depends(get_mcp_service)
):
    """向MCP添加工具"""
    # 注意：这里简化了实现，实际需要处理function参数
    # 在真实场景中，可能需要通过某种机制注册函数
    return await service.add_tool(
        mcp_name=mcp_name,
        name=tool_data.get("name", ""),
        description=tool_data.get("description", ""),
        function=None,  # 简化实现
        tags=tool_data.get("tags", [])
    )

@router.post("/mcps/{mcp_name}/tools/{tool_name}/execute")
async def execute_tool(
    mcp_name: str,
    tool_name: str,
    request: ExecuteToolRequest,
    service: MCPApplicationService = Depends(get_mcp_service)
):
    """执行工具"""
    if request.mcp_name != mcp_name or request.tool_name != tool_name:
        raise HTTPException(
            status_code=400,
            detail="路径参数与请求体不匹配"
        )
    
    return await service.execute_tool(
        mcp_name=mcp_name,
        tool_name=tool_name,
        **request.parameters
    ) 