# -*- coding: utf-8 -*-
"""
基础数据管理模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime, date
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.db_manager import DatabaseManager
from src.models.project_models import MockDataGenerator, ProjectBasicInfo, FundingArrangement
from src.utils.excel_handler import ExcelHandler

class BasicDataModule:
    """基础数据管理模块"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DatabaseManager()
        self.excel_handler = ExcelHandler()
        self.mock_generator = MockDataGenerator()
        
        self.create_widgets()
        self.refresh_data()
        
    def create_widgets(self):
        """创建界面控件"""
        # 主框架
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 左侧控制面板
        self.create_control_panel(main_frame)
        
        # 右侧数据显示区域
        self.create_data_display(main_frame)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = ttk.LabelFrame(parent, text="数据管理", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 数据表选择
        ttk.Label(control_frame, text="选择数据表：").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.table_var = tk.StringVar(value="项目基本信息表")
        table_combo = ttk.Combobox(control_frame, textvariable=self.table_var, 
                                  values=["项目基本信息表", "资金安排表", "重点项目清单"], 
                                  state="readonly", width=20)
        table_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        table_combo.bind("<<ComboboxSelected>>", self.on_table_changed)
        
        # 按钮区域
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Excel导入导出按钮
        ttk.Button(button_frame, text="导入Excel", command=self.import_excel).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(button_frame, text="导出Excel", command=self.export_excel).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 数据操作按钮
        ttk.Separator(control_frame, orient='horizontal').grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(control_frame, text="添加记录", command=self.add_record).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(control_frame, text="编辑记录", command=self.edit_record).grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(control_frame, text="删除记录", command=self.delete_record).grid(row=6, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 模拟数据生成
        ttk.Separator(control_frame, orient='horizontal').grid(row=7, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(control_frame, text="生成模拟数据", command=self.generate_mock_data).grid(row=8, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(control_frame, text="清空所有数据", command=self.clear_all_data).grid(row=9, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 数据透视表
        ttk.Separator(control_frame, orient='horizontal').grid(row=10, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(control_frame, text="资金透视表", command=self.show_pivot_table).grid(row=11, column=0, sticky=(tk.W, tk.E), pady=2)
        
    def create_data_display(self, parent):
        """创建数据显示区域"""
        display_frame = ttk.LabelFrame(parent, text="数据列表", padding="10")
        display_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview控件
        self.tree = ttk.Treeview(display_frame)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", lambda e: self.edit_record())
        
    def on_table_changed(self, event=None):
        """表格选择改变事件"""
        self.refresh_data()
        
    def refresh_data(self):
        """刷新数据显示"""
        try:
            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            table_name = self.table_var.get()
            
            if table_name == "项目基本信息表":
                self.load_project_data()
            elif table_name == "资金安排表":
                self.load_funding_data()
            elif table_name == "重点项目清单":
                self.load_key_projects_data()
                
        except Exception as e:
            messagebox.showerror("错误", f"数据加载失败：{str(e)}")
            
    def load_project_data(self):
        """加载项目基本信息数据"""
        # 设置列标题
        columns = ("项目名称", "项目编码", "建设单位", "项目主管部门", "立项时间", 
                  "概算批复金额", "预计开工时间", "预计完工时间", "项目状态")
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # 设置列宽和标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=80)
            
        # 加载数据
        df = self.db_manager.get_all_projects()
        for _, row in df.iterrows():
            values = (
                row['project_name'], row['project_code'], row['construction_unit'],
                row['supervising_department'], row['approval_date'], 
                f"{row['budget_amount']:.2f}万元", row['planned_start_date'],
                row['planned_end_date'], row['project_status']
            )
            self.tree.insert("", "end", values=values)
            
    def load_funding_data(self):
        """加载资金安排数据"""
        columns = ("项目名称", "项目编码", "建设单位", "项目主管部门", "概算批复金额",
                  "资金批复金额", "批复日期", "资金性质", "经办人", "经办处室")
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=80)
            
        df = self.db_manager.get_all_funding()
        for _, row in df.iterrows():
            values = (
                row['project_name'], row['project_code'], row['construction_unit'],
                row['supervising_department'], f"{row['budget_amount']:.2f}万元",
                f"{row['funding_amount']:.2f}万元", row['approval_date'],
                row['funding_type'], row['operator'], row['operating_department']
            )
            self.tree.insert("", "end", values=values)
            
    def load_key_projects_data(self):
        """加载重点项目清单数据"""
        columns = ("项目编码", "项目名称", "优先级", "关键特征", "战略重要性")
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, minwidth=100)
            
        # 这里可以添加重点项目的数据加载逻辑
        # 暂时显示空数据
        
    def import_excel(self):
        """导入Excel文件"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择Excel文件",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if not file_path:
                return
                
            table_name = self.table_var.get()
            
            if table_name == "项目基本信息表":
                self.excel_handler.import_project_data(file_path, self.db_manager)
            elif table_name == "资金安排表":
                self.excel_handler.import_funding_data(file_path, self.db_manager)
                
            self.refresh_data()
            messagebox.showinfo("成功", "Excel数据导入成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"Excel导入失败：{str(e)}")
            
    def export_excel(self):
        """导出Excel文件"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="保存Excel文件",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if not file_path:
                return
                
            table_name = self.table_var.get()
            
            if table_name == "项目基本信息表":
                df = self.db_manager.get_all_projects()
                self.excel_handler.export_project_data(df, file_path)
            elif table_name == "资金安排表":
                df = self.db_manager.get_all_funding()
                self.excel_handler.export_funding_data(df, file_path)
                
            messagebox.showinfo("成功", f"数据已导出到：{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"Excel导出失败：{str(e)}")
            
    def add_record(self):
        """添加记录"""
        table_name = self.table_var.get()
        
        if table_name == "项目基本信息表":
            self.show_project_dialog()
        elif table_name == "资金安排表":
            self.show_funding_dialog()
            
    def edit_record(self):
        """编辑记录"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要编辑的记录")
            return
            
        # 获取选中行的数据
        item = selection[0]
        values = self.tree.item(item, "values")
        
        table_name = self.table_var.get()
        
        if table_name == "项目基本信息表":
            self.show_project_dialog(values)
        elif table_name == "资金安排表":
            self.show_funding_dialog(values)
            
    def delete_record(self):
        """删除记录"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的记录")
            return
            
        if not messagebox.askyesno("确认", "确定要删除选中的记录吗？"):
            return
            
        try:
            item = selection[0]
            values = self.tree.item(item, "values")
            
            table_name = self.table_var.get()
            
            if table_name == "项目基本信息表":
                project_code = values[1]  # 项目编码
                self.db_manager.delete_project(project_code)
            elif table_name == "资金安排表":
                # 这里需要根据具体需求实现资金安排的删除逻辑
                pass
                
            self.refresh_data()
            messagebox.showinfo("成功", "记录删除成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"删除记录失败：{str(e)}")
            
    def generate_mock_data(self):
        """生成模拟数据"""
        if not messagebox.askyesno("确认", "这将生成200个模拟项目和1000条资金安排数据，是否继续？"):
            return
            
        try:
            # 生成模拟项目数据
            projects = self.mock_generator.generate_mock_projects(200)
            
            for project in projects:
                data = (
                    project.project_name, project.project_code, project.construction_unit,
                    project.supervising_department, project.approval_date, project.budget_amount,
                    project.planned_start_date, project.planned_end_date, project.project_status
                )
                self.db_manager.insert_project_basic_info(data)
                
            # 生成模拟资金安排数据
            funding_list = self.mock_generator.generate_mock_funding(projects, 1000)
            
            for funding in funding_list:
                data = (
                    funding.project_name, funding.project_code, funding.construction_unit,
                    funding.supervising_department, funding.budget_amount, funding.funding_amount,
                    funding.approval_date, funding.funding_type, funding.operator, funding.operating_department
                )
                self.db_manager.insert_funding_arrangement(data)
                
            self.refresh_data()
            messagebox.showinfo("成功", "模拟数据生成成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成模拟数据失败：{str(e)}")
            
    def clear_all_data(self):
        """清空所有数据"""
        if not messagebox.askyesno("警告", "这将清空所有数据，此操作不可恢复，是否继续？"):
            return
            
        try:
            self.db_manager.clear_all_data()
            self.refresh_data()
            messagebox.showinfo("成功", "所有数据已清空！")
            
        except Exception as e:
            messagebox.showerror("错误", f"清空数据失败：{str(e)}")
            
    def show_pivot_table(self):
        """显示资金安排数据透视表"""
        try:
            pivot_df = self.db_manager.get_funding_pivot_table()
            
            # 创建新窗口显示透视表
            pivot_window = tk.Toplevel(self.parent)
            pivot_window.title("资金安排数据透视表")
            pivot_window.geometry("1000x600")
            
            # 创建Treeview显示透视表
            frame = ttk.Frame(pivot_window, padding="10")
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            pivot_window.columnconfigure(0, weight=1)
            pivot_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            
            tree = ttk.Treeview(frame)
            tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # 设置列
            columns = list(pivot_df.columns)
            tree["columns"] = columns
            tree["show"] = "headings"
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, minwidth=80)
                
            # 添加数据
            for _, row in pivot_df.iterrows():
                values = []
                for col in columns:
                    value = row[col]
                    if isinstance(value, (int, float)) and col not in ['project_code']:
                        values.append(f"{value:.2f}万元")
                    else:
                        values.append(str(value))
                tree.insert("", "end", values=values)
                
            # 添加滚动条
            v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            tree.configure(yscrollcommand=v_scrollbar.set)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成透视表失败：{str(e)}")
            
    def show_project_dialog(self, values=None):
        """显示项目信息对话框"""
        # 这里可以实现项目信息的添加/编辑对话框
        messagebox.showinfo("提示", "项目信息对话框功能待实现")
        
    def show_funding_dialog(self, values=None):
        """显示资金安排对话框"""
        # 这里可以实现资金安排信息的添加/编辑对话框
        messagebox.showinfo("提示", "资金安排对话框功能待实现")