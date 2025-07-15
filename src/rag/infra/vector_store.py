from pymilvus import connections, MilvusClient, Collection, FieldSchema, CollectionSchema, DataType
from typing import List, Optional, Dict, Any

from config.settings import settings

class VectorClient:
    """Milvus向量数据库客户端类"""
    
    def __init__(self, uri: str, token: str, db_name: Optional[str] = None, collection: Optional[str] = None):

        self.uri = uri
        self.token = token
        self.db_name = db_name
        self.collection_name = collection
        self.dimension = settings.VECTOR_DIMENSION
        self.client = None
        self.collection = None
        
    async def connect(self) -> None:
        """连接到Milvus服务器"""

        self.client = MilvusClient(
            uri=self.uri,
            token=self.token,
            db_name=self.db_name
        )

            
    async def create_collection(self) -> None:
        """创建集合"""
        try:
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
                FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=100),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dimension)
            ]
            schema = CollectionSchema(fields=fields, description="Document chunks collection")
            self.collection = Collection(name=self.collection_name, schema=schema)
            
            # 创建索引
            index_params = {
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
            self.collection.create_index(field_name="embedding", index_params=index_params)
        except Exception as e:
            raise Exception(f"创建集合失败: {str(e)}")
            
    async def insert(self, ids: List[str], document_ids: List[str], embeddings: List[List[float]]) -> None:
        """插入向量数据
        
        Args:
            ids: 文档块ID列表
            document_ids: 文档ID列表
            embeddings: 向量嵌入列表
        """
        try:
            if not self.collection:
                raise Exception("集合未初始化")
                
            data = [
                ids,
                document_ids,
                embeddings
            ]
            self.collection.insert(data)
        except Exception as e:
            raise Exception(f"插入数据失败: {str(e)}")
            
    async def search(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """搜索相似向量
        
        Args:
            embedding: 查询向量
            limit: 返回结果数量限制
            
        Returns:
            相似文档列表
        """
        try:
            if not self.collection:
                raise Exception("集合未初始化")
                
            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 10}
            }
            results = self.collection.search(
                data=[embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                output_fields=["id", "document_id"]
            )
            
            return [
                {
                    "id": hit.entity.get('id'),
                    "document_id": hit.entity.get('document_id'),
                    "distance": hit.distance
                }
                for hit in results[0]
            ]
        except Exception as e:
            raise Exception(f"搜索失败: {str(e)}")
            
    async def close(self) -> None:
        """关闭连接"""
        try:
            if self.collection:
                self.collection.release()
            connections.disconnect("default")
        except Exception as e:
            raise Exception(f"关闭连接失败: {str(e)}")

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "document_chunks"
DIMENSION = 1536  # 向量维度，根据使用的嵌入模型调整

def init_milvus():
    """初始化Milvus连接"""
    connections.connect(
        alias="default",
        host=MILVUS_HOST,
        port=MILVUS_PORT
    )



def create_collection():
    """创建集合"""
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
        FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
    ]
    schema = CollectionSchema(fields=fields, description="Document chunks collection")
    collection = Collection(name=COLLECTION_NAME, schema=schema)
    
    # 创建索引
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1024}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    return collection

def get_collection() -> Collection:
    """获取集合"""
    return Collection(COLLECTION_NAME)

async def search_similar(embedding: List[float], limit: int = 5) -> List[str]:
    """搜索相似向量"""
    collection = get_collection()
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10}
    }
    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param=search_params,
        limit=limit,
        output_fields=["id", "document_id"]
    )
    return [hit.entity.get('id') for hit in results[0]] 

