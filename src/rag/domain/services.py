from typing import List, Optional
from ..domain.entities import Document, Chunk, Query
from ..domain.repositories import DocumentRepository, ChunkRepository, QueryRepository
from ..infra.vector_store import search_similar
from ..infra.embedding import EmbeddingService

class RAGDomainService:
    """RAG Domain服务"""
    
    def __init__(
        self,
        document_repo: DocumentRepository,
        chunk_repo: ChunkRepository,
        query_repo: QueryRepository,
        # embedding_service: Optional[EmbeddingService] = None
    ):
        self.document_repo = document_repo
        self.chunk_repo = chunk_repo
        self.query_repo = query_repo
        # self.embedding_service = embedding_service or EmbeddingService()
    
    async def split(self, document: Document) -> List[Chunk]:
        """处理文档"""
        saved_doc = await self.document_repo.save(document)
        
        chunks = self._split_document(document)
        
        return chunks
    
    async def search(self, query: Query) -> List[Chunk]:
        """搜索相关文档块"""
        # 生成查询的向量嵌入
        # query.embedding = await self.embedding_service.get_embedding(query.content)
        
        # 保存查询
        saved_query = await self.query_repo.save(query)
        
        # 搜索相似向量
        similar_chunk_ids = await search_similar(saved_query.embedding)
        
        # 获取完整的分块信息
        chunks = []
        for chunk_id in similar_chunk_ids:
            chunk = await self.chunk_repo.get_by_id(chunk_id)
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def _split_document(self, document: Document) -> List[Chunk]:
        """文档分块（示例实现）"""
        # TODO: 实现更复杂的分块策略
        chunks = []
        content = document.content
        chunk_size = 1000  # 示例：每1000个字符一个块
        
        for i in range(0, len(content), chunk_size):
            chunk = Chunk(
                id=f"{document.id}_chunk_{i//chunk_size}",
                document_id=document.id,
                content=content[i:i+chunk_size],
                metadata=document.metadata
            )
            chunks.append(chunk)
        
        return chunks 