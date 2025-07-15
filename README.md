# Maas 平台

这是一个基于 FastAPI 的数据资产服务和聊天平台，采用领域驱动设计(DDD)架构重构。目前系统包含两个主要模块：工具服务(`mcp_server`)和聊天应用(`chat`)。

## 架构特点

- **领域驱动设计(DDD)**: 清晰的分层架构，包含领域层、应用层、基础设施层和接口层
- **异步处理**: 基于FastAPI和SQLAlchemy 2.0的异步操作
- **模块化设计**: 独立的功能模块便于扩展和维护
- **统一API**: 集成的API端点，统一的数据和错误处理

### 系统架构图

```
maas/
├── chat/                    # 聊天模块
│   ├── domain/              # 领域层 - 核心业务模型
│   ├── application/         # 应用层 - 业务协调
│   ├── infrastructure/      # 基础设施层 - 外部集成
│   └── interfaces/          # 接口层 - API定义
├── mcp_server/              # MCP服务模块
│   ├── domain/              # 领域层 - 核心业务模型
│   ├── application/         # 应用层 - 业务协调
│   ├── infrastructure/      # 基础设施层 - 外部集成
│   └── interfaces/          # 接口层 - API定义
└── main.py                  # 主程序入口 - 集成两个模块
```

## 功能特点

### MCP服务模块

- 基于FastMCP的工具集成框架
- 提供数据资产管理和查询
- 支持数据分析和处理功能
- 通过领域服务和工厂模式创建工具

### 聊天模块

- 支持聊天会话管理
- 整合大型语言模型(LLM)
- 支持流式响应和消息历史
- 工具集成和调用能力

## 安装

### 使用 uv 安装（推荐）

1. 安装 uv：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 创建虚拟环境并安装依赖：
```bash
uv venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

uv pip install -r requirements.txt
```

### 使用传统方式安装

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行服务

```bash
# 运行完整集成版本（包含chat和mcp_server）
python main.py

```

服务将在 http://localhost:8000 启动

## API 端点

### 根路由
- GET `/`: 服务状态检查和路由信息
- GET `/health`: 健康检查

### MCP服务路由
- GET `/api/v1/server/mcp/`: MCP API根路径
- POST `/api/v1/server/mcp/mcps`: 创建MCP
- POST `/api/v1/server/mcp/mcps/{mcp_name}/tools`: 向MCP添加工具
- POST `/api/v1/server/mcp/mcps/{mcp_name}/tools/{tool_name}/execute`: 执行工具

### 用户管理路由
- POST `/api/v1/users/`: 创建用户
- POST `/api/v1/users/token`: 用户登录
- GET `/api/v1/users/me`: 获取当前用户信息
- PUT `/api/v1/users/me/password`: 修改密码
- GET `/api/v1/users/{user_id}`: 获取用户信息

### 聊天路由
- POST `/api/v1/chat/sources`: 创建源
- GET `/api/v1/chat/sources`: 获取源列表
- GET `/api/v1/chat/sources/{source_id}`: 获取源详情
- PUT `/api/v1/chat/sources/{source_id}`: 更新源
- DELETE `/api/v1/chat/sources/{source_id}`: 删除源
- POST `/api/v1/chat/chats`: 创建聊天会话
- GET `/api/v1/chat/users/{user_id}/chats`: 获取用户聊天列表
- GET `/api/v1/chat/chats/{chat_id}/messages`: 获取聊天消息
- POST `/api/v1/chat/chat-tools`: 为聊天添加工具
- POST `/api/v1/chat/chat-data`: 发送消息（流式响应）

### RAG路由
- POST `/api/v1/rag/documents`: 创建并处理文档
- POST `/api/v1/rag/search`: 搜索相关文档块
- GET `/api/v1/rag/documents/{document_id}`: 获取文档详情

## 开发

### 模块化开发
每个模块都可以独立开发和测试，同时保持与其他模块的集成能力。

### 运行测试
```bash
pytest
```

### 代码格式化
```bash
ruff format .
```

### 代码检查
```bash
ruff check .
```

## 设计原则

1. **单一职责**: 每个组件只负责一个功能
2. **依赖反转**: 使用依赖注入降低耦合度
3. **领域隔离**: 保护领域逻辑不受外部影响
4. **丰富领域模型**: 确保领域模型包含业务规则
5. **持续重构**: 持续优化代码以保持清晰性和可维护性 

## 部署指南

本项目支持使用Docker进行开发和生产环境的部署。

### 环境准备

- Docker 和 Docker Compose
- Python 3.12
- MySQL 8.0

### 环境变量配置

1. 复制示例环境变量文件:
```bash
cp .env.example .env
```

2. 根据需要编辑`.env`文件中的配置:
```
# 应用配置
APP_ENV=dev  # dev, test, prod
APP_VERSION=0.1.0
SERVER_PORT=8000
SERVER_CORS_ORIGINS=*
LOG_LEVEL=INFO

# 数据库配置
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=mcpdb
MYSQL_USER=mcpuser
MYSQL_PASSWORD=mcppassword
MYSQL_PORT=3306

# LLM配置
LLM_API_KEY=your-api-key

# Docker 部署配置
DOCKER_REGISTRY=localhost
```

### 部署

使用Docker Compose启动开发环境:

```bash
docker-compose up -d
```

停止开发环境:

```bash
docker-compose down
```
