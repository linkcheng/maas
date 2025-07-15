from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Text
from .database import Base

class DocumentModel(Base):
    """文档数据库模型"""
    __tablename__ = "documents"

    id = Column(String(100), primary_key=True)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChunkModel(Base):
    """文档分块数据库模型"""
    __tablename__ = "chunks"

    id = Column(String(100), primary_key=True)
    document_id = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class QueryModel(Base):
    """查询数据库模型"""
    __tablename__ = "queries"

    id = Column(String(100), primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow) 