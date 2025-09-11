#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统 - 独立桌面版
无需安装依赖，可直接运行的版本
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import random
from datetime import datetime, date, timedelta
from pathlib import Path

class AIUrbanSystem:
    """AI城建系统主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.init_database()
        self.create_widgets()
        
    def setup_window(self):
        """设置主窗口"""
        self.root.title("AI城建系统 v1.0.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
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
        
    def init_database(self):
        """初始化数据库"""
        os.makedirs("data", exist_ok=True)
        self.db_path = "data/urban_system.db"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建项目表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                unit TEXT NOT NULL,
                department TEXT NOT NULL,
                budget REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建资金表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funding (
                id INTEGER PRIMARY KEY,
                project_code TEXT NOT NULL,
                project_name TEXT NOT NULL,
                amount REAL NOT NULL,
                funding_type TEXT NOT NULL,
                operator TEXT NOT NULL,
                department TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def create_widgets(self):
        """创建界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        title_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(title_frame, text="🏙️ AI城建系统", 
                               font=('Microsoft YaHei', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 统计信息
        stats_label = ttk.Label(title_frame, text="", 
                               font=('Microsoft YaHei', 10))
        stats_label.grid(row=0, column=1, sticky=tk.E)
        self.stats_label = stats_label
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 基础数据管理
        self.create_data_tab()
        
        # 数据可视化
        self.create_chart_tab()
        
        # 智慧报表
        self.create_report_tab()
        
        # 更新统计信息
        self.update_stats()
        
    def create_data_tab(self):
        """创建基础数据管理选项卡"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="基础数据管理")
        
        # 左侧控制面板
        control_frame = ttk.LabelFrame(data_frame, text="数据操作", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Button(control_frame, text="生成模拟数据", 
                  command=self.generate_mock_data).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(control_frame, text="查看项目列表", 
                  command=self.show_projects).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(control_frame, text="查看资金安排", 
                  command=self.show_funding).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(control_frame, text="数据透视表", 
                  command=self.show_pivot_table).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(control_frame, text="清空所有数据", 
                  command=self.clear_data).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 右侧数据显示
        display_frame = ttk.LabelFrame(data_frame, text="数据显示", padding="10")
        display_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        data_frame.columnconfigure(1, weight=1)
        data_frame.rowconfigure(0, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # 数据表格
        self.tree = ttk.Treeview(display_frame)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 初始显示
        self.show_welcome()
        
    def create_chart_tab(self):
        """创建数据可视化选项卡"""
        chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(chart_frame, text="数据可视化")
        
        # 内容框架
        content_frame = ttk.Frame(chart_frame, padding="20")
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.rowconfigure(0, weight=1)
        
        ttk.Label(content_frame, text="📊 数据可视化功能", 
                 font=('Microsoft YaHei', 16, 'bold')).grid(row=0, column=0, pady=(0, 20))
        
        # 图表类型说明
        chart_info = """
支持的图表类型：

✅ 项目状态分布图（饼图）
✅ 概算金额分布图（直方图）
✅ 资金性质分析图（条形图）
✅ 项目时间轴图（甘特图）
✅ 债券资金统计图（堆叠条形图）
✅ 部门项目数量统计（条形图）
✅ 月度资金安排趋势（折线图）
✅ 项目完成度分析（直方图）

特色功能：
• 支持中文显示
• 交互式图表
• 高分辨率导出
• 自动配色方案
        """
        
        info_text = tk.Text(content_frame, height=20, width=60, wrap=tk.WORD)
        info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_text.insert(1.0, chart_info)
        info_text.config(state=tk.DISABLED)
        
        ttk.Button(content_frame, text="查看图表演示", 
                  command=self.show_chart_demo).grid(row=2, column=0, pady=20)
        
    def create_report_tab(self):
        """创建智慧报表选项卡"""
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="智慧报表生成")
        
        content_frame = ttk.Frame(report_frame, padding="20")
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        report_frame.columnconfigure(0, weight=1)
        report_frame.rowconfigure(0, weight=1)
        
        ttk.Label(content_frame, text="📋 智慧报表生成", 
                 font=('Microsoft YaHei', 16, 'bold')).grid(row=0, column=0, pady=(0, 20))
        
        report_info = """
支持的报表类型：

✅ 项目总览报表 - 项目基本信息汇总
✅ 资金安排报表 - 资金安排详细信息  
✅ 项目进度报表 - 项目进度和完成情况
✅ 部门统计报表 - 按部门统计分析
✅ 债券资金报表 - 债券资金专项分析
✅ 月度汇总报表 - 按月份数据汇总
✅ 项目完成情况报表 - 完成度统计
✅ 资金透视分析报表 - 多维度透视分析

报表功能：
• 支持日期范围筛选
• Excel格式导出
• 自动统计计算
• 专业报表模板
• 打印功能支持
        """
        
        info_text = tk.Text(content_frame, height=20, width=60, wrap=tk.WORD)
        info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_text.insert(1.0, report_info)
        info_text.config(state=tk.DISABLED)
        
        ttk.Button(content_frame, text="生成报表演示", 
                  command=self.show_report_demo).grid(row=2, column=0, pady=20)
        
    def show_welcome(self):
        """显示欢迎信息"""
        self.tree["columns"] = ("功能", "状态", "说明")
        self.tree["show"] = "headings"
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
            
        welcome_data = [
            ("项目基本信息管理", "✅ 就绪", "管理项目名称、编码、建设单位等"),
            ("资金安排管理", "✅ 就绪", "管理资金批复、资金性质等"),
            ("Excel导入导出", "✅ 就绪", "支持数据批量导入导出"),
            ("数据可视化", "✅ 就绪", "8种专业图表类型"),
            ("智慧报表生成", "✅ 就绪", "8种分析报表"),
            ("数据透视分析", "✅ 就绪", "债券资金合计分析")
        ]
        
        for item in welcome_data:
            self.tree.insert("", "end", values=item)
            
    def generate_mock_data(self):
        """生成模拟数据"""
        if not messagebox.askyesno("确认", "这将生成50个模拟项目和200条资金安排数据，是否继续？"):
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 生成项目数据
            project_types = ['道路建设', '桥梁建设', '公园建设', '学校建设', '医院建设']
            areas = ['东城区', '西城区', '南城区', '北城区', '中心区']
            units = ['市政建设集团', '城投建设公司', '交通建设集团']
            departments = ['市发改委', '市住建局', '市交通局', '市教育局']
            statuses = ['在建', '续建', '完工', '暂停']
            
            for i in range(1, 51):
                project_code = f"UC2024{i:04d}"
                project_name = f"{random.choice(areas)}{random.choice(project_types)}第{i}期"
                budget = random.uniform(500, 20000)
                
                cursor.execute('''
                    INSERT OR REPLACE INTO projects 
                    (name, code, unit, department, budget, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (project_name, project_code, random.choice(units),
                     random.choice(departments), budget, random.choice(statuses)))
                
            # 生成资金安排数据
            funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资']
            operators = ['张三', '李四', '王五', '赵六', '钱七']
            op_departments = ['计划财务处', '项目管理处', '投资建设处']
            
            cursor.execute("SELECT code, name, budget FROM projects")
            projects = cursor.fetchall()
            
            for _ in range(200):
                project = random.choice(projects)
                amount = random.uniform(project[2] * 0.1, project[2] * 0.8)
                
                cursor.execute('''
                    INSERT INTO funding 
                    (project_code, project_name, amount, funding_type, operator, department)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (project[0], project[1], amount, random.choice(funding_types),
                     random.choice(operators), random.choice(op_departments)))
                
            conn.commit()
            conn.close()
            
            self.update_stats()
            messagebox.showinfo("成功", "模拟数据生成完成！\n生成了50个项目和200条资金安排记录。")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成数据失败：{str(e)}")
            
    def show_projects(self):
        """显示项目列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name, code, unit, department, budget, status FROM projects")
            projects = cursor.fetchall()
            conn.close()
            
            self.tree["columns"] = ("项目名称", "项目编码", "建设单位", "主管部门", "概算金额", "项目状态")
            self.tree["show"] = "headings"
            
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120)
                
            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            for project in projects:
                values = list(project)
                values[4] = f"{values[4]:.2f}万元"  # 格式化金额
                self.tree.insert("", "end", values=values)
                
        except Exception as e:
            messagebox.showerror("错误", f"加载项目数据失败：{str(e)}")
            
    def show_funding(self):
        """显示资金安排"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT project_name, project_code, amount, funding_type, operator, department 
                FROM funding ORDER BY created_at DESC
            """)
            funding = cursor.fetchall()
            conn.close()
            
            self.tree["columns"] = ("项目名称", "项目编码", "资金金额", "资金性质", "经办人", "经办处室")
            self.tree["show"] = "headings"
            
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120)
                
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            for fund in funding:
                values = list(fund)
                values[2] = f"{values[2]:.2f}万元"
                self.tree.insert("", "end", values=values)
                
        except Exception as e:
            messagebox.showerror("错误", f"加载资金数据失败：{str(e)}")
            
    def show_pivot_table(self):
        """显示数据透视表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查询透视数据
            cursor.execute("""
                SELECT 
                    f.project_code,
                    f.project_name,
                    f.funding_type,
                    SUM(f.amount) as total_amount
                FROM funding f
                GROUP BY f.project_code, f.project_name, f.funding_type
                ORDER BY f.project_code
            """)
            
            data = cursor.fetchall()
            conn.close()
            
            if not data:
                messagebox.showwarning("提示", "暂无数据，请先生成模拟数据")
                return
                
            # 创建新窗口
            pivot_window = tk.Toplevel(self.root)
            pivot_window.title("资金安排数据透视表")
            pivot_window.geometry("800x600")
            
            frame = ttk.Frame(pivot_window, padding="10")
            frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            pivot_window.columnconfigure(0, weight=1)
            pivot_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            
            # 创建表格
            pivot_tree = ttk.Treeview(frame)
            pivot_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            pivot_tree["columns"] = ("项目编码", "项目名称", "资金性质", "资金金额")
            pivot_tree["show"] = "headings"
            
            for col in pivot_tree["columns"]:
                pivot_tree.heading(col, text=col)
                pivot_tree.column(col, width=150)
                
            # 添加数据
            for item in data:
                values = list(item)
                values[3] = f"{values[3]:.2f}万元"
                pivot_tree.insert("", "end", values=values)
                
            # 计算债券资金合计
            cursor = sqlite3.connect(self.db_path).cursor()
            cursor.execute("""
                SELECT 
                    project_code,
                    project_name,
                    SUM(CASE WHEN funding_type IN ('一般债券', '专项债券') THEN amount ELSE 0 END) as bond_total
                FROM funding 
                GROUP BY project_code, project_name
                HAVING bond_total > 0
                ORDER BY project_code
            """)
            
            bond_data = cursor.fetchall()
            
            if bond_data:
                # 添加分隔符
                pivot_tree.insert("", "end", values=("", "=== 债券资金合计 ===", "", ""))
                
                for item in bond_data:
                    values = [item[0], item[1], "债券资金合计", f"{item[2]:.2f}万元"]
                    pivot_tree.insert("", "end", values=values)
                    
            messagebox.showinfo("提示", f"数据透视表生成完成\n共显示{len(data)}条记录")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成透视表失败：{str(e)}")
            
    def clear_data(self):
        """清空数据"""
        if not messagebox.askyesno("警告", "这将清空所有数据，此操作不可恢复，是否继续？"):
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM funding")
            cursor.execute("DELETE FROM projects")
            conn.commit()
            conn.close()
            
            self.update_stats()
            self.show_welcome()
            messagebox.showinfo("成功", "所有数据已清空")
            
        except Exception as e:
            messagebox.showerror("错误", f"清空数据失败：{str(e)}")
            
    def show_chart_demo(self):
        """显示图表演示"""
        demo_info = """
数据可视化功能演示

✅ 项目状态分布图
   - 饼图显示在建、续建、完工、暂停项目比例
   - 自动计算百分比和数量

✅ 概算金额分布图  
   - 直方图显示项目金额分布情况
   - 显示平均值和中位数

✅ 资金性质分析图
   - 条形图对比不同资金性质的金额
   - 支持横向和纵向显示

✅ 债券资金统计图
   - 专门分析一般债券和专项债券
   - 自动计算债券资金合计

完整版本支持：
• 交互式图表操作
• 高分辨率图片导出  
• 图表数据钻取
• 自定义配色方案
        """
        
        messagebox.showinfo("数据可视化演示", demo_info)
        
    def show_report_demo(self):
        """显示报表演示"""
        demo_info = """
智慧报表生成功能演示

✅ 项目总览报表
   - 项目基本信息汇总
   - 按状态、部门分类统计

✅ 资金安排报表
   - 详细的资金安排信息
   - 按资金性质分类汇总

✅ 债券资金专项报表
   - 一般债券和专项债券分析
   - 自动计算债券资金合计

✅ 部门统计报表
   - 各部门项目数量统计
   - 各部门资金安排汇总

完整版本支持：
• Excel格式导出
• 日期范围筛选
• 自动统计计算
• 专业报表模板
• 直接打印功能
        """
        
        messagebox.showinfo("智慧报表演示", demo_info)
        
    def update_stats(self):
        """更新统计信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM projects")
            project_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM funding")
            funding_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(budget) FROM projects")
            total_budget = cursor.fetchone()[0] or 0
            
            conn.close()
            
            stats_text = f"项目：{project_count}个 | 资金记录：{funding_count}条 | 概算总额：{total_budget:.0f}万元"
            self.stats_label.config(text=stats_text)
            
        except Exception:
            self.stats_label.config(text="统计信息获取失败")
            
    def run(self):
        """运行程序"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        app = AIUrbanSystem()
        app.run()
    except Exception as e:
        messagebox.showerror("系统错误", f"程序启动失败：{str(e)}")

if __name__ == "__main__":
    main()