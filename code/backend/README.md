# 云衣橱后端服务

基于FastAPI的云衣橱后端API服务

## 技术栈

- **框架**: FastAPI 0.104+
- **数据库**: PostgreSQL 15+ with SQLAlchemy 2.0
- **缓存**: Redis 7+
- **认证**: JWT
- **文档**: 自动生成OpenAPI文档

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入实际配置
```

### 3. 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head
```

### 4. 启动服务

```bash
# 开发环境
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产环境
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── api/              # API路由
│   │   ├── v1/
│   │   │   ├── auth.py   # 认证相关
│   │   │   ├── users.py  # 用户相关
│   │   │   ├── clothings.py # 衣物相关
│   │   │   ├── orders.py # 订单相关
│   │   │   └── ...
│   ├── core/             # 核心配置
│   │   ├── config.py     # 配置管理
│   │   ├── security.py   # 安全相关
│   │   └── deps.py       # 依赖注入
│   ├── models/           # 数据库模型
│   │   ├── user.py
│   │   ├── clothing.py
│   │   ├── order.py
│   │   └── ...
│   ├── schemas/          # Pydantic模型
│   │   ├── user.py
│   │   ├── clothing.py
│   │   ├── order.py
│   │   └── ...
│   ├── services/         # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── clothing_service.py
│   │   └── ...
│   ├── repositories/     # 数据访问层
│   │   ├── user_repository.py
│   │   └── ...
│   └── utils/            # 工具函数
│       ├── logger.py
│       ├── redis_client.py
│       └── ...
├── alembic/              # 数据库迁移
├── tests/                # 测试
├── logs/                 # 日志文件
├── requirements.txt      # 依赖列表
├── .env                 # 环境变量
└── main.py             # 应用入口
```

## API文档

### 认证相关
- `POST /api/v1/auth/send-sms` - 发送验证码
- `POST /api/v1/auth/register` - 注册
- `POST /api/v1/auth/login` - 登录
- `POST /api/v1/auth/wechat-login` - 微信登录

### 用户相关
- `GET /api/v1/users/me` - 获取当前用户信息
- `PUT /api/v1/users/me` - 更新用户信息
- `POST /api/v1/users/verify` - 实名认证

### 衣物相关
- `GET /api/v1/clothings` - 衣物列表
- `POST /api/v1/clothings` - 发布衣物
- `GET /api/v1/clothings/{id}` - 衣物详情
- `PUT /api/v1/clothings/{id}` - 编辑衣物
- `DELETE /api/v1/clothings/{id}` - 删除衣物
- `POST /api/v1/clothings/{id}/favorite` - 收藏衣物

### 订单相关
- `GET /api/v1/orders` - 订单列表
- `POST /api/v1/orders` - 创建订单
- `GET /api/v1/orders/{id}` - 订单详情
- `PUT /api/v1/orders/{id}/confirm` - 确认订单
- `PUT /api/v1/orders/{id}/ship` - 发货
- `PUT /api/v1/orders/{id}/receive` - 确认收货
- `PUT /api/v1/orders/{id}/return` - 申请归还
- `PUT /api/v1/orders/{id}/complete` - 完成订单

## 开发规范

### 代码风格
- 遵循PEP 8规范
- 使用类型注解
- 编写文档字符串

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_users.py

# 生成覆盖率报告
pytest --cov=app tests/
```

## 部署

### Docker部署
```bash
# 构建镜像
docker build -t cloudrobe-backend .

# 运行容器
docker run -p 8000:8000 cloudrobe-backend
```

### Docker Compose部署
```bash
docker-compose up -d
```

## 许可证

MIT
