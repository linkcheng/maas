# MCP Data Analysis Server

这是一个基于 FastAPI 的数据资产服务和聊天平台，采用领域驱动设计(DDD)架构重构。系统包含两个主要模块：数据分析服务(`mcp_server`)和聊天应用(`chat`)。

## 架构特点

- **领域驱动设计(DDD)**: 清晰的分层架构，包含领域层、应用层、基础设施层和接口层
- **异步处理**: 基于FastAPI和SQLAlchemy 2.0的异步操作
- **模块化设计**: 独立的功能模块便于扩展和维护
- **统一API**: 集成的API端点，统一的数据和错误处理

### 系统架构图

```
mcp-server/
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

# 或仅运行MCP服务
python -m mcp_server.main

# 或仅运行聊天服务
python -m chat.main
```

服务将在 http://localhost:8000 启动

## API 端点

### 根路由
- GET `/`: 服务状态检查和路由信息

### MCP服务路由
- `/mcp/api/v1/mcp/`: MCP API根路径
- `/mcp/api/v1/mcp/mcps`: MCP管理
- `/mcp/api/v1/mcp/mcps/{mcp_name}/tools`: 工具管理
- `/mcp/api/v1/mcp/mcps/{mcp_name}/tools/{tool_name}/execute`: 执行工具

### 聊天路由
- `/chat/api/v1/sources`: 聊天源管理
- `/chat/api/v1/chats`: 聊天会话管理
- `/chat/api/v1/users/{user_id}/chats`: 获取用户聊天
- `/chat/api/v1/chats/{chat_id}/messages`: 聊天消息
- `/chat/api/v1/chat-data`: 发送消息（流式响应）

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

### 开发环境部署

使用Docker Compose启动开发环境:

```bash
docker-compose up -d
```

停止开发环境:

```bash
docker-compose down
```

### 生产环境部署

本项目提供了部署脚本`deploy.sh`，可以简化部署过程:

1. 构建镜像:
```bash
./deploy.sh --build
```

2. 推送镜像到仓库(可选):
```bash
./deploy.sh --push
```

3. 部署应用:
```bash
./deploy.sh --deploy
```

一键构建并部署:
```bash
./deploy.sh --build --deploy
```

停止并移除容器:
```bash
./deploy.sh --down
```

查看帮助信息:
```bash
./deploy.sh --help
```

### 自定义镜像名称

可以通过环境变量自定义镜像名称:

```bash
APP_VERSION=1.0.0 DOCKER_REGISTRY=myregistry.com ./deploy.sh --build --push
```

### 健康检查

应用程序提供了健康检查端点：

- `GET /health` - 返回应用程序状态

### 镜像构建

项目使用多阶段构建优化Docker镜像大小。Dockerfile基于Python 3.12，并使用最佳实践进行配置：

- 使用轻量级基础镜像
- 优化构建层和缓存
- 使用非root用户运行应用程序
- 包含健康检查 