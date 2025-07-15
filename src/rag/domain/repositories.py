from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Document, Chunk, Query

class DocumentRepository(ABC):
    """文档仓储接口"""
    
    @abstractmethod
    async def save(self, document: Document) -> Document:
        """保存文档"""
        pass
    
    @abstractmethod
    async def get_by_id(self, document_id: str) -> Optional[Document]:
        """根据ID获取文档"""
        pass
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """获取所有文档"""
        pass

class ChunkRepository(ABC):
    """文档分块仓储接口"""
    
    @abstractmethod
    async def save(self, chunk: Chunk) -> Chunk:
        """保存分块"""
        pass
    
    @abstractmethod
    async def get_by_id(self, chunk_id: str) -> Optional[Chunk]:
        """根据ID获取分块"""
        pass
    
    @abstractmethod
    async def search_similar(self, embedding: List[float], limit: int = 5) -> List[Chunk]:
        """搜索相似分块"""
        pass

class QueryRepository(ABC):
    """查询仓储接口"""
    
    @abstractmethod
    async def save(self, query: Query) -> Query:
        """保存查询"""
        pass
    
    @abstractmethod
    async def get_by_id(self, query_id: str) -> Optional[Query]:
        """根据ID获取查询"""
        pass 