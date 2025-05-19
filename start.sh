#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}博士申请管理系统启动脚本${NC}"
echo -e "${BLUE}====================================${NC}"

# 激活虚拟环境
SCRIPT_DIR="$(dirname "$0")"
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    echo -e "${GREEN}激活虚拟环境...${NC}"
    source "$SCRIPT_DIR/venv/bin/activate"
    PYTHON_CMD="python"
else
    # 确定Python命令
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}错误: 找不到Python。请确保安装了Python 3${NC}"
        exit 1
    fi
fi

# 安装依赖
echo -e "${GREEN}检查依赖...${NC}"
$PYTHON_CMD -m pip install -q sqlalchemy fastapi uvicorn

# 启动后端
echo -e "${GREEN}启动后端服务...${NC}"
cd "$SCRIPT_DIR/backend" || { echo -e "${RED}错误: 找不到backend目录${NC}"; exit 1; }

# 检查是否需要初始化数据库
if [ ! -f "instance/phd_application.db" ]; then
    echo -e "${BLUE}初始化数据库...${NC}"
    $PYTHON_CMD init_db.py
fi

# 启动后端服务
$PYTHON_CMD run.py &
BACKEND_PID=$!
echo -e "${GREEN}后端服务已启动 (PID: $BACKEND_PID)${NC}"

# 等待后端启动完成
echo -e "${BLUE}等待后端服务启动完成...${NC}"
sleep 3

# 检查前端目录是否存在
if [ ! -d "../frontend" ]; then
    echo -e "${RED}警告: 找不到frontend目录，只启动后端服务${NC}"
    echo -e "${GREEN}您可以通过访问 http://localhost:8000/docs 使用API${NC}"
    # 保持脚本运行，直到用户中断
    echo -e "${BLUE}按Ctrl+C停止服务${NC}"
    wait $BACKEND_PID
    exit 0
fi

# 启动前端
echo -e "${GREEN}启动前端服务...${NC}"
cd "../frontend" || { echo -e "${RED}错误: 无法进入frontend目录${NC}"; exit 1; }

# 检查Node.js和npm
if ! command -v npm &>/dev/null; then
    echo -e "${RED}警告: 找不到npm。请确保安装了Node.js和npm${NC}"
    echo -e "${GREEN}后端服务仍在运行，您可以通过访问 http://localhost:8000/docs 使用API${NC}"
    echo -e "${BLUE}按Ctrl+C停止服务${NC}"
    wait $BACKEND_PID
    exit 0
fi

# 安装依赖(如果需要)
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}安装前端依赖...${NC}"
    npm install || { echo -e "${RED}警告: 安装前端依赖失败${NC}"; }
fi

# 启动前端服务
echo -e "${BLUE}启动前端服务...${NC}"
npm run serve &
FRONTEND_PID=$!

echo -e "${GREEN}=========================${NC}"
echo -e "${GREEN}系统启动完成!${NC}"
echo -e "${GREEN}后端API: http://localhost:8000/docs${NC}"
echo -e "${GREEN}前端界面: http://localhost:8080${NC}"
echo -e "${GREEN}=========================${NC}"
echo -e "${BLUE}按Ctrl+C停止服务${NC}"

# 等待任一进程结束
wait $BACKEND_PID $FRONTEND_PID

# 确保关闭所有进程
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo -e "${RED}服务已停止${NC}" 