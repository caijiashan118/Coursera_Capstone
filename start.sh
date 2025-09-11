#!/bin/bash
# AI城建系统启动脚本 (Linux/macOS)

echo "AI城建系统启动脚本"
echo "=================="

# 检查Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "错误：未找到Python解释器"
    exit 1
fi

echo "使用Python解释器: $PYTHON_CMD"

# 检查是否在项目目录
if [ ! -f "main.py" ]; then
    echo "错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖包..."
$PYTHON_CMD -c "import tkinter, pandas, matplotlib, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告：缺少依赖包，尝试自动安装..."
    $PYTHON_CMD install.py
    if [ $? -ne 0 ]; then
        echo "错误：依赖包安装失败"
        exit 1
    fi
fi

# 启动程序
echo "启动AI城建系统..."
$PYTHON_CMD run.py