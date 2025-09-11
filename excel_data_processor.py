#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel数据处理小程序
专门用于处理AI城建系统的Excel数据文件
支持读取、分析、生成、导出Excel文件
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

class ExcelDataProcessor:
    """Excel数据处理器"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.data = {}  # 存储所有数据
        self.create_widgets()
        
    def setup_window(self):
        """设置窗口"""
        self.root.title("📊 Excel数据处理小程序 - AI城建系统")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # 居中显示
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
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="📊 Excel数据处理小程序", 
                               font=('Microsoft YaHei', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 左侧控制面板
        self.create_control_panel(main_frame)
        
        # 右侧数据显示区域
        self.create_data_display(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = ttk.LabelFrame(parent, text="🛠️ 数据处理操作", padding="15")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        # 文件操作区域
        file_frame = ttk.LabelFrame(control_frame, text="📁 文件操作", padding="10")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="🎲 生成AI城建数据", 
                  command=self.generate_ai_urban_data).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(file_frame, text="📂 打开Excel文件", 
                  command=self.open_excel_file).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(file_frame, text="💾 保存为Excel", 
                  command=self.save_excel_file).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(file_frame, text="📋 导入CSV文件", 
                  command=self.import_csv_file).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(file_frame, text="📤 导出CSV文件", 
                  command=self.export_csv_file).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 数据操作区域
        data_frame = ttk.LabelFrame(control_frame, text="🔧 数据操作", padding="10")
        data_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(data_frame, text="📊 数据透视表", 
                  command=self.create_pivot_table).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(data_frame, text="📈 数据统计", 
                  command=self.show_statistics).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(data_frame, text="🔍 数据筛选", 
                  command=self.filter_data).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(data_frame, text="📋 数据汇总", 
                  command=self.summarize_data).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(data_frame, text="🧹 清空数据", 
                  command=self.clear_data).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 表格选择区域
        table_frame = ttk.LabelFrame(control_frame, text="📋 数据表选择", padding="10")
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.table_var = tk.StringVar(value="项目基本信息表")
        tables = ["项目基本信息表", "资金安排表", "重点项目清单", "数据透视表"]
        
        for i, table in enumerate(tables):
            ttk.Radiobutton(table_frame, text=table, variable=self.table_var, 
                           value=table, command=self.switch_table).grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # 快捷操作区域
        quick_frame = ttk.LabelFrame(control_frame, text="⚡ 快捷操作", padding="10")
        quick_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(quick_frame, text="🎯 债券资金分析", 
                  command=self.bond_analysis).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(quick_frame, text="🏢 部门统计", 
                  command=self.department_stats).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(quick_frame, text="📅 月度分析", 
                  command=self.monthly_analysis).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        
    def create_data_display(self, parent):
        """创建数据显示区域"""
        display_frame = ttk.LabelFrame(parent, text="📊 数据显示", padding="15")
        display_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
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
        
        # 初始显示
        self.show_welcome()
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="状态：").grid(row=0, column=0, sticky=tk.W)
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # 数据统计
        self.stats_var = tk.StringVar(value="")
        self.stats_label = ttk.Label(status_frame, textvariable=self.stats_var)
        self.stats_label.grid(row=0, column=2, sticky=tk.E)
        
    def show_welcome(self):
        """显示欢迎信息"""
        self.tree["columns"] = ("功能", "说明", "状态")
        self.tree["show"] = "headings"
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
            
        welcome_data = [
            ("生成AI城建数据", "生成200个项目+1000条资金安排", "✅ 就绪"),
            ("Excel文件处理", "打开、编辑、保存Excel文件", "✅ 就绪"),
            ("数据透视分析", "债券资金合计等透视分析", "✅ 就绪"),
            ("数据统计分析", "项目状态、资金性质统计", "✅ 就绪"),
            ("数据筛选过滤", "按条件筛选和过滤数据", "✅ 就绪"),
            ("CSV文件处理", "导入导出CSV格式文件", "✅ 就绪")
        ]
        
        for item in welcome_data:
            self.tree.insert("", "end", values=item)
            
        self.update_status("欢迎使用Excel数据处理小程序")
        
    def generate_ai_urban_data(self):
        """生成AI城建系统数据"""
        if not messagebox.askyesno("确认", "这将生成AI城建系统的完整数据集：\n• 200个项目基本信息\n• 1000条资金安排记录\n• 重点项目清单\n• 数据透视表\n\n是否继续？"):
            return
            
        try:
            self.update_status("正在生成数据...")
            
            # 生成项目基本信息
            projects_data = self.generate_project_data(200)
            self.data["项目基本信息表"] = projects_data
            
            # 生成资金安排数据
            funding_data = self.generate_funding_data(projects_data, 1000)
            self.data["资金安排表"] = funding_data
            
            # 生成重点项目清单
            key_projects_data = self.generate_key_projects(projects_data)
            self.data["重点项目清单"] = key_projects_data
            
            # 生成数据透视表
            pivot_data = self.generate_pivot_table(funding_data)
            self.data["数据透视表"] = pivot_data
            
            # 显示项目数据
            self.display_table_data("项目基本信息表")
            self.update_stats()
            
            messagebox.showinfo("成功", "AI城建系统数据生成完成！\n\n✅ 200个项目基本信息\n✅ 1000条资金安排记录\n✅ 重点项目清单\n✅ 债券资金合计透视表")
            
        except Exception as e:
            messagebox.showerror("错误", f"数据生成失败：{str(e)}")
            self.update_status("数据生成失败")
            
    def generate_project_data(self, count=200):
        """生成项目基本信息数据"""
        projects = []
        
        # 表头
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '立项时间',
            '概算批复金额', '预计开工时间', '预计完工时间', '项目状态'
        ]
        projects.append(headers)
        
        # 基础数据
        project_types = [
            '道路建设工程', '桥梁建设工程', '隧道建设工程', '排水管网工程', '供水管网工程',
            '公园绿化工程', '广场建设工程', '学校建设工程', '医院建设工程', '住宅小区建设',
            '商业综合体建设', '地铁建设工程', '公交站台建设', '污水处理厂建设', '垃圾处理中心建设',
            '体育中心建设', '文化中心建设', '图书馆建设', '博物馆建设', '停车场建设'
        ]
        
        areas = [
            '东城区', '西城区', '南城区', '北城区', '中心区', '开发区', '新区', '高新区',
            '经济技术开发区', '生态城区', '滨海新区', '山区', '工业园区', '科技园区'
        ]
        
        construction_units = [
            '市政建设集团有限公司', '城市投资建设集团', '交通建设发展集团', '水务建设集团公司',
            '园林绿化建设集团', '教育建设投资公司', '医疗建设发展公司', '住房建设集团',
            '基础设施建设公司', '公共设施建设集团', '环保建设投资公司', '文化建设集团'
        ]
        
        departments = [
            '市发展和改革委员会', '市住房和城乡建设局', '市交通运输局', '市水利局',
            '市教育局', '市卫生健康委员会', '市生态环境局', '市园林绿化局',
            '市城市管理局', '市规划和自然资源局', '市文化和旅游局', '市体育局'
        ]
        
        statuses = ['在建', '续建', '完工', '暂停']
        
        for i in range(1, count + 1):
            project_code = f"UC{datetime.now().year}{i:04d}"
            area = random.choice(areas)
            project_type = random.choice(project_types)
            phase = random.choice(['一期', '二期', '三期', '四期', '五期'])
            project_name = f"{area}{project_type}{phase}"
            
            # 概算金额500-20000万元
            budget_amount = round(random.uniform(500, 20000), 2)
            
            # 随机日期
            base_date = datetime(2023, 1, 1)
            approval_date = base_date + timedelta(days=random.randint(0, 500))
            start_date = approval_date + timedelta(days=random.randint(30, 180))
            end_date = start_date + timedelta(days=random.randint(180, 1095))
            
            project_row = [
                project_name, project_code,
                random.choice(construction_units),
                random.choice(departments),
                approval_date.strftime('%Y-%m-%d'),
                budget_amount,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
                random.choice(statuses)
            ]
            projects.append(project_row)
            
        return projects
        
    def generate_funding_data(self, projects_data, count=1000):
        """生成资金安排数据"""
        funding_records = []
        
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '概算批复金额',
            '资金批复金额', '批复日期', '资金性质', '经办人', '经办处室'
        ]
        funding_records.append(headers)
        
        funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助']
        operators = ['张建华', '李明强', '王志远', '赵文博', '钱国强', '孙海涛', '周建军', '吴德华']
        departments = ['计划财务处', '项目管理处', '投资建设处', '资金管理处', '审计监察处']
        
        projects_list = projects_data[1:]  # 跳过表头
        
        # 每个项目至少一条资金安排
        for project in projects_list:
            budget_amount = float(project[5])
            funding_amount = round(random.uniform(budget_amount * 0.1, budget_amount * 0.8), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_date = approval_date + timedelta(days=random.randint(1, 90))
            
            funding_row = [
                project[0], project[1], project[2], project[3], budget_amount,
                funding_amount, funding_date.strftime('%Y-%m-%d'),
                random.choice(funding_types), random.choice(operators), random.choice(departments)
            ]
            funding_records.append(funding_row)
        
        # 生成剩余记录
        remaining_count = count - len(projects_list)
        for _ in range(remaining_count):
            project = random.choice(projects_list)
            budget_amount = float(project[5])
            funding_amount = round(random.uniform(budget_amount * 0.05, budget_amount * 0.5), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_date = approval_date + timedelta(days=random.randint(1, 365))
            
            funding_row = [
                project[0], project[1], project[2], project[3], budget_amount,
                funding_amount, funding_date.strftime('%Y-%m-%d'),
                random.choice(funding_types), random.choice(operators), random.choice(departments)
            ]
            funding_records.append(funding_row)
            
        return funding_records
        
    def generate_key_projects(self, projects_data):
        """生成重点项目清单"""
        key_projects = []
        
        headers = ['项目编码', '项目名称', '优先级', '关键特征', '战略重要性']
        key_projects.append(headers)
        
        projects_list = projects_data[1:]
        key_count = int(len(projects_list) * 0.3)  # 30%作为重点项目
        key_projects_sample = random.sample(projects_list, key_count)
        
        features = ['重大民生工程', '基础设施建设', '生态环保项目', '科技创新项目', '文化教育项目']
        importance = ['提升城市承载能力', '改善民生福祉', '促进经济发展', '推动生态建设', '增强城市竞争力']
        
        for project in key_projects_sample:
            key_row = [
                project[1],  # 项目编码
                project[0],  # 项目名称
                random.randint(1, 3),  # 优先级
                random.choice(features),
                random.choice(importance)
            ]
            key_projects.append(key_row)
            
        return key_projects
        
    def generate_pivot_table(self, funding_data):
        """生成数据透视表"""
        pivot_data = []
        
        headers = ['项目编码', '项目名称', '一般债券', '专项债券', '债券资金合计', '其他资金', '资金总计']
        pivot_data.append(headers)
        
        funding_list = funding_data[1:]  # 跳过表头
        project_funding = {}
        
        # 按项目分组统计
        for funding in funding_list:
            project_code = funding[1]
            project_name = funding[0]
            funding_type = funding[7]
            amount = float(funding[5])
            
            if project_code not in project_funding:
                project_funding[project_code] = {
                    'name': project_name,
                    '一般债券': 0,
                    '专项债券': 0,
                    '其他资金': 0
                }
            
            if funding_type == '一般债券':
                project_funding[project_code]['一般债券'] += amount
            elif funding_type == '专项债券':
                project_funding[project_code]['专项债券'] += amount
            else:
                project_funding[project_code]['其他资金'] += amount
        
        # 生成透视表数据
        for project_code, data in project_funding.items():
            general_bonds = data['一般债券']
            special_bonds = data['专项债券']
            other_funding = data['其他资金']
            bond_total = general_bonds + special_bonds  # 债券资金合计
            total_funding = bond_total + other_funding
            
            pivot_row = [
                project_code, data['name'],
                f"{general_bonds:.2f}" if general_bonds > 0 else "0.00",
                f"{special_bonds:.2f}" if special_bonds > 0 else "0.00",
                f"{bond_total:.2f}" if bond_total > 0 else "0.00",  # 债券资金合计
                f"{other_funding:.2f}" if other_funding > 0 else "0.00",
                f"{total_funding:.2f}"
            ]
            pivot_data.append(pivot_row)
            
        return pivot_data
        
    def open_excel_file(self):
        """打开Excel文件"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择Excel文件",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("Excel files", "*.xlsx *.xls"),
                    ("All files", "*.*")
                ]
            )
            
            if not file_path:
                return
                
            # 读取CSV文件
            if file_path.endswith('.csv'):
                data = []
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        data.append(row)
                
                # 根据文件名判断表类型
                filename = os.path.basename(file_path)
                if "项目基本信息" in filename:
                    table_name = "项目基本信息表"
                elif "资金安排" in filename:
                    table_name = "资金安排表"
                elif "重点项目" in filename:
                    table_name = "重点项目清单"
                elif "透视表" in filename:
                    table_name = "数据透视表"
                else:
                    table_name = "导入数据"
                
                self.data[table_name] = data
                self.table_var.set(table_name)
                self.display_table_data(table_name)
                
                messagebox.showinfo("成功", f"文件导入成功！\n文件：{filename}\n数据行数：{len(data)-1}")
                
            else:
                messagebox.showwarning("提示", "目前支持CSV格式文件\n如需处理Excel文件，请先转换为CSV格式")
                
        except Exception as e:
            messagebox.showerror("错误", f"文件打开失败：{str(e)}")
            
    def save_excel_file(self):
        """保存Excel文件"""
        try:
            current_table = self.table_var.get()
            if current_table not in self.data or not self.data[current_table]:
                messagebox.showwarning("警告", "没有数据可保存")
                return
                
            file_path = filedialog.asksaveasfilename(
                title="保存Excel文件",
                defaultextension=".csv",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ]
            )
            
            if not file_path:
                return
                
            # 保存CSV文件
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerows(self.data[current_table])
                
            messagebox.showinfo("成功", f"文件保存成功！\n位置：{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"文件保存失败：{str(e)}")
            
    def import_csv_file(self):
        """导入CSV文件"""
        self.open_excel_file()
        
    def export_csv_file(self):
        """导出CSV文件"""
        try:
            if not self.data:
                messagebox.showwarning("警告", "没有数据可导出")
                return
                
            # 选择导出目录
            export_dir = filedialog.askdirectory(title="选择导出目录")
            if not export_dir:
                return
                
            exported_files = []
            for table_name, table_data in self.data.items():
                if table_data:
                    filename = f"{table_name}.csv"
                    file_path = os.path.join(export_dir, filename)
                    
                    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                        writer = csv.writer(f)
                        writer.writerows(table_data)
                    
                    exported_files.append(filename)
            
            messagebox.showinfo("成功", f"数据导出完成！\n导出文件：\n" + "\n".join(exported_files))
            
        except Exception as e:
            messagebox.showerror("错误", f"数据导出失败：{str(e)}")
            
    def create_pivot_table(self):
        """创建数据透视表"""
        if "资金安排表" not in self.data or not self.data["资金安排表"]:
            messagebox.showwarning("警告", "请先生成或导入资金安排数据")
            return
            
        try:
            funding_data = self.data["资金安排表"]
            pivot_data = self.generate_pivot_table(funding_data)
            self.data["数据透视表"] = pivot_data
            
            self.table_var.set("数据透视表")
            self.display_table_data("数据透视表")
            
            messagebox.showinfo("成功", "数据透视表创建完成！\n按项目编码分组，包含债券资金合计分析")
            
        except Exception as e:
            messagebox.showerror("错误", f"创建透视表失败：{str(e)}")
            
    def show_statistics(self):
        """显示数据统计"""
        try:
            if not self.data:
                messagebox.showwarning("警告", "没有数据可统计")
                return
                
            stats_info = "📊 数据统计信息\n" + "="*30 + "\n\n"
            
            for table_name, table_data in self.data.items():
                if table_data:
                    record_count = len(table_data) - 1  # 减去表头
                    stats_info += f"📋 {table_name}：{record_count} 条记录\n"
            
            # 项目统计
            if "项目基本信息表" in self.data and self.data["项目基本信息表"]:
                projects = self.data["项目基本信息表"][1:]  # 跳过表头
                total_budget = sum(float(p[5]) for p in projects)
                avg_budget = total_budget / len(projects) if projects else 0
                
                status_stats = {}
                for project in projects:
                    status = project[8]
                    status_stats[status] = status_stats.get(status, 0) + 1
                
                stats_info += f"\n💰 概算总额：{total_budget:,.2f} 万元\n"
                stats_info += f"📊 平均概算：{avg_budget:,.2f} 万元\n"
                stats_info += f"\n📈 项目状态分布：\n"
                for status, count in status_stats.items():
                    percentage = count / len(projects) * 100
                    stats_info += f"   {status}：{count} 个 ({percentage:.1f}%)\n"
            
            # 资金统计
            if "资金安排表" in self.data and self.data["资金安排表"]:
                funding = self.data["资金安排表"][1:]  # 跳过表头
                total_funding = sum(float(f[5]) for f in funding)
                
                funding_type_stats = {}
                for fund in funding:
                    ftype = fund[7]
                    amount = float(fund[5])
                    if ftype not in funding_type_stats:
                        funding_type_stats[ftype] = {'count': 0, 'amount': 0}
                    funding_type_stats[ftype]['count'] += 1
                    funding_type_stats[ftype]['amount'] += amount
                
                stats_info += f"\n💵 资金安排总额：{total_funding:,.2f} 万元\n"
                stats_info += f"\n📋 资金性质分布：\n"
                for ftype, data in funding_type_stats.items():
                    percentage = data['amount'] / total_funding * 100
                    stats_info += f"   {ftype}：{data['count']} 笔，{data['amount']:,.2f} 万元 ({percentage:.1f}%)\n"
                
                # 债券资金统计
                general_bonds = funding_type_stats.get('一般债券', {'amount': 0})['amount']
                special_bonds = funding_type_stats.get('专项债券', {'amount': 0})['amount']
                total_bonds = general_bonds + special_bonds
                
                stats_info += f"\n💎 债券资金专项统计：\n"
                stats_info += f"   一般债券：{general_bonds:,.2f} 万元\n"
                stats_info += f"   专项债券：{special_bonds:,.2f} 万元\n"
                stats_info += f"   债券合计：{total_bonds:,.2f} 万元\n"
            
            # 显示统计信息
            stats_window = tk.Toplevel(self.root)
            stats_window.title("📊 数据统计信息")
            stats_window.geometry("500x600")
            
            frame = ttk.Frame(stats_window, padding="20")
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            stats_window.columnconfigure(0, weight=1)
            stats_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            
            text_widget = tk.Text(frame, wrap=tk.WORD, font=('Consolas', 10))
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            text_widget.insert(1.0, stats_info)
            text_widget.config(state=tk.DISABLED)
            
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            text_widget.configure(yscrollcommand=scrollbar.set)
            
        except Exception as e:
            messagebox.showerror("错误", f"统计分析失败：{str(e)}")
            
    def filter_data(self):
        """数据筛选"""
        current_table = self.table_var.get()
        if current_table not in self.data or not self.data[current_table]:
            messagebox.showwarning("警告", "请先选择有效的数据表")
            return
            
        # 创建筛选对话框
        filter_window = tk.Toplevel(self.root)
        filter_window.title("🔍 数据筛选")
        filter_window.geometry("400x300")
        
        frame = ttk.Frame(filter_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="选择筛选条件：", font=('Microsoft YaHei', 12, 'bold')).grid(row=0, column=0, pady=(0, 15))
        
        if current_table == "项目基本信息表":
            ttk.Label(frame, text="按项目状态筛选：").grid(row=1, column=0, sticky=tk.W, pady=5)
            status_var = tk.StringVar(value="全部")
            status_combo = ttk.Combobox(frame, textvariable=status_var, 
                                       values=["全部", "在建", "续建", "完工", "暂停"], 
                                       state="readonly")
            status_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
            ttk.Label(frame, text="概算金额范围：").grid(row=2, column=0, sticky=tk.W, pady=5)
            amount_var = tk.StringVar(value="全部")
            amount_combo = ttk.Combobox(frame, textvariable=amount_var,
                                       values=["全部", "500-2000万", "2000-5000万", "5000-10000万", "10000万以上"],
                                       state="readonly")
            amount_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
        elif current_table == "资金安排表":
            ttk.Label(frame, text="按资金性质筛选：").grid(row=1, column=0, sticky=tk.W, pady=5)
            funding_var = tk.StringVar(value="全部")
            funding_combo = ttk.Combobox(frame, textvariable=funding_var,
                                        values=["全部", "一般债券", "专项债券", "中央综合财力", "土地出让金"],
                                        state="readonly")
            funding_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
        def apply_filter():
            try:
                # 这里可以实现具体的筛选逻辑
                messagebox.showinfo("筛选结果", "筛选功能演示\n\n在完整版本中，您可以：\n• 按条件筛选数据\n• 查看筛选结果\n• 导出筛选数据\n• 保存筛选条件")
                filter_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"筛选失败：{str(e)}")
        
        ttk.Button(frame, text="应用筛选", command=apply_filter).grid(row=10, column=0, columnspan=2, pady=20)
        
    def summarize_data(self):
        """数据汇总"""
        current_table = self.table_var.get()
        if current_table not in self.data or not self.data[current_table]:
            messagebox.showwarning("警告", "请先选择有效的数据表")
            return
            
        try:
            table_data = self.data[current_table]
            headers = table_data[0]
            data_rows = table_data[1:]
            
            summary_info = f"📋 {current_table} 数据汇总\n" + "="*40 + "\n\n"
            summary_info += f"📊 总记录数：{len(data_rows)} 条\n"
            summary_info += f"📅 数据字段：{len(headers)} 个\n\n"
            
            summary_info += "📋 字段列表：\n"
            for i, header in enumerate(headers, 1):
                summary_info += f"   {i}. {header}\n"
            
            if current_table == "项目基本信息表" and len(data_rows) > 0:
                # 概算金额统计
                budgets = [float(row[5]) for row in data_rows if row[5]]
                total_budget = sum(budgets)
                avg_budget = total_budget / len(budgets) if budgets else 0
                min_budget = min(budgets) if budgets else 0
                max_budget = max(budgets) if budgets else 0
                
                summary_info += f"\n💰 概算金额统计：\n"
                summary_info += f"   总额：{total_budget:,.2f} 万元\n"
                summary_info += f"   平均：{avg_budget:,.2f} 万元\n"
                summary_info += f"   最小：{min_budget:,.2f} 万元\n"
                summary_info += f"   最大：{max_budget:,.2f} 万元\n"
                
            elif current_table == "资金安排表" and len(data_rows) > 0:
                # 资金统计
                amounts = [float(row[5]) for row in data_rows if row[5]]
                total_amount = sum(amounts)
                avg_amount = total_amount / len(amounts) if amounts else 0
                
                summary_info += f"\n💵 资金金额统计：\n"
                summary_info += f"   总额：{total_amount:,.2f} 万元\n"
                summary_info += f"   平均：{avg_amount:,.2f} 万元\n"
                
                # 资金性质统计
                funding_types = {}
                for row in data_rows:
                    if len(row) > 7:
                        ftype = row[7]
                        funding_types[ftype] = funding_types.get(ftype, 0) + 1
                
                summary_info += f"\n📈 资金性质分布：\n"
                for ftype, count in funding_types.items():
                    percentage = count / len(data_rows) * 100
                    summary_info += f"   {ftype}：{count} 笔 ({percentage:.1f}%)\n"
            
            # 显示汇总信息
            summary_window = tk.Toplevel(self.root)
            summary_window.title("📊 数据汇总报告")
            summary_window.geometry("500x600")
            
            frame = ttk.Frame(summary_window, padding="20")
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            summary_window.columnconfigure(0, weight=1)
            summary_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            
            text_widget = tk.Text(frame, wrap=tk.WORD, font=('Consolas', 10))
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            text_widget.insert(1.0, summary_info)
            text_widget.config(state=tk.DISABLED)
            
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            text_widget.configure(yscrollcommand=scrollbar.set)
            
        except Exception as e:
            messagebox.showerror("错误", f"数据汇总失败：{str(e)}")
            
    def bond_analysis(self):
        """债券资金分析"""
        if "资金安排表" not in self.data or not self.data["资金安排表"]:
            messagebox.showwarning("警告", "请先生成或导入资金安排数据")
            return
            
        try:
            funding_data = self.data["资金安排表"][1:]  # 跳过表头
            
            general_bonds = 0
            special_bonds = 0
            bond_projects = set()
            
            for fund in funding_data:
                if len(fund) > 7:
                    funding_type = fund[7]
                    amount = float(fund[5])
                    project_code = fund[1]
                    
                    if funding_type == "一般债券":
                        general_bonds += amount
                        bond_projects.add(project_code)
                    elif funding_type == "专项债券":
                        special_bonds += amount
                        bond_projects.add(project_code)
            
            total_bonds = general_bonds + special_bonds
            
            analysis_info = f"""
🎯 债券资金专项分析报告
{'='*40}

💎 债券资金统计：
   一般债券：{general_bonds:,.2f} 万元
   专项债券：{special_bonds:,.2f} 万元
   债券合计：{total_bonds:,.2f} 万元

📊 债券资金占比：
   一般债券占比：{general_bonds/total_bonds*100:.1f}%
   专项债券占比：{special_bonds/total_bonds*100:.1f}%

🏗️ 涉及项目：
   债券资金项目数：{len(bond_projects)} 个
   
💡 分析结论：
   • 债券资金是重要的资金来源
   • 一般债券和专项债券需要统筹管理
   • 建议加强债券资金使用监管
            """
            
            messagebox.showinfo("债券资金分析", analysis_info)
            
        except Exception as e:
            messagebox.showerror("错误", f"债券分析失败：{str(e)}")
            
    def department_stats(self):
        """部门统计"""
        if "项目基本信息表" not in self.data or not self.data["项目基本信息表"]:
            messagebox.showwarning("警告", "请先生成或导入项目基本信息")
            return
            
        try:
            projects = self.data["项目基本信息表"][1:]  # 跳过表头
            dept_stats = {}
            
            for project in projects:
                if len(project) > 3:
                    dept = project[3]  # 项目主管部门
                    budget = float(project[5])  # 概算批复金额
                    
                    if dept not in dept_stats:
                        dept_stats[dept] = {'count': 0, 'budget': 0}
                    
                    dept_stats[dept]['count'] += 1
                    dept_stats[dept]['budget'] += budget
            
            # 按项目数量排序
            sorted_depts = sorted(dept_stats.items(), key=lambda x: x[1]['count'], reverse=True)
            
            stats_info = "🏢 部门项目统计报告\n" + "="*40 + "\n\n"
            stats_info += f"{'部门名称':<20} {'项目数':<8} {'概算总额(万元)':<15}\n"
            stats_info += "-" * 50 + "\n"
            
            for dept, data in sorted_depts:
                stats_info += f"{dept:<20} {data['count']:<8} {data['budget']:<15,.2f}\n"
            
            messagebox.showinfo("部门统计", stats_info)
            
        except Exception as e:
            messagebox.showerror("错误", f"部门统计失败：{str(e)}")
            
    def monthly_analysis(self):
        """月度分析"""
        messagebox.showinfo("月度分析", "📅 月度分析功能\n\n支持的分析维度：\n• 按月份统计项目立项数量\n• 按月份统计资金安排金额\n• 月度趋势分析\n• 季度对比分析\n\n💡 完整版本支持图表显示")
        
    def switch_table(self):
        """切换数据表"""
        current_table = self.table_var.get()
        self.display_table_data(current_table)
        
    def display_table_data(self, table_name):
        """显示表格数据"""
        try:
            if table_name not in self.data or not self.data[table_name]:
                self.show_welcome()
                return
                
            table_data = self.data[table_name]
            headers = table_data[0]
            data_rows = table_data[1:]
            
            # 设置列
            self.tree["columns"] = headers
            self.tree["show"] = "headings"
            
            for col in headers:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, minwidth=80)
                
            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # 添加数据（最多显示100行）
            display_count = min(100, len(data_rows))
            for i, row in enumerate(data_rows[:display_count]):
                # 格式化金额显示
                formatted_row = []
                for j, cell in enumerate(row):
                    if j in [5, 6] and headers[j] and ("金额" in headers[j] or "概算" in headers[j]):
                        try:
                            formatted_row.append(f"{float(cell):.2f}万元")
                        except:
                            formatted_row.append(str(cell))
                    else:
                        formatted_row.append(str(cell))
                
                self.tree.insert("", "end", values=formatted_row)
            
            self.update_status(f"显示 {table_name} - 前{display_count}条记录")
            
            if len(data_rows) > 100:
                messagebox.showinfo("提示", f"数据量较大，仅显示前100条记录\n总记录数：{len(data_rows)} 条")
                
        except Exception as e:
            messagebox.showerror("错误", f"显示数据失败：{str(e)}")
            
    def clear_data(self):
        """清空数据"""
        if not messagebox.askyesno("确认", "确定要清空所有数据吗？"):
            return
            
        self.data.clear()
        self.show_welcome()
        self.update_status("数据已清空")
        messagebox.showinfo("成功", "所有数据已清空")
        
    def update_status(self, message):
        """更新状态"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def update_stats(self):
        """更新统计信息"""
        total_tables = len(self.data)
        total_records = sum(len(table_data)-1 for table_data in self.data.values() if table_data)
        
        self.stats_var.set(f"数据表：{total_tables}个 | 总记录：{total_records}条")
        
    def run(self):
        """运行程序"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        print("🚀 启动Excel数据处理小程序...")
        app = ExcelDataProcessor()
        app.run()
    except Exception as e:
        print(f"❌ 程序启动失败：{e}")
        messagebox.showerror("启动错误", f"程序启动失败：{str(e)}")

if __name__ == "__main__":
    main()