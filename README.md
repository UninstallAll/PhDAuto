# 博士申请管理系统 (PhD Application Manager)

一个全面的博士申请管理系统，帮助申请者跟踪申请进度、管理文档和邮件通信。

## 功能特点

### 数据管理
- 学校和导师信息的管理
- 申请记录追踪
- 文档管理（CV、个人陈述等）

### 信息检索
- 集成DeepSeek API（可配置）用于搜集学校和导师信息
- 获取申请截止日期
- 搜索导师研究领域和发表文章

### 邮件管理
- 自动生成邮件草稿，基于导师研究领域和学生信息
- 管理与导师的邮件往来
- 支持附件和各种邮件模板

### 通知系统
- 截止日期提醒
- 申请状态变更通知
- 邮件回复通知

## 技术栈

### 后端
- Python + FastAPI框架
- SQLite数据库 + SQLAlchemy ORM
- RESTful API设计
- 模块化服务（信息检索、邮件、通知等）

### 前端
- Vue 3 + Element Plus UI库
- 响应式设计
- 状态管理（Vuex）
- 路由管理（Vue Router）

## 安装说明

### 系统要求
- Python 3.7+
- Node.js 14+ (前端开发)
- npm 6+ (前端开发)

### 后端安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/PhDApplicationManager.git
cd PhDApplicationManager

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 前端安装
```bash
cd frontend
npm install
```

## 使用说明

### 使用启动脚本
```bash
# Mac/Linux
./start.sh

# Windows
start.bat
```

### 手动启动
```bash
# 启动后端
cd backend
python run.py

# 启动前端 (需要新开一个终端)
cd frontend
npm run serve
```

### 访问系统
- 后端API: http://localhost:8000/docs
- 前端界面: http://localhost:8080

## 配置

### 环境变量
- `DATABASE_URL`: 数据库连接URL (默认SQLite)
- `DEEPSEEK_API_KEY`: DeepSeek API密钥(可选)
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`: 邮件服务配置

## 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 许可证

MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 联系方式

项目维护者 - [您的名字](mailto:your.email@example.com)

项目链接: [https://github.com/yourusername/PhDApplicationManager](https://github.com/yourusername/PhDApplicationManager) 