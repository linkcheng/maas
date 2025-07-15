"""
应用层数据模型。
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    """文档实体"""
    content: str = Field(..., description="文档内容")
    metadata: dict = Field(default_factory=dict, description="文档元数据")


class Chunk(BaseModel):
    """文档分块实体"""
    id: str = Field(..., description="分块唯一标识")
    document_id: str = Field(..., description="所属文档ID")
    content: str = Field(..., description="分块内容")
    embedding: Optional[List[float]] = Field(None, description="向量嵌入")
    metadata: dict = Field(default_factory=dict, description="分块元数据")


class Query(BaseModel):
    """查询实体"""
    id: str = Field(..., description="查询唯一标识")
    content: str = Field(..., description="查询内容")
    embedding: Optional[List[float]] = Field(None, description="查询向量嵌入")
