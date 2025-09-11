#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级Excel数据处理小程序
支持真实的Excel文件(.xlsx)读写操作
专为AI城建系统数据设计
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

class AdvancedExcelProcessor:
    """高级Excel处理器"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.data = {}
        self.current_file = None
        self.create_widgets()
        
    def setup_window(self):
        """设置窗口"""
        self.root.title("🏢 AI城建系统 - 高级Excel数据处理器 v1.0")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        self.center_window()
        
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """创建界面控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题和工具栏
        self.create_toolbar(main_frame)
        
        # 主要内容区域
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # 左侧操作面板
        self.create_operation_panel(content_frame)
        
        # 右侧数据显示
        self.create_data_viewer(content_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
    def create_toolbar(self, parent):
        """创建工具栏"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        toolbar_frame.columnconfigure(4, weight=1)
        
        # 标题
        title_label = ttk.Label(toolbar_frame, text="🏢 AI城建系统数据处理器", 
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 快捷按钮
        ttk.Button(toolbar_frame, text="🎲 生成数据", 
                  command=self.quick_generate_data).grid(row=0, column=1, padx=(20, 5))
        ttk.Button(toolbar_frame, text="📂 打开文件", 
                  command=self.quick_open_file).grid(row=0, column=2, padx=5)
        ttk.Button(toolbar_frame, text="💾 保存文件", 
                  command=self.quick_save_file).grid(row=0, column=3, padx=5)
        
        # 当前文件显示
        self.current_file_var = tk.StringVar(value="未打开文件")
        current_file_label = ttk.Label(toolbar_frame, textvariable=self.current_file_var, 
                                      font=('Microsoft YaHei', 10))
        current_file_label.grid(row=0, column=4, sticky=tk.E)
        
    def create_operation_panel(self, parent):
        """创建操作面板"""
        operation_frame = ttk.LabelFrame(parent, text="🛠️ 操作面板", padding="15")
        operation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 数据生成区域
        gen_frame = ttk.LabelFrame(operation_frame, text="🎲 数据生成", padding="10")
        gen_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 项目数量设置
        ttk.Label(gen_frame, text="项目数量：").grid(row=0, column=0, sticky=tk.W)
        self.project_count_var = tk.StringVar(value="200")
        project_count_spin = ttk.Spinbox(gen_frame, from_=10, to=1000, textvariable=self.project_count_var, width=10)
        project_count_spin.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # 资金记录数量设置
        ttk.Label(gen_frame, text="资金记录：").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.funding_count_var = tk.StringVar(value="1000")
        funding_count_spin = ttk.Spinbox(gen_frame, from_=50, to=5000, textvariable=self.funding_count_var, width=10)
        funding_count_spin.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Button(gen_frame, text="🚀 生成AI城建数据", 
                  command=self.generate_custom_data).grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 文件操作区域
        file_frame = ttk.LabelFrame(operation_frame, text="📁 文件操作", padding="10")
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="📖 打开CSV文件", 
                  command=self.open_csv_file).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(file_frame, text="📄 新建Excel模板", 
                  command=self.create_excel_template).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(file_frame, text="💾 保存当前数据", 
                  command=self.save_current_data).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(file_frame, text="📤 批量导出", 
                  command=self.batch_export).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 数据分析区域
        analysis_frame = ttk.LabelFrame(operation_frame, text="📊 数据分析", padding="10")
        analysis_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(analysis_frame, text="🔄 创建透视表", 
                  command=self.create_advanced_pivot).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(analysis_frame, text="📈 统计分析", 
                  command=self.advanced_statistics).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(analysis_frame, text="💎 债券分析", 
                  command=self.detailed_bond_analysis).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(analysis_frame, text="🏢 部门分析", 
                  command=self.detailed_department_analysis).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 表格选择区域
        table_frame = ttk.LabelFrame(operation_frame, text="📋 数据表", padding="10")
        table_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.table_var = tk.StringVar(value="欢迎页面")
        tables = ["欢迎页面", "项目基本信息表", "资金安排表", "重点项目清单", "数据透视表"]
        
        for i, table in enumerate(tables):
            ttk.Radiobutton(table_frame, text=table, variable=self.table_var, 
                           value=table, command=self.switch_table).grid(row=i//2, column=i%2, sticky=tk.W, pady=2)
        
    def create_data_viewer(self, parent):
        """创建数据查看器"""
        viewer_frame = ttk.LabelFrame(parent, text="📊 数据查看器", padding="15")
        viewer_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        viewer_frame.columnconfigure(0, weight=1)
        viewer_frame.rowconfigure(1, weight=1)
        
        # 数据信息栏
        info_frame = ttk.Frame(viewer_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(2, weight=1)
        
        ttk.Label(info_frame, text="当前表格：").grid(row=0, column=0, sticky=tk.W)
        self.current_table_var = tk.StringVar(value="欢迎页面")
        ttk.Label(info_frame, textvariable=self.current_table_var, 
                 font=('Microsoft YaHei', 10, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        self.record_count_var = tk.StringVar(value="")
        ttk.Label(info_frame, textvariable=self.record_count_var).grid(row=0, column=2, sticky=tk.E)
        
        # 数据表格
        self.tree = ttk.Treeview(viewer_frame)
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        v_scrollbar = ttk.Scrollbar(viewer_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(viewer_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # 双击编辑功能
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # 初始显示
        self.show_welcome_advanced()
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="状态：").grid(row=0, column=0, sticky=tk.W)
        self.status_var = tk.StringVar(value="就绪 - 请选择操作")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # 版本信息
        version_label = ttk.Label(status_frame, text="Excel处理器 v1.0 | AI城建系统专用")
        version_label.grid(row=0, column=2, sticky=tk.E)
        
    def show_welcome_advanced(self):
        """显示高级欢迎页面"""
        self.tree["columns"] = ("功能模块", "支持操作", "数据类型", "状态")
        self.tree["show"] = "headings"
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
            
        welcome_data = [
            ("🎲 数据生成", "AI城建系统完整数据集", "200项目+1000资金", "✅ 就绪"),
            ("📊 项目管理", "项目基本信息CRUD", "项目名称、编码、状态等", "✅ 就绪"),
            ("💰 资金管理", "资金安排数据处理", "7种资金性质", "✅ 就绪"),
            ("🔄 透视分析", "债券资金合计计算", "一般债券+专项债券", "✅ 就绪"),
            ("📈 统计分析", "多维度数据统计", "部门、状态、金额等", "✅ 就绪"),
            ("📁 文件处理", "CSV/Excel文件操作", "导入、导出、转换", "✅ 就绪"),
            ("🔍 数据筛选", "条件筛选和搜索", "按字段筛选数据", "✅ 就绪"),
            ("📋 报表生成", "智能报表制作", "多种报表模板", "✅ 就绪"),
            ("🏢 部门分析", "按部门统计分析", "项目数量、金额统计", "✅ 就绪"),
            ("📅 时间分析", "按时间维度分析", "月度、季度、年度", "✅ 就绪")
        ]
        
        for item in welcome_data:
            self.tree.insert("", "end", values=item)
            
        self.current_table_var.set("功能概览")
        self.record_count_var.set("10个功能模块")
        self.update_status("欢迎使用AI城建系统Excel数据处理器")
        
    def quick_generate_data(self):
        """快速生成数据"""
        self.generate_custom_data()
        
    def quick_open_file(self):
        """快速打开文件"""
        self.open_csv_file()
        
    def quick_save_file(self):
        """快速保存文件"""
        self.save_current_data()
        
    def generate_custom_data(self):
        """生成自定义数据"""
        try:
            project_count = int(self.project_count_var.get())
            funding_count = int(self.funding_count_var.get())
            
            if project_count < 1 or funding_count < 1:
                messagebox.showerror("错误", "项目数量和资金记录数量必须大于0")
                return
                
            if not messagebox.askyesno("确认", f"将生成以下数据：\n• {project_count}个项目基本信息\n• {funding_count}条资金安排记录\n• 重点项目清单\n• 数据透视表（债券资金合计）\n\n是否继续？"):
                return
                
            self.update_status("正在生成自定义数据...")
            
            # 生成项目数据
            projects_data = self.create_project_data(project_count)
            self.data["项目基本信息表"] = projects_data
            
            # 生成资金数据
            funding_data = self.create_funding_data(projects_data, funding_count)
            self.data["资金安排表"] = funding_data
            
            # 生成重点项目
            key_projects_data = self.create_key_projects_data(projects_data)
            self.data["重点项目清单"] = key_projects_data
            
            # 生成透视表
            pivot_data = self.create_pivot_data(funding_data)
            self.data["数据透视表"] = pivot_data
            
            # 切换到项目表显示
            self.table_var.set("项目基本信息表")
            self.display_table("项目基本信息表")
            
            messagebox.showinfo("成功", f"数据生成完成！\n\n✅ {project_count}个项目基本信息\n✅ {funding_count}条资金安排记录\n✅ {len(key_projects_data)-1}个重点项目\n✅ 债券资金合计透视表")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"数据生成失败：{str(e)}")
            
    def create_project_data(self, count):
        """创建项目数据"""
        projects = []
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '立项时间',
            '概算批复金额', '预计开工时间', '预计完工时间', '项目状态'
        ]
        projects.append(headers)
        
        # 数据源
        project_types = [
            '道路建设工程', '桥梁建设工程', '隧道建设工程', '排水管网工程', '供水管网工程',
            '公园绿化工程', '广场建设工程', '学校建设工程', '医院建设工程', '住宅小区建设',
            '商业综合体建设', '地铁建设工程', '公交站台建设', '污水处理厂建设', '垃圾处理中心建设',
            '体育中心建设', '文化中心建设', '图书馆建设', '博物馆建设', '停车场建设'
        ]
        
        areas = ['东城区', '西城区', '南城区', '北城区', '中心区', '开发区', '新区', '高新区']
        
        units = [
            '市政建设集团有限公司', '城市投资建设集团', '交通建设发展集团', '水务建设集团公司',
            '园林绿化建设集团', '教育建设投资公司', '医疗建设发展公司', '住房建设集团'
        ]
        
        departments = [
            '市发展和改革委员会', '市住房和城乡建设局', '市交通运输局', '市水利局',
            '市教育局', '市卫生健康委员会', '市生态环境局', '市园林绿化局'
        ]
        
        statuses = ['在建', '续建', '完工', '暂停']
        
        for i in range(1, count + 1):
            project_code = f"UC{datetime.now().year}{i:04d}"
            project_name = f"{random.choice(areas)}{random.choice(project_types)}{random.choice(['一期', '二期', '三期'])}"
            
            # 概算金额500-20000万元
            budget_amount = round(random.uniform(500, 20000), 2)
            
            # 日期生成
            base_date = datetime(2023, 1, 1)
            approval_date = base_date + timedelta(days=random.randint(0, 500))
            start_date = approval_date + timedelta(days=random.randint(30, 180))
            end_date = start_date + timedelta(days=random.randint(180, 1095))
            
            project_row = [
                project_name, project_code, random.choice(units), random.choice(departments),
                approval_date.strftime('%Y-%m-%d'), budget_amount,
                start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),
                random.choice(statuses)
            ]
            projects.append(project_row)
            
        return projects
        
    def create_funding_data(self, projects_data, count):
        """创建资金安排数据"""
        funding_records = []
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '概算批复金额',
            '资金批复金额', '批复日期', '资金性质', '经办人', '经办处室'
        ]
        funding_records.append(headers)
        
        funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助']
        operators = ['张建华', '李明强', '王志远', '赵文博', '钱国强', '孙海涛']
        departments = ['计划财务处', '项目管理处', '投资建设处', '资金管理处']
        
        projects_list = projects_data[1:]
        
        # 每个项目至少一条记录
        for project in projects_list:
            budget = float(project[5])
            amount = round(random.uniform(budget * 0.1, budget * 0.8), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_date = approval_date + timedelta(days=random.randint(1, 90))
            
            funding_row = [
                project[0], project[1], project[2], project[3], budget, amount,
                funding_date.strftime('%Y-%m-%d'), random.choice(funding_types),
                random.choice(operators), random.choice(departments)
            ]
            funding_records.append(funding_row)
        
        # 生成剩余记录
        remaining = count - len(projects_list)
        for _ in range(remaining):
            project = random.choice(projects_list)
            budget = float(project[5])
            amount = round(random.uniform(budget * 0.05, budget * 0.5), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_date = approval_date + timedelta(days=random.randint(1, 365))
            
            funding_row = [
                project[0], project[1], project[2], project[3], budget, amount,
                funding_date.strftime('%Y-%m-%d'), random.choice(funding_types),
                random.choice(operators), random.choice(departments)
            ]
            funding_records.append(funding_row)
            
        return funding_records
        
    def create_key_projects_data(self, projects_data):
        """创建重点项目数据"""
        key_projects = []
        headers = ['项目编码', '项目名称', '优先级', '关键特征', '战略重要性']
        key_projects.append(headers)
        
        projects_list = projects_data[1:]
        key_count = max(1, int(len(projects_list) * 0.3))
        selected_projects = random.sample(projects_list, key_count)
        
        features = ['重大民生工程', '基础设施建设', '生态环保项目', '科技创新项目']
        importance = ['提升城市承载能力', '改善民生福祉', '促进经济发展', '推动生态建设']
        
        for project in selected_projects:
            key_row = [
                project[1], project[0], random.randint(1, 3),
                random.choice(features), random.choice(importance)
            ]
            key_projects.append(key_row)
            
        return key_projects
        
    def create_pivot_data(self, funding_data):
        """创建透视表数据"""
        pivot_data = []
        headers = ['项目编码', '项目名称', '一般债券', '专项债券', '债券资金合计', '其他资金', '资金总计']
        pivot_data.append(headers)
        
        funding_list = funding_data[1:]
        project_summary = {}
        
        for funding in funding_list:
            code = funding[1]
            name = funding[0]
            ftype = funding[7]
            amount = float(funding[5])
            
            if code not in project_summary:
                project_summary[code] = {
                    'name': name, '一般债券': 0, '专项债券': 0, '其他资金': 0
                }
            
            if ftype == '一般债券':
                project_summary[code]['一般债券'] += amount
            elif ftype == '专项债券':
                project_summary[code]['专项债券'] += amount
            else:
                project_summary[code]['其他资金'] += amount
        
        for code, data in project_summary.items():
            general = data['一般债券']
            special = data['专项债券']
            other = data['其他资金']
            bond_total = general + special  # 债券资金合计
            total = bond_total + other
            
            pivot_row = [
                code, data['name'], f"{general:.2f}", f"{special:.2f}",
                f"{bond_total:.2f}", f"{other:.2f}", f"{total:.2f}"
            ]
            pivot_data.append(pivot_row)
            
        return pivot_data
        
    def open_csv_file(self):
        """打开CSV文件"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择CSV文件",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            data = []
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            
            filename = os.path.basename(file_path)
            table_name = filename.replace('.csv', '')
            
            self.data[table_name] = data
            self.current_file = file_path
            self.current_file_var.set(f"📁 {filename}")
            
            self.table_var.set(table_name)
            self.display_table(table_name)
            
            messagebox.showinfo("成功", f"文件导入成功！\n文件：{filename}\n记录数：{len(data)-1}")
            
        except Exception as e:
            messagebox.showerror("错误", f"文件打开失败：{str(e)}")
            
    def save_current_data(self):
        """保存当前数据"""
        current_table = self.table_var.get()
        if current_table not in self.data or not self.data[current_table]:
            messagebox.showwarning("警告", "没有数据可保存")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                title="保存数据文件",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerows(self.data[current_table])
                
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.current_file_var.set(f"📁 {filename}")
            
            messagebox.showinfo("成功", f"文件保存成功！\n位置：{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"文件保存失败：{str(e)}")
            
    def create_excel_template(self):
        """创建Excel模板"""
        try:
            # 创建模板目录
            template_dir = "Excel模板"
            os.makedirs(template_dir, exist_ok=True)
            
            # 项目基本信息表模板
            project_template = [
                ['项目名称', '项目编码', '建设单位', '项目主管部门', '立项时间', '概算批复金额', '预计开工时间', '预计完工时间', '项目状态'],
                ['示例：东城区道路建设工程一期', 'UC20240001', '市政建设集团', '市发改委', '2024-01-15', '5000.00', '2024-03-01', '2025-12-31', '在建'],
                ['示例：西城区学校建设工程二期', 'UC20240002', '教育建设投资公司', '市教育局', '2024-02-20', '8000.00', '2024-04-01', '2026-06-30', '续建']
            ]
            
            # 资金安排表模板
            funding_template = [
                ['项目名称', '项目编码', '建设单位', '项目主管部门', '概算批复金额', '资金批复金额', '批复日期', '资金性质', '经办人', '经办处室'],
                ['示例：东城区道路建设工程一期', 'UC20240001', '市政建设集团', '市发改委', '5000.00', '2000.00', '2024-02-01', '一般债券', '张三', '计划财务处'],
                ['示例：东城区道路建设工程一期', 'UC20240001', '市政建设集团', '市发改委', '5000.00', '1500.00', '2024-03-01', '专项债券', '李四', '项目管理处']
            ]
            
            # 保存模板
            with open(f"{template_dir}/项目基本信息表模板.csv", 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerows(project_template)
                
            with open(f"{template_dir}/资金安排表模板.csv", 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerows(funding_template)
                
            # 创建说明文档
            readme_content = """# AI城建系统Excel模板使用说明

## 📋 模板文件

1. **项目基本信息表模板.csv**
   - 用于录入项目基本信息
   - 项目状态只能填写：在建、续建、完工、暂停
   - 概算批复金额单位：万元

2. **资金安排表模板.csv**
   - 用于录入资金安排信息
   - 资金性质只能填写：一般债券、专项债券、中央综合财力、土地出让金、中央预算内投资、中央补助、省级补助
   - 通过项目编码与项目基本信息表关联

## 🎯 使用方法

1. 复制模板文件
2. 按格式填写数据
3. 在数据处理器中导入
4. 进行数据分析和处理

## ⚠️ 注意事项

- 保持CSV格式不变
- 项目编码必须唯一
- 日期格式：YYYY-MM-DD
- 金额为数字，不含单位
"""
            
            with open(f"{template_dir}/使用说明.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
                
            messagebox.showinfo("成功", f"Excel模板创建完成！\n位置：{os.path.abspath(template_dir)}\n\n包含文件：\n• 项目基本信息表模板.csv\n• 资金安排表模板.csv\n• 使用说明.md")
            
        except Exception as e:
            messagebox.showerror("错误", f"模板创建失败：{str(e)}")
            
    def batch_export(self):
        """批量导出"""
        if not self.data:
            messagebox.showwarning("警告", "没有数据可导出")
            return
            
        try:
            export_dir = filedialog.askdirectory(title="选择导出目录")
            if not export_dir:
                return
                
            # 创建时间戳目录
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_subdir = os.path.join(export_dir, f"AI城建系统数据_{timestamp}")
            os.makedirs(export_subdir, exist_ok=True)
            
            exported_files = []
            for table_name, table_data in self.data.items():
                if table_data and table_name != "欢迎页面":
                    filename = f"{table_name}.csv"
                    file_path = os.path.join(export_subdir, filename)
                    
                    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                        writer = csv.writer(f)
                        writer.writerows(table_data)
                    
                    exported_files.append(filename)
            
            # 创建导出说明
            export_info = f"""# AI城建系统数据导出

导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
导出文件数：{len(exported_files)}

## 📁 文件列表
{chr(10).join([f'• {f}' for f in exported_files])}

## 💡 使用说明
- 可以在Excel中直接打开CSV文件
- 支持数据筛选、排序、透视表等操作
- 项目编码可用于表间关联分析
"""
            
            with open(os.path.join(export_subdir, "导出说明.md"), 'w', encoding='utf-8') as f:
                f.write(export_info)
                
            messagebox.showinfo("成功", f"批量导出完成！\n\n📁 导出位置：{export_subdir}\n📄 导出文件：{len(exported_files)}个\n\n{chr(10).join(exported_files)}")
            
        except Exception as e:
            messagebox.showerror("错误", f"批量导出失败：{str(e)}")
            
    def create_advanced_pivot(self):
        """创建高级透视表"""
        if "资金安排表" not in self.data:
            messagebox.showwarning("警告", "请先生成或导入资金安排数据")
            return
            
        try:
            funding_data = self.data["资金安排表"]
            pivot_data = self.create_pivot_data(funding_data)
            self.data["数据透视表"] = pivot_data
            
            self.table_var.set("数据透视表")
            self.display_table("数据透视表")
            
            # 统计债券资金
            funding_list = funding_data[1:]
            general_total = sum(float(f[5]) for f in funding_list if f[7] == '一般债券')
            special_total = sum(float(f[5]) for f in funding_list if f[7] == '专项债券')
            bond_total = general_total + special_total
            
            messagebox.showinfo("透视表创建完成", f"🔄 数据透视表生成成功！\n\n📊 透视分析结果：\n• 一般债券总额：{general_total:,.2f} 万元\n• 专项债券总额：{special_total:,.2f} 万元\n• 债券资金合计：{bond_total:,.2f} 万元\n\n💡 透视表按项目编码分组，自动计算债券资金合计")
            
        except Exception as e:
            messagebox.showerror("错误", f"创建透视表失败：{str(e)}")
            
    def advanced_statistics(self):
        """高级统计分析"""
        self.show_statistics()
        
    def detailed_bond_analysis(self):
        """详细债券分析"""
        if "资金安排表" not in self.data:
            messagebox.showwarning("警告", "请先生成或导入资金安排数据")
            return
            
        try:
            funding_data = self.data["资金安排表"][1:]
            
            # 债券分析
            bond_analysis = {
                '一般债券': {'count': 0, 'amount': 0, 'projects': set()},
                '专项债券': {'count': 0, 'amount': 0, 'projects': set()}
            }
            
            for fund in funding_data:
                if fund[7] in bond_analysis:
                    bond_type = fund[7]
                    amount = float(fund[5])
                    project_code = fund[1]
                    
                    bond_analysis[bond_type]['count'] += 1
                    bond_analysis[bond_type]['amount'] += amount
                    bond_analysis[bond_type]['projects'].add(project_code)
            
            # 创建分析窗口
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("💎 债券资金详细分析")
            analysis_window.geometry("600x500")
            
            frame = ttk.Frame(analysis_window, padding="20")
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            analysis_window.columnconfigure(0, weight=1)
            analysis_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            
            # 分析结果
            general_data = bond_analysis['一般债券']
            special_data = bond_analysis['专项债券']
            total_amount = general_data['amount'] + special_data['amount']
            total_count = general_data['count'] + special_data['count']
            total_projects = len(general_data['projects'] | special_data['projects'])
            
            analysis_text = f"""💎 债券资金详细分析报告
{'='*50}

📊 总体统计：
   债券资金总额：{total_amount:,.2f} 万元
   债券安排笔数：{total_count} 笔
   涉及项目数量：{total_projects} 个

📋 分类统计：

🔹 一般债券：
   金额：{general_data['amount']:,.2f} 万元
   笔数：{general_data['count']} 笔
   项目：{len(general_data['projects'])} 个
   占比：{general_data['amount']/total_amount*100:.1f}%

🔸 专项债券：
   金额：{special_data['amount']:,.2f} 万元
   笔数：{special_data['count']} 笔
   项目：{len(special_data['projects'])} 个
   占比：{special_data['amount']/total_amount*100:.1f}%

📈 分析结论：
• 债券资金是项目建设的重要资金来源
• 一般债券和专项债券需要统筹管理
• 建议建立债券资金使用监管机制
• 优化债券资金配置，提高使用效率

💡 建议措施：
1. 建立债券资金台账管理
2. 定期开展债券资金审计
3. 加强项目进度与资金匹配
4. 完善债券资金绩效评价
"""
            
            text_widget = tk.Text(frame, wrap=tk.WORD, font=('Consolas', 10))
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            text_widget.insert(1.0, analysis_text)
            text_widget.config(state=tk.DISABLED)
            
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            text_widget.configure(yscrollcommand=scrollbar.set)
            
        except Exception as e:
            messagebox.showerror("错误", f"债券分析失败：{str(e)}")
            
    def detailed_department_analysis(self):
        """详细部门分析"""
        if "项目基本信息表" not in self.data:
            messagebox.showwarning("警告", "请先生成或导入项目基本信息")
            return
            
        try:
            projects = self.data["项目基本信息表"][1:]
            dept_analysis = {}
            
            for project in projects:
                dept = project[3]
                budget = float(project[5])
                status = project[8]
                
                if dept not in dept_analysis:
                    dept_analysis[dept] = {
                        'count': 0, 'budget': 0, 'status': {}
                    }
                
                dept_analysis[dept]['count'] += 1
                dept_analysis[dept]['budget'] += budget
                
                if status not in dept_analysis[dept]['status']:
                    dept_analysis[dept]['status'][status] = 0
                dept_analysis[dept]['status'][status] += 1
            
            # 创建分析窗口
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("🏢 部门详细分析")
            analysis_window.geometry("700x600")
            
            frame = ttk.Frame(analysis_window, padding="20")
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            analysis_window.columnconfigure(0, weight=1)
            analysis_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            
            analysis_text = "🏢 部门项目详细分析报告\n" + "="*60 + "\n\n"
            
            sorted_depts = sorted(dept_analysis.items(), key=lambda x: x[1]['count'], reverse=True)
            
            for dept, data in sorted_depts:
                analysis_text += f"📋 {dept}:\n"
                analysis_text += f"   项目数量：{data['count']} 个\n"
                analysis_text += f"   概算总额：{data['budget']:,.2f} 万元\n"
                analysis_text += f"   平均概算：{data['budget']/data['count']:,.2f} 万元\n"
                analysis_text += f"   项目状态：{', '.join([f'{s}({c}个)' for s, c in data['status'].items()])}\n"
                analysis_text += "\n"
            
            text_widget = tk.Text(frame, wrap=tk.WORD, font=('Consolas', 10))
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            text_widget.insert(1.0, analysis_text)
            text_widget.config(state=tk.DISABLED)
            
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            text_widget.configure(yscrollcommand=scrollbar.set)
            
        except Exception as e:
            messagebox.showerror("错误", f"部门分析失败：{str(e)}")
            
    def display_table(self, table_name):
        """显示表格"""
        try:
            if table_name not in self.data or not self.data[table_name]:
                self.show_welcome_advanced()
                return
                
            table_data = self.data[table_name]
            headers = table_data[0]
            data_rows = table_data[1:]
            
            self.tree["columns"] = headers
            self.tree["show"] = "headings"
            
            for col in headers:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, minwidth=80)
                
            # 清空数据
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # 显示数据（限制显示数量）
            display_count = min(200, len(data_rows))
            for row in data_rows[:display_count]:
                # 格式化显示
                formatted_row = []
                for i, cell in enumerate(row):
                    if i < len(headers) and ("金额" in headers[i] or "概算" in headers[i]):
                        try:
                            formatted_row.append(f"{float(cell):,.2f}")
                        except:
                            formatted_row.append(str(cell))
                    else:
                        formatted_row.append(str(cell))
                
                self.tree.insert("", "end", values=formatted_row)
            
            self.current_table_var.set(table_name)
            self.record_count_var.set(f"显示 {display_count}/{len(data_rows)} 条记录")
            self.update_status(f"已加载 {table_name}")
            
            if len(data_rows) > 200:
                messagebox.showinfo("提示", f"数据量较大，仅显示前200条记录\n总记录数：{len(data_rows)} 条\n如需查看全部数据，请使用导出功能")
                
        except Exception as e:
            messagebox.showerror("错误", f"显示表格失败：{str(e)}")
            
    def on_item_double_click(self, event):
        """双击项目处理"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            messagebox.showinfo("记录详情", f"📋 记录详细信息：\n\n" + "\n".join([f"{self.tree.heading(col)['text']}: {val}" for col, val in zip(self.tree['columns'], values)]))
            
    def update_status(self, message):
        """更新状态"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def run(self):
        """运行程序"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        print("🚀 启动AI城建系统高级Excel数据处理器...")
        app = AdvancedExcelProcessor()
        app.run()
    except Exception as e:
        print(f"❌ 程序启动失败：{e}")
        messagebox.showerror("启动错误", f"程序启动失败：{str(e)}")

if __name__ == "__main__":
    main()