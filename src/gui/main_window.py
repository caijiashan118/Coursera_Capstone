# -*- coding: utf-8 -*-
"""
主窗口界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.gui.basic_data_module import BasicDataModule
from src.gui.visualization_module import VisualizationModule  
from src.gui.report_module import ReportModule

class MainWindow:
    """主窗口类"""
    
    def __init__(self, root):
        self.root = root
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        
        # 设置主题
        try:
            style.theme_use('clam')
        except:
            pass
            
        # 自定义样式
        style.configure('Title.TLabel', font=('Microsoft YaHei', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Microsoft YaHei', 12, 'bold'))
        style.configure('Module.TButton', font=('Microsoft YaHei', 11), padding=10)
        
    def create_widgets(self):
        """创建界面控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="AI城建系统", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 创建Notebook控件（选项卡）
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 基础数据模块
        self.basic_data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_data_frame, text="基础数据管理")
        self.basic_data_module = BasicDataModule(self.basic_data_frame)
        
        # 数据可视化模块
        self.visualization_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visualization_frame, text="数据可视化")
        self.visualization_module = VisualizationModule(self.visualization_frame)
        
        # 智慧报表生成模块
        self.report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.report_frame, text="智慧报表生成")
        self.report_module = ReportModule(self.report_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
        # 绑定选项卡切换事件
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        # 状态标签
        ttk.Label(status_frame, text="状态：").grid(row=0, column=0, sticky=tk.W)
        self.status_var = tk.StringVar(value="系统就绪")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # 版本信息
        version_label = ttk.Label(status_frame, text="版本：v1.0.0")
        version_label.grid(row=0, column=2, sticky=tk.E)
        
    def on_tab_changed(self, event):
        """选项卡切换事件处理"""
        selected_tab = event.widget.tab('current')['text']
        self.update_status(f"切换到：{selected_tab}")
        
        # 刷新当前模块的数据
        current_index = self.notebook.index('current')
        if current_index == 0:  # 基础数据模块
            self.basic_data_module.refresh_data()
        elif current_index == 1:  # 数据可视化模块
            self.visualization_module.refresh_charts()
        elif current_index == 2:  # 报表生成模块
            self.report_module.refresh_reports()
            
    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def show_info(self, title, message):
        """显示信息对话框"""
        messagebox.showinfo(title, message)
        
    def show_error(self, title, message):
        """显示错误对话框"""
        messagebox.showerror(title, message)
        
    def show_warning(self, title, message):
        """显示警告对话框"""
        messagebox.showwarning(title, message)
        
    def ask_yes_no(self, title, message):
        """显示是否确认对话框"""
        return messagebox.askyesno(title, message)