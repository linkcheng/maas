from typing import List, Dict, Any, Optional
from .vector_store import MilvusClient
from .embedding import EmbeddingService

class VectorStoreService:
    """向量存储服务类"""
    
    def __init__(self):
        """初始化向量存储服务"""
        self.client = MilvusClient()
        self.embedding_service = EmbeddingService()
        
    async def initialize(self) -> None:
        """初始化服务"""
        await self.client.connect()
        await self.client.create_collection()
        
    async def store_document_chunks(
        self,
        document_id: str,
        chunks: List[str],
        chunk_ids: Optional[List[str]] = None
    ) -> None:
        """存储文档块
        
        Args:
            document_id: 文档ID
            chunks: 文档块列表
            chunk_ids: 文档块ID列表，如果为None则自动生成
        """
        # 获取文档块的向量嵌入
        embeddings = await self.embedding_service.get_embeddings(chunks)
        
        # 如果没有提供chunk_ids，则生成
        if chunk_ids is None:
            chunk_ids = [f"{document_id}_{i}" for i in range(len(chunks))]
            
        # 存储到Milvus
        await self.client.insert(
            ids=chunk_ids,
            document_ids=[document_id] * len(chunks),
            embeddings=embeddings
        )
        
    async def search_similar_chunks(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """搜索相似文档块
        
        Args:
            query: 查询文本
            limit: 返回结果数量限制
            
        Returns:
            相似文档块列表
        """
        # 获取查询文本的向量嵌入
        embedding = await self.embedding_service.get_embedding(query)
        
        # 搜索相似向量
        results = await self.client.search(embedding, limit)
        return results
        
    async def close(self) -> None:
        """关闭服务"""
        await self.client.close() 