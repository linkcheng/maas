import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.client.transports import SSETransport
from litellm import completion
import ujson

def mcp_client():
    http_url = "http://localhost:8000/api/v1/server/mcp/"

    # Option 1: Inferred transport (default for HTTP URLs)
    client_inferred = Client(http_url)

    # Option 2: Explicit transport (e.g., to add custom headers)
    # headers = {"Authorization": "Bearer mytoken"}
    # transport_explicit = StreamableHttpTransport(url=http_url, headers=headers)
    # client_explicit = Client(transport_explicit)

    async def use_streamable_http_client(client: Client):
        async with client:
            tools = await client.list_tools()
            print(f"Connected via Streamable HTTP, found tools: {tools}")
        
            
            # result = await client.call_tool_mcp("mymcp_add", {"a": 1, "b": 2})
            # print(f"Result: {result}")
            
            result = await client.call_tool_mcp("data-asset_get_data_asset", {"asset_id": "S1909166170532089856", "order_id": "OD25040716492024109", "limit": 2})
            # print(f"Result: {result}")
            return result
            # import ujson
            # print(f"Result: {ujson.loads(result.content[0].text)}")

    return asyncio.run(use_streamable_http_client(client_inferred))
    # asyncio.run(use_streamable_http_client(client_explicit))


def sse_client():

    sse_url = "http://localhost:8000/server/sse"

    transport_explicit = SSETransport(url=sse_url)
    client_explicit = Client(transport_explicit)

    async def use_sse_client(client: Client):
        async with client:
            tools = await client.list_tools()
            print(f"Connected via SSE, found tools: {tools}")
            
            result = await client.call_tool("repeat", {"text": "Hello"})
            print(f"Result: {result}")
            
            result = await client.call_tool_mcp("mymcp_add", {"a": 1, "b": 2})
            print(f"Result: {result}")

    asyncio.run(use_sse_client(client_explicit))



system_prompt = """请生成可直接在 Jupyter Notebook 中执行的 Python 代码，严格遵守以下规范：

#### 1. **数据访问强制要求**
```python
# 必须使用以下方式加载数据（示例模板）
from data_assets import DataAssets  # 私有SDK
df = DataAssets(asset_id="{asset_id}").read()
```

#### 2. **数据资产Id限制**
- 数据资产Id（asset_id）只能是用系统提供的信息，不管用户提供什么，都只能使用系统提供的信息；

#### 3. **第三方包使用限制**
- 在进行数据分析和建模过程中，模型训练预测评估等只能使用 {packages}，不能使用其他包，其他过程没有限制；

#### 4. **代码执行限制**
# 严格遵循的执行流程
# 1. 加载和准备数据
# 2. 创建预处理管道
# 3. 评估基础模型
# 4. 超参数调优
# 5. 评估最佳模型
# 6. 保存模型

#### 5. **模型指标记录**
```python
# 必须使用以下方式进行指标记录
from data_assets.metrics import MetricsCollector
# 记录单个指标
MetricsCollector().record_metric(metric_name, value)
# 记录多个指标
MetricsCollector().record_batch_metrics(metrics_dict)
```
#### 6. **模型结果保存**
```python
# 必须使用以下方式进行结果保存
from data_assets.result import ModelResult
# 创建结果对象
result = ModelResult(
    model_type=self.problem_type,
    model_name=model_name,
    params=params
)
# 添加模型
result.add_model(model)
# 添加指标
result.add_metrics(metrics)
# 添加预测结果
result.add_predictions(
    predictions=y_pred,
    actual_values=y_test
)
# 添加其他而外数据
result.add_info('feature_importance', {})
# 保存结果
result.save()
```

#### 7. **可以调用外部工具辅助获取数据资产信息**
#### 8. **当前数据资产 {asset_id} 属于订单 {order_id}**
#### 9. **如果最终结果返回的是代码，那么只返回代码，不要返回任何解释**
"""

class MCPClient:
    http_url = "http://localhost:8000/server/mcp" 
    client = Client(transport=StreamableHttpTransport(url=http_url))
    
    model = "openai/deepseek-ai/DeepSeek-V3"
    # model = "openai/Qwen/Qwen3-235B-A22B"
    api_key = "sk-vrykswymcidtirbfulkojdwwgevlirmtoiwtiocquuuhhmhv"
    api_base = "https://api.siliconflow.cn/v1"
    @classmethod
    def build_messages(cls):
        asset_id = "S1909166170532089856"
        model_packages = "sklearn,xgboost"
        order_id = "OD25040716492024109"
        messages = [
            {"role": "system", "content": system_prompt.format(asset_id=asset_id, model_packages=model_packages, order_id=order_id)},
            {"role": "assistant", "content": "你好，我是你的助手，有什么可以帮你的吗？"},
            {"role": "user", "content": "请使用当前数据开发分类模型训练代码"},
        ]
        return messages
    
    @classmethod
    def chat(cls):
        messages = cls.build_messages()
        tools = cls.get_tools()

        response = cls.chat_llm(messages, tools)
        print("\nFirst LLM Response:\n", response)
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        print("response_message:", response_message)
        print("\nTool calls:", tool_calls)

        if not tool_calls:
            return response_message.content
      
        messages.append({"role": response_message.role, "content": response_message.content})

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_response = cls.function_call(tool_call)
            print(f"=================function_response:{function_response}")
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        print(f"=================messages:{messages}")
        second_response = cls.chat_llm(messages)
        print("\nSecond LLM response:\n", second_response)
        return second_response.choices[0].message.content
    
    @classmethod
    def function_call(cls, tool_call):
        async def list_tools(client):
            async with client:
                
                tools = await client.call_tool(tool_call.function.name, ujson.loads(tool_call.function.arguments))
                return tools
        ret = asyncio.run(list_tools(cls.client))
        return ret[0].text

    @classmethod
    def chat_llm(cls, messages: list, tools: list=None ):
        response = completion(
            model=cls.model,
            api_key=cls.api_key,
            api_base=cls.api_base,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        return response
    
    @classmethod
    def get_tools(cls):
        async def list_tools(client):
            async with client:
                tools = await client.list_tools()
                return tools
        ret = asyncio.run(list_tools(cls.client))
        
        tools = [
            {
                "type": "function", 
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                    # "parameters": {
                    #     "type": tool.inputSchema.type,
                    #     "properties": {
                    #         **tool.inputSchema.properties,
                    #     },
                    #     "required": tool.inputSchema.required,
                    # },
                },
            }
            for tool in ret
        ]
        return tools
    


if __name__ == "__main__":
    ret = mcp_client()
    # ret = MCPClient.chat()
    print(f"===============ret:{ret}")   

    # sse_client()
