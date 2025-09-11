@echo off
REM AI城建系统启动脚本 (Windows)

echo AI城建系统启动脚本
echo ==================

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误：未找到Python解释器
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

echo 使用Python解释器: %PYTHON_CMD%

REM 检查是否在项目目录
if not exist "main.py" (
    echo 错误：请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
%PYTHON_CMD% -c "import tkinter, pandas, matplotlib, openpyxl" >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告：缺少依赖包，尝试自动安装...
    %PYTHON_CMD% install.py
    if %errorlevel% neq 0 (
        echo 错误：依赖包安装失败
        pause
        exit /b 1
    )
)

REM 启动程序
echo 启动AI城建系统...
%PYTHON_CMD% run.py

pause