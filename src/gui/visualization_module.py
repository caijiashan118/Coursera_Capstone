# -*- coding: utf-8 -*-
"""
数据可视化模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.db_manager import DatabaseManager

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class VisualizationModule:
    """数据可视化模块"""
    
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DatabaseManager()
        self.figure = None
        self.canvas = None
        
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
        
        # 右侧图表显示区域
        self.create_chart_area(main_frame)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = ttk.LabelFrame(parent, text="图表选择", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 图表类型选择
        ttk.Label(control_frame, text="选择图表类型：").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        chart_types = [
            "项目状态分布图",
            "概算金额分布图", 
            "资金性质分析图",
            "项目时间轴图",
            "债券资金统计图",
            "部门项目数量统计",
            "月度资金安排趋势",
            "项目完成度分析"
        ]
        
        self.chart_var = tk.StringVar(value=chart_types[0])
        
        for i, chart_type in enumerate(chart_types):
            ttk.Radiobutton(control_frame, text=chart_type, variable=self.chart_var, 
                           value=chart_type).grid(row=i+1, column=0, sticky=tk.W, pady=2)
            
        # 生成图表按钮
        ttk.Button(control_frame, text="生成图表", 
                  command=self.generate_chart).grid(row=len(chart_types)+1, column=0, 
                                                   sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 保存图表按钮
        ttk.Button(control_frame, text="保存图表", 
                  command=self.save_chart).grid(row=len(chart_types)+2, column=0, 
                                               sticky=(tk.W, tk.E), pady=5)
        
        # 刷新数据按钮
        ttk.Button(control_frame, text="刷新数据", 
                  command=self.refresh_charts).grid(row=len(chart_types)+3, column=0, 
                                                   sticky=(tk.W, tk.E), pady=5)
        
    def create_chart_area(self, parent):
        """创建图表显示区域"""
        chart_frame = ttk.LabelFrame(parent, text="图表显示", padding="10")
        chart_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.rowconfigure(0, weight=1)
        
        # 创建matplotlib图表
        self.figure = plt.Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加工具栏
        toolbar_frame = ttk.Frame(chart_frame)
        toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
        # 初始显示欢迎信息
        self.show_welcome_chart()
        
    def show_welcome_chart(self):
        """显示欢迎图表"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'AI城建系统\n数据可视化模块\n\n请选择图表类型并点击"生成图表"', 
                ha='center', va='center', fontsize=16, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
        
    def generate_chart(self):
        """生成图表"""
        try:
            chart_type = self.chart_var.get()
            
            if chart_type == "项目状态分布图":
                self.create_project_status_chart()
            elif chart_type == "概算金额分布图":
                self.create_budget_distribution_chart()
            elif chart_type == "资金性质分析图":
                self.create_funding_type_chart()
            elif chart_type == "项目时间轴图":
                self.create_project_timeline_chart()
            elif chart_type == "债券资金统计图":
                self.create_bond_funding_chart()
            elif chart_type == "部门项目数量统计":
                self.create_department_projects_chart()
            elif chart_type == "月度资金安排趋势":
                self.create_monthly_funding_trend()
            elif chart_type == "项目完成度分析":
                self.create_project_completion_chart()
                
        except Exception as e:
            messagebox.showerror("错误", f"生成图表失败：{str(e)}")
            
    def create_project_status_chart(self):
        """创建项目状态分布图"""
        try:
            df = self.db_manager.get_all_projects()
            if df.empty:
                self.show_no_data_chart("项目状态分布图")
                return
                
            status_counts = df['project_status'].value_counts()
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建饼图
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
            wedges, texts, autotexts = ax.pie(status_counts.values, labels=status_counts.index, 
                                             autopct='%1.1f%%', startangle=90, colors=colors)
            
            ax.set_title('项目状态分布图', fontsize=14, fontweight='bold')
            
            # 添加图例
            ax.legend(wedges, [f"{label}: {count}个" for label, count in status_counts.items()],
                     title="项目状态", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建项目状态分布图失败：{str(e)}")
            
    def create_budget_distribution_chart(self):
        """创建概算金额分布图"""
        try:
            df = self.db_manager.get_all_projects()
            if df.empty:
                self.show_no_data_chart("概算金额分布图")
                return
                
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建直方图
            ax.hist(df['budget_amount'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax.set_xlabel('概算金额（万元）')
            ax.set_ylabel('项目数量')
            ax.set_title('项目概算金额分布图', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # 添加统计信息
            mean_budget = df['budget_amount'].mean()
            median_budget = df['budget_amount'].median()
            
            ax.axvline(mean_budget, color='red', linestyle='--', label=f'平均值: {mean_budget:.2f}万元')
            ax.axvline(median_budget, color='green', linestyle='--', label=f'中位数: {median_budget:.2f}万元')
            ax.legend()
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建概算金额分布图失败：{str(e)}")
            
    def create_funding_type_chart(self):
        """创建资金性质分析图"""
        try:
            df = self.db_manager.get_all_funding()
            if df.empty:
                self.show_no_data_chart("资金性质分析图")
                return
                
            # 按资金性质汇总
            funding_summary = df.groupby('funding_type')['funding_amount'].sum().sort_values(ascending=True)
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建水平条形图
            bars = ax.barh(range(len(funding_summary)), funding_summary.values, 
                          color=plt.cm.Set3(np.linspace(0, 1, len(funding_summary))))
            
            ax.set_yticks(range(len(funding_summary)))
            ax.set_yticklabels(funding_summary.index)
            ax.set_xlabel('资金金额（万元）')
            ax.set_title('资金性质分析图', fontsize=14, fontweight='bold')
            
            # 在条形图上添加数值标签
            for i, (bar, value) in enumerate(zip(bars, funding_summary.values)):
                ax.text(value + max(funding_summary.values) * 0.01, i, f'{value:.2f}万元', 
                       va='center', ha='left')
            
            ax.grid(True, alpha=0.3, axis='x')
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建资金性质分析图失败：{str(e)}")
            
    def create_project_timeline_chart(self):
        """创建项目时间轴图"""
        try:
            df = self.db_manager.get_all_projects()
            if df.empty:
                self.show_no_data_chart("项目时间轴图")
                return
                
            # 过滤有效日期的项目
            df_valid = df.dropna(subset=['planned_start_date', 'planned_end_date'])
            if df_valid.empty:
                self.show_no_data_chart("项目时间轴图（无有效日期数据）")
                return
                
            # 转换日期格式
            df_valid['start_date'] = pd.to_datetime(df_valid['planned_start_date'])
            df_valid['end_date'] = pd.to_datetime(df_valid['planned_end_date'])
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建甘特图
            colors = plt.cm.Set3(np.linspace(0, 1, len(df_valid)))
            
            for i, (_, row) in enumerate(df_valid.head(10).iterrows()):  # 只显示前10个项目
                start = row['start_date']
                end = row['end_date']
                duration = (end - start).days
                
                ax.barh(i, duration, left=start, height=0.6, 
                       color=colors[i], alpha=0.8, 
                       label=row['project_name'][:20] + ('...' if len(row['project_name']) > 20 else ''))
            
            ax.set_xlabel('时间')
            ax.set_ylabel('项目')
            ax.set_title('项目时间轴图（前10个项目）', fontsize=14, fontweight='bold')
            
            # 设置y轴标签
            ax.set_yticks(range(len(df_valid.head(10))))
            ax.set_yticklabels([name[:15] + ('...' if len(name) > 15 else '') 
                               for name in df_valid.head(10)['project_name']])
            
            # 格式化x轴日期
            self.figure.autofmt_xdate()
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建项目时间轴图失败：{str(e)}")
            
    def create_bond_funding_chart(self):
        """创建债券资金统计图"""
        try:
            df = self.db_manager.get_all_funding()
            if df.empty:
                self.show_no_data_chart("债券资金统计图")
                return
                
            # 筛选债券资金
            bond_data = df[df['funding_type'].isin(['一般债券', '专项债券'])]
            if bond_data.empty:
                self.show_no_data_chart("债券资金统计图（无债券数据）")
                return
                
            # 按项目和债券类型汇总
            bond_summary = bond_data.groupby(['project_code', 'funding_type'])['funding_amount'].sum().unstack(fill_value=0)
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建堆叠条形图
            bond_summary.plot(kind='bar', stacked=True, ax=ax, 
                            color=['lightcoral', 'lightblue'])
            
            ax.set_title('债券资金统计图', fontsize=14, fontweight='bold')
            ax.set_xlabel('项目编码')
            ax.set_ylabel('资金金额（万元）')
            ax.legend(title='债券类型')
            ax.tick_params(axis='x', rotation=45)
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建债券资金统计图失败：{str(e)}")
            
    def create_department_projects_chart(self):
        """创建部门项目数量统计图"""
        try:
            df = self.db_manager.get_all_projects()
            if df.empty:
                self.show_no_data_chart("部门项目数量统计")
                return
                
            dept_counts = df['supervising_department'].value_counts()
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建条形图
            bars = ax.bar(range(len(dept_counts)), dept_counts.values, 
                         color=plt.cm.viridis(np.linspace(0, 1, len(dept_counts))))
            
            ax.set_xticks(range(len(dept_counts)))
            ax.set_xticklabels(dept_counts.index, rotation=45, ha='right')
            ax.set_ylabel('项目数量')
            ax.set_title('各部门项目数量统计', fontsize=14, fontweight='bold')
            
            # 在条形图上添加数值标签
            for bar, value in zip(bars, dept_counts.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                       str(value), ha='center', va='bottom')
            
            ax.grid(True, alpha=0.3, axis='y')
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建部门项目数量统计图失败：{str(e)}")
            
    def create_monthly_funding_trend(self):
        """创建月度资金安排趋势图"""
        try:
            df = self.db_manager.get_all_funding()
            if df.empty:
                self.show_no_data_chart("月度资金安排趋势")
                return
                
            # 转换日期并按月汇总
            df['approval_date'] = pd.to_datetime(df['approval_date'])
            df['year_month'] = df['approval_date'].dt.to_period('M')
            
            monthly_funding = df.groupby('year_month')['funding_amount'].sum()
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建折线图
            ax.plot(monthly_funding.index.astype(str), monthly_funding.values, 
                   marker='o', linewidth=2, markersize=6, color='blue')
            
            ax.set_title('月度资金安排趋势图', fontsize=14, fontweight='bold')
            ax.set_xlabel('月份')
            ax.set_ylabel('资金金额（万元）')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
            
            # 添加数值标签
            for x, y in zip(range(len(monthly_funding)), monthly_funding.values):
                ax.annotate(f'{y:.0f}万', (x, y), textcoords="offset points", 
                           xytext=(0,10), ha='center')
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建月度资金安排趋势图失败：{str(e)}")
            
    def create_project_completion_chart(self):
        """创建项目完成度分析图"""
        try:
            df = self.db_manager.get_all_projects()
            if df.empty:
                self.show_no_data_chart("项目完成度分析")
                return
                
            # 模拟完成度数据（基于项目状态）
            completion_mapping = {'完工': 100, '在建': 65, '续建': 45, '暂停': 20}
            df['completion'] = df['project_status'].map(completion_mapping)
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 创建完成度分布直方图
            ax.hist(df['completion'], bins=10, alpha=0.7, color='lightgreen', 
                   edgecolor='black', range=(0, 100))
            
            ax.set_xlabel('完成度（%）')
            ax.set_ylabel('项目数量')
            ax.set_title('项目完成度分析图', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # 添加平均完成度线
            mean_completion = df['completion'].mean()
            ax.axvline(mean_completion, color='red', linestyle='--', 
                      label=f'平均完成度: {mean_completion:.1f}%')
            ax.legend()
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            raise Exception(f"创建项目完成度分析图失败：{str(e)}")
            
    def show_no_data_chart(self, chart_name):
        """显示无数据图表"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, f'{chart_name}\n\n暂无数据\n请先生成模拟数据或导入数据', 
                ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
        
    def save_chart(self):
        """保存图表"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="保存图表",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("PDF files", "*.pdf")]
            )
            
            if file_path:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("成功", f"图表已保存到：{file_path}")
                
        except Exception as e:
            messagebox.showerror("错误", f"保存图表失败：{str(e)}")
            
    def refresh_charts(self):
        """刷新图表数据"""
        try:
            self.generate_chart()
            messagebox.showinfo("成功", "图表数据已刷新")
        except Exception as e:
            messagebox.showerror("错误", f"刷新图表失败：{str(e)}")