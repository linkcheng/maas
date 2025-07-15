import logging
from typing import Annotated
from pydantic import Field

from mcp_server.domain.services.tool_factory import ToolRegistry

logger = logging.getLogger(__name__)

@ToolRegistry.register(
    name="get_data_asset",
    description="读取数据资产抽样数据",
    tags=["data_asset", "read_data"]
)
def get_data_asset(
    asset_id: Annotated[str, Field(description="数据资产Id")],
    order_id: Annotated[str, Field(description="订单Id")],
    limit: Annotated[int, Field(description="一次读取的数据量，默认为 5 条", default=5)] = 5,
) -> Annotated[list[dict], Field(description="数据资产数据信息")]:
    """读取数据资产抽样数据"""

    import os
    from data_assets import DataAssets
    
    logger.info(f"{os.environ.get('DATA_URL')}")
    
    original_order_id = os.environ.get("ORDER_ID") 
    
    os.environ["ORDER_ID"] = order_id
    data = DataAssets(asset_id, logger=logger).read()
    
    if original_order_id:
        os.environ["ORDER_ID"] = original_order_id
    else:
        os.environ.pop("ORDER_ID")
    return data.head(limit).to_dict("records")


@ToolRegistry.register(
    name="add",
    description="加法演示工具",
    tags=["demo", "math"]
)
def add(a: int, b: int) -> int:
    """加法演示工具"""
    return a + b 
