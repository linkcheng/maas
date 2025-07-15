"""
MCP Server 数据库模型
"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON, Integer, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Dict, Any, List

from infra.database import Base


class MCPModel(Base):
    """MCP数据库模型"""
    __tablename__ = "mcp_servers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=False)
    
    # 关联关系
    tools: Mapped[List["MCPToolModel"]] = relationship("MCPToolModel", back_populates="mcp", cascade="all, delete-orphan")


class MCPToolModel(Base):
    """MCP工具数据库模型"""
    __tablename__ = "mcp_tools"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    mcp_id: Mapped[int] = mapped_column(Integer, nullable=False)
    function_name: Mapped[str] = mapped_column(String(200), nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=False)
    
    # 关联关系
    mcp: Mapped["MCPModel"] = relationship("MCPModel", back_populates="tools")