# Deepfake 检测系统后端

这是一个基于 Flask 的 Deepfake 检测系统后端服务。

## 项目结构

```
backend/
├── app/                    # 应用主目录
│   ├── api/               # API 接口
│   │   ├── v1/           # API 版本1
│   │   │   ├── auth.py   # 认证相关接口
│   │   │   ├── user.py   # 用户相关接口
│   │   │   └── deepfake.py # Deepfake检测接口
│   │   └── __init__.py
│   ├── core/             # 核心功能
│   │   ├── config.py     # 配置管理
│   │   ├── security.py   # 安全相关
│   │   └── extensions.py # 扩展初始化
│   ├── models/           # 数据模型
│   │   ├── user.py      # 用户模型
│   │   └── deepfake.py  # Deepfake检测记录模型
│   ├── services/         # 业务逻辑
│   │   ├── auth.py      # 认证服务
│   │   ├── user.py      # 用户服务
│   │   └── deepfake.py  # Deepfake检测服务
│   ├── tasks/           # 异步任务
│   │   ├── celery.py    # Celery配置
│   │   └── deepfake.py  # Deepfake检测任务
│   ├── utils/           # 工具函数
│   │   ├── logger.py    # 日志工具
│   │   ├── cache.py     # 缓存工具
│   │   └── file.py      # 文件处理工具
│   └── __init__.py      # 应用初始化
├── migrations/          # 数据库迁移
├── tests/              # 测试用例
│   ├── unit/          # 单元测试
│   ├── integration/   # 集成测试
│   └── conftest.py    # 测试配置
├── docs/              # 文档
│   ├── api/          # API文档
│   └── deployment/   # 部署文档
├── scripts/          # 脚本文件
├── .env.example     # 环境变量示例
├── .gitignore      # Git忽略文件
├── config.py       # 配置文件
├── requirements.txt # 项目依赖
└── run.py          # 应用入口
```

## 架构说明

### 1. 分层架构

- **API层**：处理HTTP请求和响应
- **Service层**：实现业务逻辑
- **Model层**：数据模型和数据库交互
- **Task层**：处理异步任务
- **Utils层**：提供通用工具

### 2. 模块化设计

- 按功能模块划分代码
- 每个模块独立维护
- 清晰的依赖关系

### 3. 扩展性考虑

- 支持API版本控制
- 可扩展的服务架构
- 插件化的功能模块

### 4. 安全性设计

- 统一的认证机制
- 请求速率限制
- 文件上传安全

### 5. 性能优化

- 缓存机制
- 异步任务处理
- 数据库优化

## 技术栈

- Python 3.8+
- Flask
- SQLAlchemy
- Celery
- Redis
- MySQL
- JWT
- Swagger

## 安装和运行

1. 克隆项目
```bash
git clone [项目地址]
cd backend
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入相应的配置信息
```

5. 初始化数据库
```bash
flask db upgrade
```

6. 运行项目
```bash
python run.py
```

## 开发指南

- 使用 `black` 进行代码格式化
- 使用 `flake8` 进行代码检查
- 使用 `mypy` 进行类型检查
- 使用 `pytest` 运行测试

## API 文档

API 文档请参考 [API.md](docs/api/API.md)

## 部署指南

部署说明请参考 [Deployment.md](docs/deployment/Deployment.md)

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT
