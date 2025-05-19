@echo off
setlocal enabledelayedexpansion

echo 博士申请管理系统启动脚本
echo ====================================

:: 确定Python命令
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set PYTHON_CMD=python3
    ) else (
        echo 错误: 找不到Python。请确保安装了Python 3
        pause
        exit /b 1
    )
)

:: 启动后端
echo 启动后端服务...
cd "%~dp0backend" || (
    echo 错误: 找不到backend目录
    pause
    exit /b 1
)

:: 检查是否需要初始化数据库
if not exist "instance\phd_application.db" (
    echo 初始化数据库...
    %PYTHON_CMD% init_db.py
)

:: 启动后端服务
start cmd /k "%PYTHON_CMD% run.py"
echo 后端服务已启动，请勿关闭新打开的命令窗口

:: 等待后端启动完成
echo 等待后端服务启动完成...
timeout /t 3 /nobreak >nul

:: 检查前端目录是否存在
if not exist "..\frontend" (
    echo 警告: 找不到frontend目录，只启动后端服务
    echo 您可以通过访问 http://localhost:8000/docs 使用API
    echo 按任意键停止服务
    pause
    exit /b 0
)

:: 启动前端
echo 启动前端服务...
cd "..\frontend" || (
    echo 错误: 无法进入frontend目录
    pause
    exit /b 1
)

:: 检查Node.js和npm
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 警告: 找不到npm。请确保安装了Node.js和npm
    echo 后端服务仍在运行，您可以通过访问 http://localhost:8000/docs 使用API
    echo 按任意键停止服务
    pause
    exit /b 0
)

:: 安装依赖(如果需要)
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)

:: 启动前端服务
echo 启动前端服务...
start cmd /k "npm run serve"

echo =========================
echo 系统启动完成!
echo 后端API: http://localhost:8000/docs
echo 前端界面: http://localhost:8080
echo =========================
echo 关闭此窗口将不会停止服务，您需要手动关闭服务窗口

pause 