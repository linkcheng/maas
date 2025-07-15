"""
MCP Server 数据库仓储实现
"""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..domain.models.tool import MCPEntity, ToolEntity
from ..domain.repositories.tool_repository import MCPRepositoryInterface
from .models import MCPModel, MCPToolModel


class SQLMCPRepository(MCPRepositoryInterface):
    """MCP SQL仓储实现"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_entity(self, model: MCPModel) -> MCPEntity:
        """将数据库模型转换为领域实体"""
        if not model:
            return None
        
        entity = MCPEntity(
            name=model.name,
            description=model.description
        )
        
        # 转换工具
        for tool_model in model.tools:
            if tool_model.enabled:
                tool = ToolEntity(
                    name=tool_model.name,
                    description=tool_model.description,
                    function=None,  # 函数需要从工具注册表中获取
                    tags=tool_model.tags,
                    metadata=tool_model.metadata
                )
                entity.add_tool(tool)
        
        return entity
    
    def _to_model(self, entity: MCPEntity) -> MCPModel:
        """将领域实体转换为数据库模型"""
        return MCPModel(
            name=entity.name,
            description=entity.description,
            enabled=True
        )
    
    async def create_mcp(self, mcp: MCPEntity) -> MCPEntity:
        """创建MCP"""
        model = self._to_model(mcp)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_mcp(self, name: str) -> Optional[MCPEntity]:
        """获取MCP"""
        stmt = select(MCPModel).options(
            selectinload(MCPModel.tools)
        ).where(MCPModel.name == name)
        
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        return self._to_entity(model)
    
    async def list_mcps(self) -> List[MCPEntity]:
        """列出所有MCP"""
        stmt = select(MCPModel).options(
            selectinload(MCPModel.tools)
        ).where(MCPModel.enabled == True)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def update_mcp(self, mcp: MCPEntity) -> MCPEntity:
        """更新MCP"""
        stmt = select(MCPModel).where(MCPModel.name == mcp.name)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        model.description = mcp.description
        await self.session.flush()
        await self.session.refresh(model)
        
        return self._to_entity(model)
    
    async def delete_mcp(self, name: str) -> bool:
        """删除MCP"""
        stmt = select(MCPModel).where(MCPModel.name == name)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        model.enabled = False
        await self.session.flush()
        return True
    
    async def mount_sub_mcp(self, parent_name: str, name: str, sub_mcp: MCPEntity) -> bool:
        """将子MCP挂载到父MCP"""
        # 这里可以实现层级结构，暂时简化为创建新的MCP
        await self.create_mcp(sub_mcp)
        return True
    
    async def add_tool_to_mcp(self, mcp_name: str, tool: ToolEntity) -> bool:
        """向MCP添加工具"""
        # 获取MCP
        stmt = select(MCPModel).where(MCPModel.name == mcp_name)
        result = await self.session.execute(stmt)
        mcp_model = result.scalar_one_or_none()
        
        if not mcp_model:
            return False
        
        # 创建工具模型
        tool_model = MCPToolModel(
            name=tool.name,
            description=tool.description,
            mcp_id=mcp_model.id,
            function_name=tool.function.__name__ if tool.function else "",
            tags=tool.tags,
            metadata=tool.metadata
        )
        
        self.session.add(tool_model)
        await self.session.flush()
        return True