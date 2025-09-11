#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统一键创建脚本
运行此脚本将自动创建完整的项目结构和所有文件
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """创建目录结构"""
    directories = [
        "src",
        "src/database", 
        "src/gui",
        "src/models",
        "src/utils",
        "assets",
        "data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def create_requirements_txt():
    """创建requirements.txt"""
    content = """pandas==2.0.3
openpyxl==3.1.2
SQLAlchemy==2.0.21
plotly==5.17.0
numpy==1.24.3
python-dateutil==2.8.2
matplotlib==3.7.2
tkinter-tooltip==2.1.0
Pillow==10.0.0
pyinstaller==5.13.2"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ 创建文件: requirements.txt")

def create_main_py():
    """创建main.py"""
    content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统 - 主程序入口
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.gui.main_window import MainWindow
from src.database.db_manager import DatabaseManager

class AIUrbanConstructionSystem:
    """AI城建系统主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.init_database()
        self.main_window = None
        
    def setup_window(self):
        """设置主窗口"""
        self.root.title("AI城建系统")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # 设置窗口图标
        try:
            icon_path = project_root / "assets" / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass
            
        # 居中显示窗口
        self.center_window()
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def init_database(self):
        """初始化数据库"""
        try:
            db_manager = DatabaseManager()
            db_manager.create_tables()
        except Exception as e:
            messagebox.showerror("数据库错误", f"数据库初始化失败：{str(e)}")
            
    def run(self):
        """运行应用程序"""
        try:
            # 创建主界面
            self.main_window = MainWindow(self.root)
            
            # 运行主循环
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("系统错误", f"系统运行出错：{str(e)}")
            
    def on_closing(self):
        """关闭程序时的处理"""
        if messagebox.askokcancel("退出", "确定要退出AI城建系统吗？"):
            self.root.destroy()

def main():
    """主函数"""
    try:
        app = AIUrbanConstructionSystem()
        app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.run()
    except Exception as e:
        print(f"程序启动失败：{e}")
        messagebox.showerror("启动错误", f"程序启动失败：{str(e)}")

if __name__ == "__main__":
    main()'''
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ 创建文件: main.py")

def create_run_py():
    """创建run.py"""
    content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统启动脚本
用于开发环境下直接运行程序
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # 检查必要的依赖包
    print("检查依赖包...")
    
    import tkinter as tk
    import pandas as pd
    import matplotlib.pyplot as plt
    import openpyxl
    import numpy as np
    
    print("✓ 所有依赖包检查通过")
    
    # 导入并运行主程序
    from main import main
    
    print("启动AI城建系统...")
    main()
    
except ImportError as e:
    print(f"✗ 缺少依赖包：{e}")
    print("请运行以下命令安装依赖：")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"✗ 程序运行出错：{e}")
    import traceback
    traceback.print_exc()'''
    
    with open("run.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ 创建文件: run.py")

def create_init_files():
    """创建__init__.py文件"""
    init_files = [
        "src/__init__.py",
        "src/database/__init__.py", 
        "src/gui/__init__.py",
        "src/models/__init__.py",
        "src/utils/__init__.py"
    ]
    
    for init_file in init_files:
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('# -*- coding: utf-8 -*-')
        print(f"✓ 创建文件: {init_file}")

def create_readme():
    """创建README.md"""
    content = '''# AI城建系统

AI城建系统是一个智能城市建设管理平台，提供项目管理、资金安排、数据可视化和智慧报表生成功能。

## 🚀 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python main.py
```

## 🌟 主要功能

- ✅ 项目基本信息管理
- ✅ 资金安排管理  
- ✅ Excel导入导出
- ✅ 数据可视化图表
- ✅ 智慧报表生成
- ✅ 数据透视分析

## 📊 系统模块

1. **基础数据管理** - 项目信息、资金安排、重点项目清单
2. **数据可视化** - 8种图表类型
3. **智慧报表生成** - 8种报表类型

## 🎯 使用说明

启动程序后：
1. 点击"生成模拟数据"创建测试数据
2. 在各模块间切换体验功能
3. 使用Excel导入导出功能
4. 查看数据可视化图表
5. 生成各种智慧报表

享受使用AI城建系统！'''
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ 创建文件: README.md")

def main():
    """主函数"""
    print("AI城建系统项目创建器")
    print("=" * 40)
    
    # 创建目录结构
    print("\n创建目录结构...")
    create_directory_structure()
    
    # 创建核心文件
    print("\n创建核心文件...")
    create_requirements_txt()
    create_main_py()
    create_run_py()
    create_init_files()
    create_readme()
    
    print("\n" + "=" * 40)
    print("✅ 项目结构创建完成！")
    print("\n📋 注意事项：")
    print("1. 还需要创建其他源代码文件（数据库、GUI等模块）")
    print("2. 运行 'pip install -r requirements.txt' 安装依赖")
    print("3. 完整的源代码文件请参考原始项目")
    print("\n🚀 下一步：")
    print("python run.py  # 测试基础框架")

if __name__ == "__main__":
    main()