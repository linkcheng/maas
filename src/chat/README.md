# 聊天模块 (Chat Module)

这是一个基于FastAPI和SQLAlchemy 2.0的聊天模块，使用领域驱动设计(DDD)模式进行构建。

## 架构

本项目采用DDD分层架构:

```
mcp-server/chat/
├── domain/                  # 领域层
│   ├── models/              # 领域模型
│   ├── repositories/        # 仓储接口
│   └── services/            # 领域服务
├── application/             # 应用层
│   ├── chat_service.py      # 聊天应用服务
│   └── schemas.py           # 应用数据模型
├── infrastructure/          # 基础设施层
│   └── persistence/         # 持久化实现
│       ├── database.py      # 数据库配置
│       ├── models.py        # ORM模型
│       └── repositories.py  # 仓储实现
└── interfaces/              # 接口层
    └── api/                 # API接口
        └── router.py        # API路由
```

## 关键技术

- **FastAPI**: 现代、高性能的Python Web框架
- **SQLAlchemy 2.0**: 强大的ORM工具，支持异步数据库操作
- **Pydantic**: 数据验证和序列化库
- **asyncio**: 异步编程支持
- **领域驱动设计(DDD)**: 软件设计方法，强调领域模型

## 设计原则

1. **分层架构**: 清晰的分层结构，关注点分离
2. **领域模型**: 核心业务领域以实体和值对象表示
3. **仓储模式**: 数据访问抽象化
4. **依赖注入**: 降低组件间耦合
5. **微服务设计**: 可独立部署和扩展

## 主要功能

1. **聊天管理**: 创建、查询聊天会话
2. **消息处理**: 发送、接收消息
3. **工具集成**: 集成外部工具和服务
4. **大型语言模型(LLM)交互**: 与LLM进行对话，支持流式响应

## 安装与运行

### 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy aiomysql pydantic[email] fastmcp litellm
```

### 环境变量配置

创建`.env`文件:

```
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/dbname
MCP_SERVER_URL=http://localhost:8000
LLM_MODEL=gpt-3.5-turbo
LLM_API_KEY=your-api-key
LLM_API_BASE=https://api.openai.com/v1
```

### 运行服务

```bash
uvicorn chat.main:app --reload
```

## API文档

启动服务后，访问:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 开发指南

### 添加新功能

1. 在领域层定义新的实体或值对象
2. 在领域服务中实现业务逻辑
3. 在应用层创建服务方法协调领域对象
4. 在接口层暴露API端点 