from pymilvus import MilvusClient
from pymilvus import DataType, FunctionType, Function
from pymilvus import AnnSearchRequest
from pymilvus import RRFRanker

def init_milvus() -> MilvusClient:
    """
    初始化 Milvus
    """
    client = MilvusClient(
        uri="http://localhost:19530",
        token="root:Milvus"
    )
    return client

def test_database(client: MilvusClient):

    # 创建数据库
    client.create_database(
        db_name="my_database_1"
    )
    # 列出数据库
    client.list_databases()
    # 获取数据库信息
    client.describe_database(
        db_name="default"
    )
    # 切换数据库
    client.use_database(
        db_name="my_database_1"
    )

    # 创建数据库，设置属性
    client.create_database(
        db_name="my_database_2",
        properties={
            "database.replica.number": 3
        }
    )    
    # 删除数据库
    client.drop_database(
        db_name="my_database_1"
    )
    # 修改数据库属性
    client.alter_database_properties(
        db_name="my_database_1",
        properties={
            "database.max.collections": 10
        }
    )
    # 删除数据库属性
    client.drop_database_properties(
        db_name="my_database_1",
        property_keys=[
            "database.max.collections"
        ]
    )
    
def test_collection(client: MilvusClient):
    
    # 创建schema
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )

    # 添加字段
    schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=5)
    schema.add_field(field_name="my_varchar", datatype=DataType.VARCHAR, max_length=512)
    
    index_params = client.prepare_index_params()

    # 添加索引
    index_params.add_index(
        field_name="my_id",
        index_type="AUTOINDEX"
    )

    index_params.add_index(
        field_name="my_vector", 
        index_type="AUTOINDEX",
        metric_type="COSINE"
    )
    
    # 创建集合 collection 
    client.create_collection(
        collection_name="quick_setup",  
        schema=schema,
        index_params=index_params
    )
    # 列出集合
    res = client.list_collections()
    # 获取集合信息
    res = client.describe_collection(
        collection_name="quick_setup"
    )
    # 重命名集合
    client.rename_collection(
        old_name="quick_setup",
        new_name="my_collection"
    )
    # 修改集合属性
    client.alter_collection_properties(
        collection_name="my_collection",
        properties={"collection.ttl.seconds": 60}
    )
    # 删除集合属性
    client.drop_collection_properties(
        collection_name="my_collection",
        property_keys=[
            "collection.ttl.seconds"
        ]
    )
    # 加载集合
    client.load_collection(
        collection_name="my_collection"
    )
    # 释放集合
    client.release_collection(
        collection_name="my_collection"
    )
    # 查看分区
    res = client.list_partitions(
        collection_name="my_collection"
    )
    # 创建分区
    client.create_partition(
        collection_name="my_collection",
        partition_name="partitionA"
    )
    # 是否存在分区
    res = client.has_partition(
        collection_name="my_collection",
        partition_name="partitionA"
    )
    # 加载分区
    client.load_partitions(
        collection_name="my_collection",
        partition_names=["partitionA"]
    )
    # 释放分区
    client.release_partitions(
        collection_name="my_collection",
        partition_names=["partitionA"]
    )
    # 删除分区
    client.drop_partition(
        collection_name="my_collection",
        partition_name="partitionA"
    )
    # 创建集合别名
    client.create_alias(
        collection_name="my_collection",
        alias="bob"
    )
    # 获取集合别名
    res = client.list_aliases(
        collection_name="my_collection"
    )
    # 查看集合信息
    res = client.describe_alias(
        alias="bob"
    )
    # 修改集合别名
    client.alter_alias(
        collection_name="my_collection",
        alias="alice"
    )
    # 删除集合别名
    client.drop_alias(
        alias="bob"
    )
    # 删除集合
    client.drop_collection(
        collection_name="my_collection"
    )
    

def test_crud(client: MilvusClient):
    schema = client.create_schema()
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=5)
    schema.add_field("color", DataType.VARCHAR, max_length=100)
    
    client.create_collection(
        collection_name="my_collection",
        schema=schema,
    )
    data = [
        {"id": 0, "vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592], "color": "pink_8682"},
        {"id": 1, "vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104], "color": "red_7025"},
        {"id": 2, "vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185, 0.20785793220625592], "color": "orange_6781"},
        {"id": 3, "vector": [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995, 0.95791889146345], "color": "pink_9298"},
        {"id": 4, "vector": [0.4452349528804562, -0.8757026943054742, 0.8220779437047674, 0.46406290649483184, 0.30337481143159106], "color": "red_4794"},
        {"id": 5, "vector": [0.985825131989184, -0.8144651566660419, 0.6299267002202009, 0.1206906911183383, -0.1446277761879955], "color": "yellow_4222"},
        {"id": 6, "vector": [0.8371977790571115, -0.015764369584852833, -0.31062937026679327, -0.562666951622192, -0.8984947637863987], "color": "red_9392"},
        {"id": 7, "vector": [-0.33445148015177995, -0.2567135004164067, 0.8987539745369246, 0.9402995886420709, 0.5378064918413052], "color": "grey_8510"},
        {"id": 8, "vector": [0.39524717779832685, 0.4000257286739164, -0.5890507376891594, -0.8650502298996872, -0.6140360785406336], "color": "white_9381"},
        {"id": 9, "vector": [0.5718280481994695, 0.24070317428066512, -0.3737913482606834, -0.06726932177492717, -0.6980531615588608], "color": "purple_4976"},        
    ]
    res = client.insert(
        collection_name="my_collection",
        data=data
    )

    print(res)
    
    index_params = client.prepare_index_params()

    index_params.add_index(
        field_name="color",               # Name of the "column" you see in queries (the dynamic key).
        index_type="INVERTED",            # Currently only "INVERTED" is supported for indexing JSON fields.
        index_name="color_index",         # Assign a name to this index.
        params={
            "json_path": "color",         # JSON path to the key you want to index.
            "json_cast_type": "varchar"   # Type to which Milvus will cast the extracted values.
        }
    )

    # Create the index
    client.create_index(
        collection_name="my_collection",
        index_params=index_params
    )
    
    query_vector = [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592]

    res = client.search(
        collection_name="my_collection",
        data=[query_vector],
        limit=5,
        # highlight-start
        filter='color like "red%"',
        output_fields=["color"]
        # highlight-end
    )

    print(res)
    
    
    data=[
        {"id": 10, "vector": [0.06998888224297328, 0.8582816610326578, -0.9657938677934292, 0.6527905683627726, -0.8668460657158576], "color": "black_3651"},
        {"id": 11, "vector": [0.6060703043917468, -0.3765080534566074, -0.7710758854987239, 0.36993888322346136, 0.5507513364206531], "color": "grey_2049"},
        {"id": 12, "vector": [-0.9041813104515337, -0.9610546012461163, 0.20033003106083358, 0.11842506351635174, 0.8327356724591011], "color": "blue_6168"},
        {"id": 13, "vector": [0.3202914977909075, -0.7279137773695252, -0.04747830871620273, 0.8266053056909548, 0.8277957187455489], "color": "blue_1672"},
        {"id": 14, "vector": [0.2975811497890859, 0.2946936202691086, 0.5399463833894609, 0.8385334966677529, -0.4450543984655133], "color": "pink_1601"},
        {"id": 15, "vector": [-0.04697464305600074, -0.08509022265734134, 0.9067184632552001, -0.2281912685064822, -0.9747503428652762], "color": "yellow_9925"},
        {"id": 16, "vector": [-0.9363075919673911, -0.8153981031085669, 0.7943039120490902, -0.2093886809842529, 0.0771191335807897], "color": "orange_9872"},
        {"id": 17, "vector": [-0.050451522820639916, 0.18931572752321935, 0.7522886192190488, -0.9071793089474034, 0.6032647330692296], "color": "red_6450"},
        {"id": 18, "vector": [-0.9181544231141592, 0.6700755998126806, -0.014174674636136642, 0.6325780463623432, -0.49662222164032976], "color": "purple_7392"},
        {"id": 19, "vector": [0.11426945899602536, 0.6089190684002581, -0.5842735738352236, 0.057050610092692855, -0.035163433018196244], "color": "pink_4996"}
    ]

    res = client.upsert(
        collection_name="my_collection",
        data=data,
    )

    print(res)

    res = client.delete(
        collection_name="my_collection",
        filter="color in ['red_7025', 'purple_4976']"
    )

    print(res)


def test_search(client: MilvusClient):
    schema = client.create_schema(auto_id=False)
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, description="product id")
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=1000, enable_analyzer=True, description="raw text of product description")
    schema.add_field(field_name="text_dense", datatype=DataType.FLOAT_VECTOR, dim=768, description="text dense embedding")
    schema.add_field(field_name="text_sparse", datatype=DataType.SPARSE_FLOAT_VECTOR, description="text sparse embedding auto-generated by the built-in BM25 function")
    schema.add_field(field_name="image_dense", datatype=DataType.FLOAT_VECTOR, dim=512, description="image dense embedding")

    # 添加 BM25 函数
    bm25_function = Function(
        name="text_bm25_emb",
        input_field_names=["text"],
        output_field_names=["text_sparse"],
        function_type=FunctionType.BM25,
    )
    schema.add_function(bm25_function)
    
    index_params = client.prepare_index_params()

    index_params.add_index(
        field_name="text_dense",
        index_name="text_dense_index",
        index_type="AUTOINDEX",
        metric_type="IP"
    )

    index_params.add_index(
        field_name="text_sparse",
        index_name="text_sparse_index",
        index_type="SPARSE_INVERTED_INDEX",
        metric_type="BM25",
        params={"inverted_index_algo": "DAAT_MAXSCORE"}, # or "DAAT_WAND" or "TAAT_NAIVE"
    )

    index_params.add_index(
        field_name="image_dense",
        index_name="image_dense_index",
        index_type="AUTOINDEX",
        metric_type="IP"
    )
    
    # 创建 Collection 并插入数据
    client.create_collection(
        collection_name="my_collection",
        schema=schema,
        index_params=index_params
    )
    
    data=[
        {
            "id": 0,
            "text": "Red cotton t-shirt with round neck",
            "text_dense": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, ...],
            "image_dense": [0.6366019600530924, -0.09323198122475052, ...]
        },
        {
            "id": 1,
            "text": "Wireless noise-cancelling over-ear headphones",
            "text_dense": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, ...],
            "image_dense": [0.6414180010301553, 0.8976979978567611, ...]
        },
        {
            "id": 2,
            "text": "Stainless steel water bottle, 500ml",
            "dense": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, ...],
            "image_dense": [-0.6901259768402174, 0.6100500332193755, ...]
        }
    ]

    res = client.insert(
        collection_name="my_collection",
        data=data
    )

    # BM25 搜索
    results = client.search(
        collection_name="my_collection",
        data=["headphones"],
        anns_field="text_sparse",
        limit=3
    )
    print(results)

    # 混合查询
    query_text = "white headphones, quiet and comfortable"
    query_dense_vector = [0.3580376395471989, -0.6023495712049978, 0.5142999509918703, ...]
    query_multimodal_vector = [0.015829865178701663, 0.5264158340734488, ...]

    # text semantic search (dense)
    search_param_1 = {
        "data": [query_dense_vector],
        "anns_field": "text_dense",
        "param": {"nprobe": 10},
        "limit": 2
    }
    request_1 = AnnSearchRequest(**search_param_1)

    # full-text search (sparse)
    search_param_2 = {
        "data": [query_text],
        "anns_field": "text_sparse",
        "param": {"drop_ratio_search": 0.2},
        "limit": 2
    }
    request_2 = AnnSearchRequest(**search_param_2)

    # text-to-image search (multimodal)
    search_param_3 = {
        "data": [query_multimodal_vector],
        "anns_field": "image_dense",
        "param": {"nprobe": 10},
        "limit": 2
    }
    request_3 = AnnSearchRequest(**search_param_3)

    reqs = [request_1, request_2, request_3]

    ranker = RRFRanker(100)

    res = client.hybrid_search(
        collection_name="my_collection",
        reqs=reqs,
        ranker=ranker,
        limit=2
    )
    for hits in res:
        print("TopK results:")
        for hit in hits:
            print(hit)


def test_query(client: MilvusClient):
    data = [
            {"id": 0, "vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592], "color": "pink_8682"},
            {"id": 1, "vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104], "color": "red_7025"},
            {"id": 2, "vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185, 0.20785793220625592], "color": "orange_6781"},
            {"id": 3, "vector": [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995, 0.95791889146345], "color": "pink_9298"},
            {"id": 4, "vector": [0.4452349528804562, -0.8757026943054742, 0.8220779437047674, 0.46406290649483184, 0.30337481143159106], "color": "red_4794"},
            {"id": 5, "vector": [0.985825131989184, -0.8144651566660419, 0.6299267002202009, 0.1206906911183383, -0.1446277761879955], "color": "yellow_4222"},
            {"id": 6, "vector": [0.8371977790571115, -0.015764369584852833, -0.31062937026679327, -0.562666951622192, -0.8984947637863987], "color": "red_9392"},
            {"id": 7, "vector": [-0.33445148015177995, -0.2567135004164067, 0.8987539745369246, 0.9402995886420709, 0.5378064918413052], "color": "grey_8510"},
            {"id": 8, "vector": [0.39524717779832685, 0.4000257286739164, -0.5890507376891594, -0.8650502298996872, -0.6140360785406336], "color": "white_9381"},
            {"id": 9, "vector": [0.5718280481994695, 0.24070317428066512, -0.3737913482606834, -0.06726932177492717, -0.6980531615588608], "color": "purple_4976"},
    ]
    
    schema = client.create_schema()
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=5)
    schema.add_field("color", DataType.VARCHAR, max_length=100)
    
    client.create_collection(
        collection_name="my_collection",
        schema=schema
    )
    
    client.insert(
        collection_name="my_collection",
        data=data
    )
    
    res = client.get(
        collection_name="my_collection",
        ids=[0, 1, 2],
        output_fields=["vector", "color"]
    )

    print(res)
    
    res = client.query(
        collection_name="my_collection",
        filter="color like \"red%\"",
        output_fields=["vector", "color"],
        limit=3
    )
    print(res)
    
    res = client.query_iterator(
        collection_name="my_collection",
        filter="color like \"red%\"",
        output_fields=["vector", "color"],
        limit=3
    ) 
    for item in res:
        print(item)


if __name__ == "__main__":
    client = init_milvus() 
    test_query(client)
    client.close()
