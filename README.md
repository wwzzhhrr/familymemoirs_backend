# 邮件验证码服务

一个基于 FastAPI 的邮件验证码发送和验证服务，支持阿里云邮件推送服务。

## 项目结构

```
jiashuwanjin-mail/
├── app/                    # 核心应用代码
│   ├── __init__.py
│   ├── main.py            # FastAPI 应用主文件
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   └── email_models.py
│   └── services/          # 业务逻辑服务
│       ├── __init__.py
│       ├── email_service.py
│       └── verification_service.py
├── config/                # 配置管理
│   ├── __init__.py
│   └── settings.py
├── utils/                 # 工具函数
│   ├── __init__.py
│   └── logger.py
├── service/              # 旧版本服务目录（待删除）
├── main.py               # 应用入口文件
├── requirements.txt      # 项目依赖
├── .env.example         # 环境变量配置模板
├── mail_body.html       # 邮件模板
└── README.md            # 项目说明
```

## 功能特性

- 🚀 基于 FastAPI 的高性能 Web 服务
- 📧 支持阿里云邮件推送服务
- 🔐 Redis 存储验证码，支持过期时间设置
- 📝 完整的日志记录和错误处理
- ⚙️ 灵活的配置管理，支持环境变量
- 🏗️ 标准化的项目结构，易于扩展和维护

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制环境变量模板文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置信息：

```env
# 邮件服务配置
ALIBABA_ACCESS_KEY_ID=your_access_key_id
ALIBABA_ACCESS_KEY_SECRET=your_access_key_secret
EMAIL_ACCOUNT_NAME=your_email@domain.com

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 应用配置
DEBUG=True
PORT=8000
```

### 3. 启动服务

```bash
python main.py
```

或者使用 uvicorn 直接启动：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API 接口

API采用功能模块化设计，按业务功能组织路径，遵循RESTful设计规范。

### 基础接口

#### 根路径
**GET** `/`

响应：
```json
{
    "message": "邮件验证码服务已启动",
    "docs": "/docs"
}
```

#### 全局健康检查
**GET** `/health`

响应：
```json
{
    "status": "healthy",
    "service": "邮件验证码服务",
    "version": "1.0.0"
}
```

### 邮件模块 (`/mail`)

#### 邮件模块健康检查
**GET** `/mail/health`

响应：
```json
{
    "status": "healthy",
    "module": "邮件服务",
    "features": ["发送验证码", "验证验证码"]
}
```

#### 发送验证码
**POST** `/mail/send-verification-code`

请求体：
```json
{
    "to_address": "user@example.com",
    "subject": "验证码通知",
    "from_alias": "家书万金"
}
```

响应：
```json
{
    "message": "验证码已发送",
    "email": "user@example.com"
}
```

#### 验证验证码
**POST** `/mail/verify-code`

请求体：
```json
{
    "address": "user@example.com",
    "code": "123456"
}
```

响应：
```json
{
    "message": "验证成功",
    "valid": true
}
```

### API 文档

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### 功能模块设计

当前项目采用功能模块化的API设计：
- `/mail` - 邮件相关功能（验证码发送、验证等）
- `/health` - 全局健康检查
- 未来可扩展其他模块，如：
  - `/sms` - 短信功能
  - `/auth` - 认证功能
  - `/user` - 用户管理功能

## 配置说明

### 邮件服务配置

- `ALIBABA_ACCESS_KEY_ID`: 阿里云访问密钥 ID
- `ALIBABA_ACCESS_KEY_SECRET`: 阿里云访问密钥密码
- `ALIBABA_EMAIL_ENDPOINT`: 阿里云邮件服务端点
- `EMAIL_ACCOUNT_NAME`: 发件人邮箱账号
- `EMAIL_TEMPLATE_PATH`: 邮件模板文件路径

### Redis 配置

- `REDIS_HOST`: Redis 服务器地址
- `REDIS_PORT`: Redis 服务器端口
- `REDIS_DB`: Redis 数据库编号
- `VERIFICATION_CODE_EXPIRY`: 验证码过期时间（秒）

### 应用配置

- `DEBUG`: 调试模式开关
- `HOST`: 服务监听地址
- `PORT`: 服务监听端口
- `LOG_LEVEL`: 日志级别

## 开发指南

### 项目结构说明

- **app/**: 核心应用代码目录
  - **models/**: 数据模型定义
  - **services/**: 业务逻辑服务
  - **main.py**: FastAPI 应用主文件

- **config/**: 配置管理模块
  - **settings.py**: 统一配置管理

- **utils/**: 工具函数模块
  - **logger.py**: 日志配置工具

### 添加新功能

1. 在 `app/models/` 中定义新的数据模型
2. 在 `app/services/` 中实现业务逻辑
3. 在 `app/main.py` 中添加 API 路由
4. 在 `config/settings.py` 中添加相关配置

## 部署

### Docker 部署（推荐）

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

### 生产环境部署

```bash
# 使用 gunicorn 部署
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 许可证

MIT License