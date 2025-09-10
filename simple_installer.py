#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统简化安装脚本
复制此文件到您的桌面，然后运行：python simple_installer.py
"""

print("🚀 AI城建系统简化版安装器")
print("=" * 40)

# 检查Python版本
import sys
if sys.version_info < (3, 7):
    print("❌ 需要Python 3.7或更高版本")
    exit(1)

print("✅ Python版本检查通过")

# 创建基本项目结构
import os
from pathlib import Path

print("📁 创建项目目录...")
directories = ["src", "src/gui", "src/database", "data", "templates", "static"]
for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {directory}/")

# 创建requirements.txt
print("📄 创建依赖文件...")
requirements = """Flask==2.3.3
pandas==2.0.3
plotly==5.17.0
openpyxl==3.1.2
numpy==1.24.3"""

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements)
print("  ✓ requirements.txt")

# 创建简单的Flask应用
print("🌐 创建Web应用...")
web_app_code = '''from flask import Flask, render_template, jsonify
import sqlite3
import json

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI城建系统</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
            .module { background: #ecf0f1; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3498db; }
            .button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .button:hover { background: #2980b9; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
            .stat-card { background: #34495e; color: white; padding: 20px; border-radius: 8px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏙️ AI城建系统</h1>
                <p>智能城市建设管理平台 - Web版本</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>项目总数</h3>
                    <div style="font-size: 2em; margin: 10px 0;">0</div>
                    <p>个项目</p>
                </div>
                <div class="stat-card">
                    <h3>概算总额</h3>
                    <div style="font-size: 2em; margin: 10px 0;">0</div>
                    <p>万元</p>
                </div>
                <div class="stat-card">
                    <h3>资金安排</h3>
                    <div style="font-size: 2em; margin: 10px 0;">0</div>
                    <p>条记录</p>
                </div>
                <div class="stat-card">
                    <h3>系统状态</h3>
                    <div style="font-size: 1.5em; margin: 10px 0;">🟢</div>
                    <p>运行正常</p>
                </div>
            </div>
            
            <div class="module">
                <h3>🗂️ 基础数据管理</h3>
                <p>管理项目基本信息、资金安排、重点项目清单</p>
                <button class="button" onclick="alert('生成模拟数据功能\\n\\n✅ 支持生成200个项目\\n✅ 支持生成1000条资金记录\\n✅ 包含项目状态：在建、续建、完工、暂停\\n✅ 包含资金性质：一般债券、专项债券等')">生成模拟数据</button>
                <button class="button" onclick="alert('Excel导入导出功能\\n\\n✅ 支持导入项目信息\\n✅ 支持导入资金安排\\n✅ 支持导出数据报表\\n✅ 自动验证数据格式')">Excel导入导出</button>
                <button class="button" onclick="showPivotTable()">数据透视表</button>
            </div>
            
            <div class="module">
                <h3>📊 数据可视化</h3>
                <p>提供8种图表类型，全面展示项目和资金数据</p>
                <button class="button" onclick="showCharts()">项目状态分布图</button>
                <button class="button" onclick="showCharts()">资金性质分析图</button>
                <button class="button" onclick="showCharts()">债券资金统计图</button>
                <button class="button" onclick="showCharts()">更多图表...</button>
            </div>
            
            <div class="module">
                <h3>📋 智慧报表生成</h3>
                <p>生成8种专业报表，支持日期筛选和Excel导出</p>
                <button class="button" onclick="showReports()">项目总览报表</button>
                <button class="button" onclick="showReports()">资金安排报表</button>
                <button class="button" onclick="showReports()">部门统计报表</button>
                <button class="button" onclick="showReports()">更多报表...</button>
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #7f8c8d;">
                <p>🎉 AI城建系统 v1.0.0 - 让城市建设管理更智能！</p>
                <p>💡 提示：这是演示版本，完整功能请安装桌面版</p>
            </div>
        </div>
        
        <script>
            function showPivotTable() {
                alert('数据透视表功能\\n\\n✅ 按项目编码分组\\n✅ 显示各资金性质分布\\n✅ 自动计算债券资金合计\\n✅ 支持数据筛选和排序\\n\\n债券资金合计 = 一般债券 + 专项债券');
            }
            
            function showCharts() {
                alert('数据可视化功能\\n\\n支持的图表类型：\\n• 项目状态分布图（饼图）\\n• 概算金额分布图（直方图）\\n• 资金性质分析图（条形图）\\n• 项目时间轴图（甘特图）\\n• 债券资金统计图（堆叠图）\\n• 部门项目数量统计\\n• 月度资金安排趋势\\n• 项目完成度分析\\n\\n✨ 支持中文显示和图片导出');
            }
            
            function showReports() {
                alert('智慧报表生成功能\\n\\n支持的报表类型：\\n• 项目总览报表\\n• 资金安排报表\\n• 项目进度报表\\n• 部门统计报表\\n• 债券资金报表\\n• 月度汇总报表\\n• 项目完成情况报表\\n• 资金透视分析报表\\n\\n✨ 支持日期范围筛选和Excel导出');
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

with open("web_app.py", "w", encoding="utf-8") as f:
    f.write(web_app_code)
print("  ✓ web_app.py")

# 创建启动说明
readme = """# AI城建系统简化版

## 🚀 快速启动

1. 安装依赖：
   pip install -r requirements.txt

2. 启动Web版本：
   python web_app.py

3. 浏览器访问：
   http://localhost:5000

## 📋 功能说明

✅ 基础数据管理
✅ 数据可视化演示  
✅ 智慧报表功能介绍
✅ Web界面展示

## 🎯 获取完整版

完整的桌面版本包含：
- 完整的数据库功能
- 真实的图表生成
- Excel导入导出
- 数据透视表
- 200个模拟项目
- 1000条资金记录

联系开发团队获取完整版本。

## 💡 提示

这是演示版本，展示系统界面和功能概览。
完整功能请使用桌面版AI城建系统。
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
print("  ✓ README.md")

print("\n🎉 AI城建系统简化版安装完成！")
print("\n📋 使用步骤：")
print("1. pip install -r requirements.txt")
print("2. python web_app.py") 
print("3. 浏览器访问：http://localhost:5000")
print("\n💡 这是演示版本，展示系统功能概览")
print("完整版本请联系开发团队获取")

# 尝试自动安装依赖
print("\n🔄 尝试自动安装依赖...")
try:
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 依赖安装成功！")
        print("\n🚀 现在可以运行：python web_app.py")
    else:
        print("⚠️ 自动安装失败，请手动运行：pip install -r requirements.txt")
except Exception as e:
    print(f"⚠️ 自动安装出错：{e}")
    print("请手动运行：pip install -r requirements.txt")