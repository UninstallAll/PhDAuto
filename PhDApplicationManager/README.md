# 博士申请管理系统 (PhD Application Manager)

一个全面的博士申请管理工具，帮助您跟踪申请进度、管理文档、与导师沟通，以及获取实时申请信息。

## 功能特点

- **申请跟踪**：管理学校和导师信息，跟踪申请状态
- **文档管理**：集中存储和组织申请文档（如CV、个人陈述、推荐信等）
- **邮件管理**：根据导师研究领域自动生成邮件草稿，管理与导师的邮件往来
- **信息检索**：集成AI接口（如DeepSeek）搜集学校申请截止日期等信息
- **通知提醒**：关键日期和事件的自动提醒

## 技术栈

### 后端

- **Python 3.x**
- **FastAPI**: 高性能Web框架
- **SQLAlchemy**: ORM工具
- **SQLite**: 轻量级数据库
- **Pydantic**: 数据验证

### 前端

- **Vue 3**: 渐进式JavaScript框架
- **Element Plus**: UI组件库
- **Axios**: HTTP客户端
- **Vue Router**: 路由管理
- **Vuex**: 状态管理

## 安装与运行

### 必备条件

- Python 3.7+
- Node.js 12+ (前端开发)

### 后端设置

1. 创建并激活虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

2. 安装依赖：

```bash
pip install fastapi uvicorn sqlalchemy pydantic python-multipart aiofiles requests
```

3. 运行后端：

```bash
cd backend
python run.py
```

后端服务器将在 http://localhost:8000 上运行。

### 前端设置

1. 安装依赖：

```bash
cd frontend
npm install
```

2. 运行开发服务器：

```bash
npm run serve
```

前端应用将在 http://localhost:8080 上运行。

### 快速启动（仅后端）

使用提供的脚本启动后端服务器：

```bash
./run.sh
```

## 使用指南

1. **添加学校**：记录您有兴趣申请的学校、部门和项目信息。
2. **添加导师**：添加您感兴趣的导师信息，包括研究领域和联系信息。
3. **创建申请**：为每个学校/导师组合创建申请记录，跟踪申请状态。
4. **上传文档**：添加CV、个人陈述等文档到对应的申请记录。
5. **发送邮件**：使用系统生成的邮件模板与导师进行联系。
6. **信息检索**：通过AI服务搜索学校和导师信息。
7. **设置提醒**：为重要日期设置通知提醒。

## API文档

API文档可在后端服务器运行后通过 http://localhost:8000/docs 访问。

## 数据库结构

系统使用SQLite数据库，包含以下主要表：

- `schools`: 存储学校信息
- `professors`: 存储导师信息
- `applications`: 存储申请记录
- `documents`: 存储文档信息
- `emails`: 存储邮件记录
- `notifications`: 存储通知记录

## 开发计划

- 移动应用支持
- 多语言支持
- 更多第三方AI服务集成
- 高级数据分析和可视化

## 贡献

欢迎贡献！请随时提交问题或拉取请求。

## 许可

[MIT](LICENSE) 