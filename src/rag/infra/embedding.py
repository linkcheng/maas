from typing import List, Optional
import litellm
from ..infra.config import get_settings

class EmbeddingService:
    """向量嵌入服务"""
    
    def __init__(self, model_name: Optional[str] = None):
        settings = get_settings()
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.dimension = settings.VECTOR_DIMENSION
    
    async def get_embedding(self, text: str) -> List[float]:
        """获取文本的向量嵌入"""
        try:
            response = await litellm.aembedding(
                model=self.model_name,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"获取向量嵌入失败: {str(e)}")
    
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """批量获取文本的向量嵌入"""
        try:
            response = await litellm.aembedding(
                model=self.model_name,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise Exception(f"批量获取向量嵌入失败: {str(e)}") 