from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from rag.domain.services import RAGDomainService
from rag.application.schemas import Document, Query, Chunk
from rag.application.services import RAGService
from infra.database import get_session
from rag.infra.repositories import (
    SQLDocumentRepository,
    SQLChunkRepository,
    SQLQueryRepository
)
from rag.infra.embedding import EmbeddingService


router = APIRouter()

def get_rag_service(db: AsyncSession = Depends(get_session)) -> RAGService:
    """获取RAG服务实例"""
    document_repo = SQLDocumentRepository(db)
    chunk_repo = SQLChunkRepository(db)
    query_repo = SQLQueryRepository(db)
    embedding_svc = EmbeddingService()
    rag_domain_svc = RAGDomainService(document_repo, chunk_repo, query_repo)
    return RAGService(rag_domain_svc, embedding_svc)

@router.post("/documents", response_model=Document)
async def create_document(
    document: Document,
    rag_service: RAGService = Depends(get_rag_service)
):
    """创建并处理文档"""
    try:
        return await rag_service.process_document(document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[Chunk])
async def search_documents(
    query: Query,
    rag_service: RAGService = Depends(get_rag_service)
):
    """搜索相关文档块"""
    try:
        return await rag_service.search(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    rag_service: RAGService = Depends(get_rag_service)
):
    """获取文档详情"""
    try:
        document = await rag_service.document_repo.get_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 