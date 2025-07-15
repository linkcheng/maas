# MCP Server 模块

使用领域驱动设计(DDD)架构重构的MCP服务器模块。

## 架构

本项目采用DDD的分层架构:

```
mcp_server/
├── domain/                  # 领域层
│   ├── models/              # 领域模型
│   │   └── tool.py          # 工具和MCP实体
│   ├── repositories/        # 仓储接口
│   │   └── tool_repository.py  # 工具仓储接口
│   └── services/            # 领域服务
│       ├── mcp_service.py   # MCP领域服务
│       └── tool_factory.py  # 工具工厂
├── application/             # 应用层
│   ├── services/            # 应用服务
│   │   └── mcp_application_service.py  # MCP应用服务
│   └── schemas/             # 数据模型
│       └── mcp_schemas.py   # MCP数据模型
├── infrastructure/          # 基础设施层
│   ├── persistence/         # 持久化实现
│   │   └── mcp_repository.py  # MCP仓储实现
│   └── services/            # 外部服务集成
│       └── fastmcp_adapter.py  # FastMCP适配器
└── interfaces/              # 接口层
    └── api/                 # API接口
        └── router.py        # API路由
```

## 关键技术

- **FastAPI**: 现代、高性能的Python Web框架
- **领域驱动设计(DDD)**: 软件架构方法，关注领域模型
- **FastMCP**: MCP工具集成库
- **Pydantic**: 数据验证和序列化库

## 设计原则

1. **分层架构**: 清晰的分层结构，实现关注点分离
2. **领域模型**: 核心业务领域以实体和值对象表示
3. **仓储模式**: 数据访问抽象化
4. **依赖注入**: 降低组件间耦合
5. **适配器模式**: 通过适配器连接外部服务

## 重构改进

相比原有代码：

1. **消除重复代码**: 通过领域服务和工厂提取公共逻辑
2. **提高可维护性**: 清晰的分层架构，职责单一
3. **增强可测试性**: 通过依赖注入，便于单元测试
4. **改进错误处理**: 统一的异常处理机制
5. **统一API响应**: 标准化的API响应格式

## 使用方法

### 单独运行

```bash
cd mcp-server
python -m mcp_server.main
```

### 与Chat模块集成

```bash
cd mcp-server
python main.py
```

## API文档

启动服务后，访问:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 