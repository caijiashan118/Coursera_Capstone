#!/usr/bin/env python3
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
    main()