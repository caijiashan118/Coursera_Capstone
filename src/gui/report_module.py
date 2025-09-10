# -*- coding: utf-8 -*-
"""
智慧报表生成模块
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime, date
import sys
from pathlib import Path
from io import BytesIO
import base64

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.db_manager import DatabaseManager
from src.utils.excel_handler import ExcelHandler

class ReportModule:
    """智慧报表生成模块"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DatabaseManager()
        self.excel_handler = ExcelHandler()
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面控件"""
        # 主框架
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # 左侧控制面板
        self.create_control_panel(main_frame)
        
        # 右侧报表显示区域
        self.create_report_display(main_frame)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = ttk.LabelFrame(parent, text="报表生成", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 报表类型选择
        ttk.Label(control_frame, text="选择报表类型：").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.report_var = tk.StringVar(value="项目总览报表")
        report_types = [
            "项目总览报表",
            "资金安排报表", 
            "项目进度报表",
            "部门统计报表",
            "债券资金报表",
            "月度汇总报表",
            "项目完成情况报表",
            "资金透视分析报表"
        ]
        
        for i, report_type in enumerate(report_types):
            ttk.Radiobutton(control_frame, text=report_type, variable=self.report_var,
                           value=report_type).grid(row=i+1, column=0, sticky=tk.W, pady=2)
            
        # 日期范围选择
        ttk.Separator(control_frame, orient='horizontal').grid(row=len(report_types)+1, column=0, 
                                                              sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(control_frame, text="报表日期范围：").grid(row=len(report_types)+2, column=0, sticky=tk.W)
        
        date_frame = ttk.Frame(control_frame)
        date_frame.grid(row=len(report_types)+3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(date_frame, text="开始日期：").grid(row=0, column=0, sticky=tk.W)
        self.start_date_var = tk.StringVar(value="2024-01-01")
        ttk.Entry(date_frame, textvariable=self.start_date_var, width=12).grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(date_frame, text="结束日期：").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.end_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.end_date_var, width=12).grid(row=1, column=1, padx=(5, 0), pady=(5, 0))
        
        # 操作按钮
        ttk.Separator(control_frame, orient='horizontal').grid(row=len(report_types)+4, column=0, 
                                                              sticky=(tk.W, tk.E), pady=10)
        
        button_row = len(report_types) + 5
        ttk.Button(control_frame, text="生成报表", 
                  command=self.generate_report).grid(row=button_row, column=0, 
                                                    sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(control_frame, text="导出Excel", 
                  command=self.export_report).grid(row=button_row+1, column=0, 
                                                  sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(control_frame, text="导出PDF", 
                  command=self.export_pdf).grid(row=button_row+2, column=0, 
                                               sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(control_frame, text="打印报表", 
                  command=self.print_report).grid(row=button_row+3, column=0, 
                                                 sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(control_frame, text="刷新数据", 
                  command=self.refresh_reports).grid(row=button_row+4, column=0, 
                                                    sticky=(tk.W, tk.E), pady=2)
        
    def create_report_display(self, parent):
        """创建报表显示区域"""
        display_frame = ttk.LabelFrame(parent, text="报表预览", padding="10")
        display_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=1)
        
        # 报表标题
        self.report_title_var = tk.StringVar(value="AI城建系统 - 智慧报表")
        title_label = ttk.Label(display_frame, textvariable=self.report_title_var, 
                               font=('Microsoft YaHei', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # 创建Treeview显示报表数据
        self.report_tree = ttk.Treeview(display_frame)
        self.report_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.report_tree.yview)
        v_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.report_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=self.report_tree.xview)
        h_scrollbar.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.report_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # 报表统计信息
        self.stats_frame = ttk.LabelFrame(display_frame, text="统计信息", padding="10")
        self.stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.stats_text = tk.Text(self.stats_frame, height=4, wrap=tk.WORD)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.stats_frame.columnconfigure(0, weight=1)
        
        # 显示欢迎信息
        self.show_welcome_report()
        
    def show_welcome_report(self):
        """显示欢迎报表"""
        self.report_title_var.set("AI城建系统 - 智慧报表生成模块")
        
        # 清空报表数据
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        # 设置欢迎列
        self.report_tree["columns"] = ("功能", "描述")
        self.report_tree["show"] = "headings"
        
        self.report_tree.heading("功能", text="功能")
        self.report_tree.heading("描述", text="描述")
        self.report_tree.column("功能", width=150)
        self.report_tree.column("描述", width=400)
        
        # 添加功能说明
        features = [
            ("项目总览报表", "显示所有项目的基本信息和概况"),
            ("资金安排报表", "展示各项目的资金安排详情"),
            ("项目进度报表", "分析项目的进度和完成情况"),
            ("部门统计报表", "统计各部门的项目数量和资金"),
            ("债券资金报表", "专门分析债券资金的使用情况"),
            ("月度汇总报表", "按月份汇总项目和资金数据"),
            ("项目完成情况报表", "分析项目完成度和状态分布"),
            ("资金透视分析报表", "提供资金安排的透视分析")
        ]
        
        for feature, description in features:
            self.report_tree.insert("", "end", values=(feature, description))
            
        # 显示统计信息
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, "欢迎使用AI城建系统智慧报表生成模块！\n\n"
                                   "请选择报表类型，设置日期范围，然后点击'生成报表'按钮。\n"
                                   "支持导出Excel、PDF格式，以及直接打印功能。")
        
    def generate_report(self):
        """生成报表"""
        try:
            report_type = self.report_var.get()
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()
            
            # 验证日期格式
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("错误", "日期格式不正确，请使用YYYY-MM-DD格式")
                return
                
            if report_type == "项目总览报表":
                self.generate_project_overview_report(start_date, end_date)
            elif report_type == "资金安排报表":
                self.generate_funding_report(start_date, end_date)
            elif report_type == "项目进度报表":
                self.generate_progress_report(start_date, end_date)
            elif report_type == "部门统计报表":
                self.generate_department_report(start_date, end_date)
            elif report_type == "债券资金报表":
                self.generate_bond_report(start_date, end_date)
            elif report_type == "月度汇总报表":
                self.generate_monthly_report(start_date, end_date)
            elif report_type == "项目完成情况报表":
                self.generate_completion_report(start_date, end_date)
            elif report_type == "资金透视分析报表":
                self.generate_pivot_report(start_date, end_date)
                
        except Exception as e:
            messagebox.showerror("错误", f"生成报表失败：{str(e)}")
            
    def generate_project_overview_report(self, start_date, end_date):
        """生成项目总览报表"""
        df = self.db_manager.get_all_projects()
        if df.empty:
            self.show_no_data_report("项目总览报表")
            return
            
        # 过滤日期范围
        df_filtered = self.filter_by_date_range(df, 'approval_date', start_date, end_date)
        
        self.report_title_var.set(f"项目总览报表 ({start_date} 至 {end_date})")
        
        # 设置列
        columns = ("项目名称", "项目编码", "建设单位", "主管部门", "概算金额", "项目状态", "立项时间")
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120, minwidth=80)
            
        # 清空现有数据
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        # 添加数据
        for _, row in df_filtered.iterrows():
            values = (
                row['project_name'], row['project_code'], row['construction_unit'],
                row['supervising_department'], f"{row['budget_amount']:.2f}万元",
                row['project_status'], row['approval_date']
            )
            self.report_tree.insert("", "end", values=values)
            
        # 生成统计信息
        self.generate_project_stats(df_filtered)
        
    def generate_funding_report(self, start_date, end_date):
        """生成资金安排报表"""
        df = self.db_manager.get_all_funding()
        if df.empty:
            self.show_no_data_report("资金安排报表")
            return
            
        df_filtered = self.filter_by_date_range(df, 'approval_date', start_date, end_date)
        
        self.report_title_var.set(f"资金安排报表 ({start_date} 至 {end_date})")
        
        columns = ("项目名称", "项目编码", "资金性质", "资金金额", "批复日期", "经办人", "经办处室")
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120, minwidth=80)
            
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        for _, row in df_filtered.iterrows():
            values = (
                row['project_name'], row['project_code'], row['funding_type'],
                f"{row['funding_amount']:.2f}万元", row['approval_date'],
                row['operator'], row['operating_department']
            )
            self.report_tree.insert("", "end", values=values)
            
        self.generate_funding_stats(df_filtered)
        
    def generate_progress_report(self, start_date, end_date):
        """生成项目进度报表"""
        df = self.db_manager.get_all_projects()
        if df.empty:
            self.show_no_data_report("项目进度报表")
            return
            
        df_filtered = self.filter_by_date_range(df, 'approval_date', start_date, end_date)
        
        self.report_title_var.set(f"项目进度报表 ({start_date} 至 {end_date})")
        
        # 计算项目进度（模拟）
        progress_mapping = {'完工': 100, '在建': 65, '续建': 45, '暂停': 20}
        df_filtered['progress'] = df_filtered['project_status'].map(progress_mapping)
        
        columns = ("项目名称", "项目编码", "项目状态", "进度", "开工时间", "计划完工时间")
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120, minwidth=80)
            
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        for _, row in df_filtered.iterrows():
            values = (
                row['project_name'], row['project_code'], row['project_status'],
                f"{row['progress']}%", row['planned_start_date'], row['planned_end_date']
            )
            self.report_tree.insert("", "end", values=values)
            
        self.generate_progress_stats(df_filtered)
        
    def generate_department_report(self, start_date, end_date):
        """生成部门统计报表"""
        projects_df = self.db_manager.get_all_projects()
        funding_df = self.db_manager.get_all_funding()
        
        if projects_df.empty:
            self.show_no_data_report("部门统计报表")
            return
            
        projects_filtered = self.filter_by_date_range(projects_df, 'approval_date', start_date, end_date)
        funding_filtered = self.filter_by_date_range(funding_df, 'approval_date', start_date, end_date)
        
        self.report_title_var.set(f"部门统计报表 ({start_date} 至 {end_date})")
        
        # 按部门统计
        dept_projects = projects_filtered.groupby('supervising_department').agg({
            'project_code': 'count',
            'budget_amount': 'sum'
        }).round(2)
        
        dept_funding = funding_filtered.groupby('supervising_department')['funding_amount'].sum().round(2)
        
        # 合并数据
        dept_stats = dept_projects.join(dept_funding, how='left', rsuffix='_funding')
        dept_stats.fillna(0, inplace=True)
        
        columns = ("主管部门", "项目数量", "概算总额", "资金安排总额")
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=150, minwidth=100)
            
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        for dept, row in dept_stats.iterrows():
            values = (
                dept, 
                int(row['project_code']),
                f"{row['budget_amount']:.2f}万元",
                f"{row['funding_amount']:.2f}万元"
            )
            self.report_tree.insert("", "end", values=values)
            
        self.generate_department_stats(dept_stats)
        
    def generate_bond_report(self, start_date, end_date):
        """生成债券资金报表"""
        df = self.db_manager.get_all_funding()
        if df.empty:
            self.show_no_data_report("债券资金报表")
            return
            
        # 筛选债券数据
        bond_df = df[df['funding_type'].isin(['一般债券', '专项债券'])]
        bond_filtered = self.filter_by_date_range(bond_df, 'approval_date', start_date, end_date)
        
        if bond_filtered.empty:
            self.show_no_data_report("债券资金报表（无债券数据）")
            return
            
        self.report_title_var.set(f"债券资金报表 ({start_date} 至 {end_date})")
        
        columns = ("项目名称", "项目编码", "债券类型", "债券金额", "批复日期", "经办处室")
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120, minwidth=80)
            
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        for _, row in bond_filtered.iterrows():
            values = (
                row['project_name'], row['project_code'], row['funding_type'],
                f"{row['funding_amount']:.2f}万元", row['approval_date'],
                row['operating_department']
            )
            self.report_tree.insert("", "end", values=values)
            
        self.generate_bond_stats(bond_filtered)
        
    def generate_monthly_report(self, start_date, end_date):
        """生成月度汇总报表"""
        funding_df = self.db_manager.get_all_funding()
        if funding_df.empty:
            self.show_no_data_report("月度汇总报表")
            return
            
        funding_filtered = self.filter_by_date_range(funding_df, 'approval_date', start_date, end_date)
        
        self.report_title_var.set(f"月度汇总报表 ({start_date} 至 {end_date})")
        
        # 按月份汇总
        funding_filtered['approval_date'] = pd.to_datetime(funding_filtered['approval_date'])
        funding_filtered['year_month'] = funding_filtered['approval_date'].dt.to_period('M')
        
        monthly_stats = funding_filtered.groupby('year_month').agg({
            'project_code': 'nunique',  # 项目数量
            'funding_amount': 'sum',    # 资金总额
            'funding_type': lambda x: x.value_counts().to_dict()  # 资金类型分布
        }).round(2)
        
        columns = ("月份", "项目数量", "资金总额", "主要资金类型")
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=150, minwidth=100)
            
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        for month, row in monthly_stats.iterrows():
            # 获取主要资金类型
            funding_types = row['funding_type']
            main_type = max(funding_types.items(), key=lambda x: x[1])[0] if funding_types else "无"
            
            values = (
                str(month),
                int(row['project_code']),
                f"{row['funding_amount']:.2f}万元",
                main_type
            )
            self.report_tree.insert("", "end", values=values)
            
        self.generate_monthly_stats(monthly_stats)
        
    def generate_completion_report(self, start_date, end_date):
        """生成项目完成情况报表"""
        df = self.db_manager.get_all_projects()
        if df.empty:
            self.show_no_data_report("项目完成情况报表")
            return
            
        df_filtered = self.filter_by_date_range(df, 'approval_date', start_date, end_date)
        
        self.report_title_var.set(f"项目完成情况报表 ({start_date} 至 {end_date})")
        
        # 按状态统计
        status_stats = df_filtered['project_status'].value_counts()
        
        columns = ("项目状态", "项目数量", "占比", "概算总额")
        self.report_tree["columns"] = columns
        self.report_tree["show"] = "headings"
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120, minwidth=80)
            
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        total_projects = len(df_filtered)
        for status, count in status_stats.items():
            # 计算该状态下的概算总额
            status_budget = df_filtered[df_filtered['project_status'] == status]['budget_amount'].sum()
            percentage = (count / total_projects * 100) if total_projects > 0 else 0
            
            values = (
                status,
                count,
                f"{percentage:.1f}%",
                f"{status_budget:.2f}万元"
            )
            self.report_tree.insert("", "end", values=values)
            
        self.generate_completion_stats(df_filtered, status_stats)
        
    def generate_pivot_report(self, start_date, end_date):
        """生成资金透视分析报表"""
        try:
            pivot_df = self.db_manager.get_funding_pivot_table()
            if pivot_df.empty:
                self.show_no_data_report("资金透视分析报表")
                return
                
            self.report_title_var.set(f"资金透视分析报表 ({start_date} 至 {end_date})")
            
            # 设置列
            columns = list(pivot_df.columns)
            self.report_tree["columns"] = columns
            self.report_tree["show"] = "headings"
            
            for col in columns:
                self.report_tree.heading(col, text=col)
                self.report_tree.column(col, width=100, minwidth=80)
                
            for item in self.report_tree.get_children():
                self.report_tree.delete(item)
                
            # 添加数据
            for _, row in pivot_df.iterrows():
                values = []
                for col in columns:
                    value = row[col]
                    if isinstance(value, (int, float)) and col not in ['project_code']:
                        values.append(f"{value:.2f}万元")
                    else:
                        values.append(str(value))
                self.report_tree.insert("", "end", values=values)
                
            self.generate_pivot_stats(pivot_df)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成透视分析报表失败：{str(e)}")
        
    def filter_by_date_range(self, df, date_column, start_date, end_date):
        """根据日期范围过滤数据"""
        try:
            if date_column not in df.columns:
                return df
                
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='coerce')
            
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            mask = (df_copy[date_column] >= start_dt) & (df_copy[date_column] <= end_dt)
            return df_copy[mask]
            
        except Exception:
            return df
            
    def show_no_data_report(self, report_name):
        """显示无数据报表"""
        self.report_title_var.set(f"{report_name} - 暂无数据")
        
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        self.report_tree["columns"] = ("提示",)
        self.report_tree["show"] = "headings"
        self.report_tree.heading("提示", text="提示信息")
        self.report_tree.column("提示", width=400)
        
        self.report_tree.insert("", "end", values=("暂无数据，请先生成模拟数据或导入数据",))
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, f"{report_name}暂无可用数据。\n请先在基础数据模块中生成模拟数据或导入数据。")
        
    def generate_project_stats(self, df):
        """生成项目统计信息"""
        total_projects = len(df)
        total_budget = df['budget_amount'].sum()
        avg_budget = df['budget_amount'].mean() if total_projects > 0 else 0
        
        status_dist = df['project_status'].value_counts()
        
        stats_text = f"项目总数：{total_projects} 个\n"
        stats_text += f"概算总额：{total_budget:.2f} 万元\n"
        stats_text += f"平均概算：{avg_budget:.2f} 万元\n"
        stats_text += f"状态分布：{', '.join([f'{k}({v}个)' for k, v in status_dist.items()])}"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def generate_funding_stats(self, df):
        """生成资金统计信息"""
        total_funding = df['funding_amount'].sum()
        total_records = len(df)
        avg_funding = df['funding_amount'].mean() if total_records > 0 else 0
        
        type_dist = df['funding_type'].value_counts()
        
        stats_text = f"资金安排记录：{total_records} 条\n"
        stats_text += f"资金总额：{total_funding:.2f} 万元\n"
        stats_text += f"平均金额：{avg_funding:.2f} 万元\n"
        stats_text += f"类型分布：{', '.join([f'{k}({v}条)' for k, v in type_dist.head(3).items()])}"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def generate_progress_stats(self, df):
        """生成进度统计信息"""
        avg_progress = df['progress'].mean() if len(df) > 0 else 0
        completed_projects = len(df[df['project_status'] == '完工'])
        in_progress_projects = len(df[df['project_status'].isin(['在建', '续建'])])
        
        stats_text = f"项目总数：{len(df)} 个\n"
        stats_text += f"平均进度：{avg_progress:.1f}%\n"
        stats_text += f"已完工：{completed_projects} 个\n"
        stats_text += f"进行中：{in_progress_projects} 个"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def generate_department_stats(self, df):
        """生成部门统计信息"""
        total_depts = len(df)
        total_projects = df['project_code'].sum()
        total_budget = df['budget_amount'].sum()
        total_funding = df['funding_amount'].sum()
        
        stats_text = f"统计部门：{total_depts} 个\n"
        stats_text += f"项目总数：{int(total_projects)} 个\n"
        stats_text += f"概算总额：{total_budget:.2f} 万元\n"
        stats_text += f"资金总额：{total_funding:.2f} 万元"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def generate_bond_stats(self, df):
        """生成债券统计信息"""
        general_bonds = df[df['funding_type'] == '一般债券']['funding_amount'].sum()
        special_bonds = df[df['funding_type'] == '专项债券']['funding_amount'].sum()
        total_bonds = general_bonds + special_bonds
        
        stats_text = f"债券资金总额：{total_bonds:.2f} 万元\n"
        stats_text += f"一般债券：{general_bonds:.2f} 万元\n"
        stats_text += f"专项债券：{special_bonds:.2f} 万元\n"
        stats_text += f"涉及项目：{df['project_code'].nunique()} 个"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def generate_monthly_stats(self, df):
        """生成月度统计信息"""
        total_months = len(df)
        total_projects = df['project_code'].sum() if len(df) > 0 else 0
        total_funding = df['funding_amount'].sum() if len(df) > 0 else 0
        avg_monthly_funding = total_funding / total_months if total_months > 0 else 0
        
        stats_text = f"统计月份：{total_months} 个月\n"
        stats_text += f"涉及项目：{int(total_projects)} 个\n"
        stats_text += f"资金总额：{total_funding:.2f} 万元\n"
        stats_text += f"月均资金：{avg_monthly_funding:.2f} 万元"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def generate_completion_stats(self, df, status_stats):
        """生成完成情况统计信息"""
        completion_rate = (status_stats.get('完工', 0) / len(df) * 100) if len(df) > 0 else 0
        in_progress_rate = ((status_stats.get('在建', 0) + status_stats.get('续建', 0)) / len(df) * 100) if len(df) > 0 else 0
        
        stats_text = f"项目总数：{len(df)} 个\n"
        stats_text += f"完工率：{completion_rate:.1f}%\n"
        stats_text += f"在建率：{in_progress_rate:.1f}%\n"
        stats_text += f"暂停项目：{status_stats.get('暂停', 0)} 个"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def generate_pivot_stats(self, df):
        """生成透视表统计信息"""
        total_projects = len(df)
        
        # 计算债券资金统计
        bond_total = 0
        if '债券资金合计' in df.columns:
            bond_total = df['债券资金合计'].sum()
            
        stats_text = f"透视表项目数：{total_projects} 个\n"
        stats_text += f"债券资金合计：{bond_total:.2f} 万元\n"
        stats_text += f"数据维度：{len(df.columns)} 个\n"
        stats_text += "按项目编码分组，展示各资金性质分布情况"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def export_report(self):
        """导出Excel报表"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="导出Excel报表",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if not file_path:
                return
                
            # 获取当前显示的数据
            data = []
            columns = self.report_tree["columns"]
            
            for item in self.report_tree.get_children():
                values = self.report_tree.item(item, "values")
                data.append(values)
                
            if not data:
                messagebox.showwarning("警告", "没有数据可导出")
                return
                
            # 创建DataFrame并导出
            df = pd.DataFrame(data, columns=columns)
            
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='报表数据', index=False)
                
                # 设置列宽
                worksheet = writer.sheets['报表数据']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                    
            messagebox.showinfo("成功", f"报表已导出到：{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出报表失败：{str(e)}")
            
    def export_pdf(self):
        """导出PDF报表"""
        messagebox.showinfo("提示", "PDF导出功能待实现")
        
    def print_report(self):
        """打印报表"""
        messagebox.showinfo("提示", "打印功能待实现")
        
    def refresh_reports(self):
        """刷新报表数据"""
        try:
            self.generate_report()
            messagebox.showinfo("成功", "报表数据已刷新")
        except Exception as e:
            messagebox.showerror("错误", f"刷新报表失败：{str(e)}")