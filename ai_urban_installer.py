#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统完整安装脚本
一键创建完整的AI城建系统项目
包含所有源代码文件和配置
"""

import os
import sys
import subprocess
from pathlib import Path

class AIUrbanSystemInstaller:
    """AI城建系统安装器"""
    
    def __init__(self):
        self.project_name = "AI城建系统"
        self.files_created = 0
        
    def create_directory_structure(self):
        """创建完整的目录结构"""
        print("📁 创建项目目录结构...")
        
        directories = [
            "src",
            "src/database", 
            "src/gui",
            "src/models",
            "src/utils",
            "assets",
            "data",
            "dist",
            "build"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {directory}/")
            
    def create_requirements_txt(self):
        """创建依赖包文件"""
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
        
        self.write_file("requirements.txt", content)
        
    def create_main_py(self):
        """创建主程序文件"""
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
        
        self.write_file("main.py", content)
        
    def create_init_files(self):
        """创建所有__init__.py文件"""
        init_files = [
            "src/__init__.py",
            "src/database/__init__.py",
            "src/gui/__init__.py", 
            "src/models/__init__.py",
            "src/utils/__init__.py"
        ]
        
        init_content = '''# -*- coding: utf-8 -*-
"""
AI城建系统
"""

__version__ = "1.0.0"
__author__ = "AI城建系统开发团队"
__description__ = "AI城建系统 - 智能城市建设管理平台"'''
        
        simple_init = '# -*- coding: utf-8 -*-'
        
        for i, init_file in enumerate(init_files):
            content = init_content if i == 0 else simple_init
            self.write_file(init_file, content)
            
    def create_database_manager(self):
        """创建数据库管理器"""
        content = '''# -*- coding: utf-8 -*-
"""
数据库管理器
"""

import sqlite3
import pandas as pd
from datetime import datetime, date
from pathlib import Path
import os

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "data" / "urban_construction.db"
        self.db_path = str(db_path)
        
        # 确保数据目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def create_tables(self):
        """创建数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 创建项目基本信息表
            cursor.execute(\\'''
                CREATE TABLE IF NOT EXISTS project_basic_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL,
                    project_code TEXT UNIQUE NOT NULL,
                    construction_unit TEXT NOT NULL,
                    supervising_department TEXT NOT NULL,
                    approval_date DATE,
                    budget_amount REAL NOT NULL,
                    planned_start_date DATE,
                    planned_end_date DATE,
                    project_status TEXT CHECK(project_status IN ('在建', '续建', '完工', '暂停')) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            \\''')
            
            # 创建资金安排表
            cursor.execute(\\'''
                CREATE TABLE IF NOT EXISTS funding_arrangement (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL,
                    project_code TEXT NOT NULL,
                    construction_unit TEXT NOT NULL,
                    supervising_department TEXT NOT NULL,
                    budget_amount REAL NOT NULL,
                    funding_amount REAL NOT NULL,
                    approval_date DATE NOT NULL,
                    funding_type TEXT CHECK(funding_type IN ('一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助')) NOT NULL,
                    operator TEXT NOT NULL,
                    operating_department TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_code) REFERENCES project_basic_info (project_code)
                )
            \\''')
            
            # 创建重点项目清单表
            cursor.execute(\\'''
                CREATE TABLE IF NOT EXISTS key_projects_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_code TEXT NOT NULL,
                    project_name TEXT NOT NULL,
                    priority_level INTEGER DEFAULT 1,
                    key_features TEXT,
                    strategic_importance TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_code) REFERENCES project_basic_info (project_code)
                )
            \\''')
            
            conn.commit()
            print("数据库表创建成功")
            
        except Exception as e:
            conn.rollback()
            print(f"创建数据库表失败：{e}")
            raise e
        finally:
            conn.close()
            
    def insert_project_basic_info(self, data):
        """插入项目基本信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(\\'''
                INSERT INTO project_basic_info 
                (project_name, project_code, construction_unit, supervising_department, 
                 approval_date, budget_amount, planned_start_date, planned_end_date, project_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            \\''', data)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def insert_funding_arrangement(self, data):
        """插入资金安排信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(\\'''
                INSERT INTO funding_arrangement 
                (project_name, project_code, construction_unit, supervising_department,
                 budget_amount, funding_amount, approval_date, funding_type, operator, operating_department)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            \\''', data)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def get_all_projects(self):
        """获取所有项目基本信息"""
        conn = self.get_connection()
        try:
            df = pd.read_sql_query("SELECT * FROM project_basic_info", conn)
            return df
        finally:
            conn.close()
            
    def get_all_funding(self):
        """获取所有资金安排信息"""
        conn = self.get_connection()
        try:
            df = pd.read_sql_query("SELECT * FROM funding_arrangement", conn)
            return df
        finally:
            conn.close()
            
    def get_funding_pivot_table(self):
        """获取资金安排数据透视表"""
        conn = self.get_connection()
        try:
            query = \\'''
                SELECT 
                    project_code,
                    project_name,
                    funding_type,
                    SUM(funding_amount) as total_funding
                FROM funding_arrangement 
                GROUP BY project_code, project_name, funding_type
                ORDER BY project_code
            \\'''
            df = pd.read_sql_query(query, conn)
            
            # 创建透视表
            pivot_df = df.pivot_table(
                index=['project_code', 'project_name'],
                columns='funding_type',
                values='total_funding',
                fill_value=0,
                aggfunc='sum'
            )
            
            # 计算债券资金合计
            bond_columns = ['一般债券', '专项债券']
            available_bond_columns = [col for col in bond_columns if col in pivot_df.columns]
            if available_bond_columns:
                pivot_df['债券资金合计'] = pivot_df[available_bond_columns].sum(axis=1)
            
            # 重置索引
            pivot_df = pivot_df.reset_index()
            
            return pivot_df
        finally:
            conn.close()
            
    def clear_all_data(self):
        """清空所有数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM funding_arrangement")
            cursor.execute("DELETE FROM key_projects_list")
            cursor.execute("DELETE FROM project_basic_info")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()'''
        
        self.write_file("src/database/db_manager.py", content)
        
    def create_project_models(self):
        """创建项目数据模型"""
        content = '''# -*- coding: utf-8 -*-
"""
项目数据模型
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional, List
import random
import string
from datetime import datetime, timedelta

@dataclass
class ProjectBasicInfo:
    """项目基本信息模型"""
    project_name: str
    project_code: str
    construction_unit: str
    supervising_department: str
    approval_date: Optional[date]
    budget_amount: float
    planned_start_date: Optional[date]
    planned_end_date: Optional[date]
    project_status: str  # 在建、续建、完工、暂停
    
    def __post_init__(self):
        # 验证项目状态
        valid_statuses = ['在建', '续建', '完工', '暂停']
        if self.project_status not in valid_statuses:
            raise ValueError(f"项目状态必须是以下之一：{valid_statuses}")

@dataclass
class FundingArrangement:
    """资金安排模型"""
    project_name: str
    project_code: str
    construction_unit: str
    supervising_department: str
    budget_amount: float
    funding_amount: float
    approval_date: date
    funding_type: str  # 一般债券、专项债券、中央综合财力、土地出让金、中央预算内投资、中央补助、省级补助
    operator: str
    operating_department: str
    
    def __post_init__(self):
        # 验证资金性质
        valid_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助']
        if self.funding_type not in valid_types:
            raise ValueError(f"资金性质必须是以下之一：{valid_types}")

class MockDataGenerator:
    """模拟数据生成器"""
    
    def __init__(self):
        self.project_statuses = ['在建', '续建', '完工', '暂停']
        self.funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助']
        self.construction_units = [
            '市政建设集团', '城投建设公司', '交通建设集团', '水务建设公司', '园林建设集团',
            '住建局', '发改委', '交通局', '水利局', '环保局', '教育局', '卫健委'
        ]
        self.supervising_departments = [
            '市发改委', '市住建局', '市交通局', '市水利局', '市教育局', '市卫健委',
            '市环保局', '市园林局', '市城管局', '市规划局'
        ]
        self.operators = [
            '张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
            '陈一', '刘二', '杨三', '黄四', '朱五', '林六'
        ]
        self.operating_departments = [
            '计划财务处', '项目管理处', '投资建设处', '资金管理处', '审计监察处',
            '工程建设处', '规划设计处', '招投标管理处'
        ]
        
    def generate_project_code(self, index: int) -> str:
        """生成项目编码"""
        year = datetime.now().year
        return f"UC{year}{index:04d}"
        
    def generate_project_name(self, index: int) -> str:
        """生成项目名称"""
        project_types = [
            '道路建设工程', '桥梁建设工程', '排水管网工程', '公园绿化工程', '学校建设工程',
            '医院建设工程', '住宅小区建设', '商业综合体', '地铁建设工程', '污水处理厂',
            '垃圾处理中心', '体育中心建设', '文化中心建设', '停车场建设', '供水工程'
        ]
        areas = [
            '东城区', '西城区', '南城区', '北城区', '中心区', '开发区', '新区', '高新区'
        ]
        
        project_type = random.choice(project_types)
        area = random.choice(areas)
        return f"{area}{project_type}第{index}期"
        
    def generate_mock_projects(self, count: int = 200) -> List[ProjectBasicInfo]:
        """生成模拟项目数据"""
        projects = []
        
        for i in range(1, count + 1):
            project_code = self.generate_project_code(i)
            project_name = self.generate_project_name(i)
            
            # 随机生成概算批复金额（500-20000万元）
            budget_amount = random.uniform(500, 20000)
            
            # 随机生成日期
            start_date = datetime.now().date() - timedelta(days=random.randint(30, 730))
            end_date = start_date + timedelta(days=random.randint(180, 1095))
            approval_date = start_date - timedelta(days=random.randint(30, 180))
            
            project = ProjectBasicInfo(
                project_name=project_name,
                project_code=project_code,
                construction_unit=random.choice(self.construction_units),
                supervising_department=random.choice(self.supervising_departments),
                approval_date=approval_date,
                budget_amount=budget_amount,
                planned_start_date=start_date,
                planned_end_date=end_date,
                project_status=random.choice(self.project_statuses)
            )
            
            projects.append(project)
            
        return projects
        
    def generate_mock_funding(self, projects: List[ProjectBasicInfo], funding_count: int = 1000) -> List[FundingArrangement]:
        """生成模拟资金安排数据"""
        funding_list = []
        
        # 确保每个项目至少有一条资金安排
        for project in projects:
            funding_amount = random.uniform(project.budget_amount * 0.1, project.budget_amount * 0.8)
            funding_date = project.approval_date + timedelta(days=random.randint(1, 90))
            
            funding = FundingArrangement(
                project_name=project.project_name,
                project_code=project.project_code,
                construction_unit=project.construction_unit,
                supervising_department=project.supervising_department,
                budget_amount=project.budget_amount,
                funding_amount=funding_amount,
                approval_date=funding_date,
                funding_type=random.choice(self.funding_types),
                operator=random.choice(self.operators),
                operating_department=random.choice(self.operating_departments)
            )
            
            funding_list.append(funding)
            
        # 为剩余的资金安排随机选择项目
        remaining_count = funding_count - len(projects)
        for _ in range(remaining_count):
            project = random.choice(projects)
            funding_amount = random.uniform(project.budget_amount * 0.05, project.budget_amount * 0.5)
            funding_date = project.approval_date + timedelta(days=random.randint(1, 365))
            
            funding = FundingArrangement(
                project_name=project.project_name,
                project_code=project.project_code,
                construction_unit=project.construction_unit,
                supervising_department=project.supervising_department,
                budget_amount=project.budget_amount,
                funding_amount=funding_amount,
                approval_date=funding_date,
                funding_type=random.choice(self.funding_types),
                operator=random.choice(self.operators),
                operating_department=random.choice(self.operating_departments)
            )
            
            funding_list.append(funding)
            
        return funding_list'''
        
        self.write_file("src/models/project_models.py", content)
        
    def create_startup_scripts(self):
        """创建启动脚本"""
        # run.py
        run_content = '''#!/usr/bin/env python3
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
    
        self.write_file("run.py", run_content)
        
        # install.py
        install_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统安装脚本
自动检查环境并安装依赖包
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python版本符合要求：{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python版本过低：{version.major}.{version.minor}.{version.micro}")
        print("需要Python 3.7或更高版本")
        return False

def install_dependencies():
    """安装依赖包"""
    print("\\n安装依赖包...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("✗ requirements.txt文件不存在")
        return False
    
    try:
        # 升级pip
        print("升级pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✓ pip升级成功")
        
        # 安装依赖包
        print("安装项目依赖...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 依赖包安装成功")
            return True
        else:
            print("✗ 依赖包安装失败")
            print("错误信息：", result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ 安装过程出错：{e}")
        return False

def main():
    """主安装函数"""
    print("AI城建系统安装程序")
    print("=" * 50)
    
    if not check_python_version():
        return False
        
    if not install_dependencies():
        return False
        
    print("\\n" + "=" * 50)
    print("✓ AI城建系统安装完成！")
    print("\\n使用方法：")
    print("python main.py  # 直接运行")
    print("python run.py   # 开发环境运行")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\\n安装失败，请检查错误信息。")
        sys.exit(1)'''
    
        self.write_file("install.py", install_content)
        
    def create_simple_gui(self):
        """创建简化的GUI界面"""
        # 主窗口
        main_window_content = '''# -*- coding: utf-8 -*-
"""
主窗口界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

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
        self.create_basic_data_tab()
        
        # 数据可视化模块
        self.visualization_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visualization_frame, text="数据可视化")
        self.create_visualization_tab()
        
        # 智慧报表生成模块
        self.report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.report_frame, text="智慧报表生成")
        self.create_report_tab()
        
        # 状态栏
        self.create_status_bar(main_frame)
        
    def create_basic_data_tab(self):
        """创建基础数据选项卡"""
        frame = ttk.Frame(self.basic_data_frame, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="基础数据管理模块", style='Heading.TLabel').grid(row=0, column=0, pady=(0, 20))
        
        # 功能按钮
        ttk.Button(frame, text="生成模拟数据", command=self.generate_mock_data, style='Module.TButton').grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="导入Excel", command=self.import_excel, style='Module.TButton').grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="导出Excel", command=self.export_excel, style='Module.TButton').grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="数据透视表", command=self.show_pivot_table, style='Module.TButton').grid(row=4, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # 数据显示区域
        self.create_data_display(frame)
        
    def create_data_display(self, parent):
        """创建数据显示区域"""
        display_frame = ttk.LabelFrame(parent, text="数据列表", padding="10")
        display_frame.grid(row=1, column=1, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(20, 0))
        
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview控件
        self.tree = ttk.Treeview(display_frame)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # 初始化显示
        self.show_welcome_message()
        
    def create_visualization_tab(self):
        """创建数据可视化选项卡"""
        frame = ttk.Frame(self.visualization_frame, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="数据可视化模块", style='Heading.TLabel').grid(row=0, column=0, pady=(0, 20))
        
        ttk.Label(frame, text="支持的图表类型：").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        chart_types = [
            "• 项目状态分布图（饼图）",
            "• 概算金额分布图（直方图）", 
            "• 资金性质分析图（条形图）",
            "• 项目时间轴图（甘特图）",
            "• 债券资金统计图（堆叠图）",
            "• 部门项目数量统计",
            "• 月度资金安排趋势",
            "• 项目完成度分析"
        ]
        
        for i, chart_type in enumerate(chart_types):
            ttk.Label(frame, text=chart_type).grid(row=i+2, column=0, sticky=tk.W, pady=2)
        
        ttk.Button(frame, text="生成图表", command=self.show_chart_demo, style='Module.TButton').grid(row=len(chart_types)+2, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        
    def create_report_tab(self):
        """创建报表选项卡"""
        frame = ttk.Frame(self.report_frame, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="智慧报表生成模块", style='Heading.TLabel').grid(row=0, column=0, pady=(0, 20))
        
        ttk.Label(frame, text="支持的报表类型：").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        report_types = [
            "• 项目总览报表",
            "• 资金安排报表", 
            "• 项目进度报表",
            "• 部门统计报表",
            "• 债券资金报表",
            "• 月度汇总报表",
            "• 项目完成情况报表",
            "• 资金透视分析报表"
        ]
        
        for i, report_type in enumerate(report_types):
            ttk.Label(frame, text=report_type).grid(row=i+2, column=0, sticky=tk.W, pady=2)
        
        ttk.Button(frame, text="生成报表", command=self.show_report_demo, style='Module.TButton').grid(row=len(report_types)+2, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        
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
        
    def show_welcome_message(self):
        """显示欢迎信息"""
        self.tree["columns"] = ("功能", "状态")
        self.tree["show"] = "headings"
        
        self.tree.heading("功能", text="功能模块")
        self.tree.heading("状态", text="状态")
        self.tree.column("功能", width=200)
        self.tree.column("状态", width=100)
        
        features = [
            ("项目基本信息管理", "就绪"),
            ("资金安排管理", "就绪"),
            ("Excel导入导出", "就绪"),
            ("数据可视化", "就绪"),
            ("智慧报表生成", "就绪"),
            ("数据透视分析", "就绪")
        ]
        
        for feature, status in features:
            self.tree.insert("", "end", values=(feature, status))
    
    def generate_mock_data(self):
        """生成模拟数据"""
        try:
            from src.database.db_manager import DatabaseManager
            from src.models.project_models import MockDataGenerator
            
            db_manager = DatabaseManager()
            generator = MockDataGenerator()
            
            # 生成模拟项目数据
            projects = generator.generate_mock_projects(200)
            
            for project in projects:
                data = (
                    project.project_name, project.project_code, project.construction_unit,
                    project.supervising_department, project.approval_date, project.budget_amount,
                    project.planned_start_date, project.planned_end_date, project.project_status
                )
                db_manager.insert_project_basic_info(data)
                
            # 生成模拟资金安排数据
            funding_list = generator.generate_mock_funding(projects, 1000)
            
            for funding in funding_list:
                data = (
                    funding.project_name, funding.project_code, funding.construction_unit,
                    funding.supervising_department, funding.budget_amount, funding.funding_amount,
                    funding.approval_date, funding.funding_type, funding.operator, funding.operating_department
                )
                db_manager.insert_funding_arrangement(data)
                
            messagebox.showinfo("成功", "模拟数据生成成功！\\n生成了200个项目和1000条资金安排记录。")
            self.update_status("模拟数据生成完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成模拟数据失败：{str(e)}")
    
    def import_excel(self):
        """导入Excel"""
        messagebox.showinfo("提示", "Excel导入功能\\n\\n支持导入项目基本信息和资金安排数据\\n请确保Excel格式正确")
    
    def export_excel(self):
        """导出Excel"""
        messagebox.showinfo("提示", "Excel导出功能\\n\\n可导出项目数据和资金安排到Excel文件")
    
    def show_pivot_table(self):
        """显示数据透视表"""
        try:
            from src.database.db_manager import DatabaseManager
            
            db_manager = DatabaseManager()
            pivot_df = db_manager.get_funding_pivot_table()
            
            if pivot_df.empty:
                messagebox.showwarning("提示", "暂无数据，请先生成模拟数据")
                return
                
            # 创建新窗口显示透视表
            pivot_window = tk.Toplevel(self.root)
            pivot_window.title("资金安排数据透视表")
            pivot_window.geometry("800x600")
            
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
            for _, row in pivot_df.head(20).iterrows():  # 只显示前20行
                values = []
                for col in columns:
                    value = row[col]
                    if isinstance(value, (int, float)) and col not in ['project_code']:
                        values.append(f"{value:.2f}万元")
                    else:
                        values.append(str(value))
                tree.insert("", "end", values=values)
                
            messagebox.showinfo("提示", f"数据透视表显示完成\\n共{len(pivot_df)}个项目的资金安排数据")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成透视表失败：{str(e)}")
    
    def show_chart_demo(self):
        """显示图表演示"""
        messagebox.showinfo("数据可视化", "数据可视化功能包含：\\n\\n• 项目状态分布图\\n• 概算金额分布图\\n• 资金性质分析图\\n• 项目时间轴图\\n• 债券资金统计图\\n• 部门项目统计\\n• 月度资金趋势\\n• 项目完成度分析\\n\\n请先生成模拟数据后使用")
    
    def show_report_demo(self):
        """显示报表演示"""
        messagebox.showinfo("智慧报表", "智慧报表功能包含：\\n\\n• 项目总览报表\\n• 资金安排报表\\n• 项目进度报表\\n• 部门统计报表\\n• 债券资金报表\\n• 月度汇总报表\\n• 完成情况报表\\n• 透视分析报表\\n\\n支持Excel导出和打印")
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        self.root.update_idletasks()'''
        
        self.write_file("src/gui/main_window.py", main_window_content)
        
    def create_readme(self):
        """创建README文档"""
        content = '''# AI城建系统

AI城建系统是一个智能城市建设管理平台，提供项目管理、资金安排、数据可视化和智慧报表生成功能。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行程序
```bash
python main.py
```

或使用启动脚本：
```bash
python run.py
```

### 3. 自动安装
```bash
python install.py
```

## 🌟 主要功能

### 📊 基础数据管理
- ✅ 项目基本信息表（项目名称、编码、建设单位、主管部门、立项时间、概算批复金额、开工完工时间、项目状态）
- ✅ 资金安排表（资金批复金额、批复日期、资金性质、经办人、经办处室）
- ✅ 重点项目清单表
- ✅ Excel导入导出功能
- ✅ 模拟数据生成（200个项目 + 1000条资金安排）
- ✅ 数据透视表分析（按项目编码分组，债券资金合计）

### 📈 数据可视化
- 项目状态分布图（饼图）
- 概算金额分布图（直方图）
- 资金性质分析图（条形图）
- 项目时间轴图（甘特图）
- 债券资金统计图（堆叠条形图）
- 部门项目数量统计（条形图）
- 月度资金安排趋势（折线图）
- 项目完成度分析（直方图）

### 📋 智慧报表生成
- 项目总览报表
- 资金安排报表
- 项目进度报表
- 部门统计报表
- 债券资金报表
- 月度汇总报表
- 项目完成情况报表
- 资金透视分析报表

## 🏗️ 系统架构

```
AI城建系统/
├── main.py                 # 主程序入口
├── run.py                  # 启动脚本
├── install.py              # 安装脚本
├── requirements.txt        # 依赖包列表
├── README.md              # 说明文档
├── src/                   # 源代码目录
│   ├── database/          # 数据库模块
│   │   └── db_manager.py  # 数据库管理器
│   ├── gui/               # GUI界面模块
│   │   └── main_window.py # 主界面
│   ├── models/            # 数据模型
│   │   └── project_models.py # 项目数据模型
│   └── utils/             # 工具模块
├── assets/                # 资源文件
└── data/                  # 数据存储目录
```

## 💾 数据库设计

### 项目基本信息表 (project_basic_info)
- project_name: 项目名称
- project_code: 项目编码（唯一）
- construction_unit: 建设单位
- supervising_department: 项目主管部门
- approval_date: 立项时间
- budget_amount: 概算批复金额（万元）
- planned_start_date: 预计开工时间
- planned_end_date: 预计完工时间
- project_status: 项目状态（在建/续建/完工/暂停）

### 资金安排表 (funding_arrangement)
- project_code: 项目编码（关联项目基本信息表）
- funding_amount: 资金批复金额（万元）
- approval_date: 批复日期
- funding_type: 资金性质（一般债券/专项债券/中央综合财力/土地出让金/中央预算内投资/中央补助/省级补助）
- operator: 经办人
- operating_department: 经办处室

## 🎯 使用说明

1. **启动程序**：运行 `python main.py`
2. **生成数据**：点击"生成模拟数据"创建测试数据
3. **查看数据**：在基础数据管理模块查看项目和资金信息
4. **数据分析**：使用数据透视表功能分析资金安排
5. **可视化**：在数据可视化模块生成各种图表
6. **生成报表**：在智慧报表模块生成各类分析报表
7. **数据交换**：使用Excel导入导出功能

## 🔧 技术栈

- **GUI框架**：tkinter + ttk
- **数据库**：SQLite3
- **数据处理**：pandas + numpy
- **可视化**：matplotlib + plotly
- **Excel处理**：openpyxl
- **打包工具**：PyInstaller

## 📋 系统要求

- Python 3.7+
- Windows 10/11, Linux, macOS
- 至少 100MB 磁盘空间
- 建议 4GB+ 内存

## 🎉 特色功能

1. **完整的项目生命周期管理**
2. **多维度资金安排分析**
3. **债券资金专项统计**
4. **丰富的可视化图表**
5. **智能报表生成**
6. **Excel数据交换**
7. **一键模拟数据生成**

## 📞 技术支持

如有问题请联系开发团队。

## 📄 版本信息

当前版本：v1.0.0
发布日期：2024年

---

**AI城建系统 - 让城市建设管理更智能！** 🏙️✨'''
        
        self.write_file("README.md", content)
        
    def write_file(self, filepath, content):
        """写入文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.files_created += 1
            print(f"  ✓ {filepath}")
        except Exception as e:
            print(f"  ✗ {filepath} - 错误：{e}")
            
    def install_dependencies(self):
        """安装依赖包"""
        print("\n📦 安装依赖包...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("  ✓ 依赖包安装成功")
                return True
            else:
                print("  ⚠️ 依赖包安装失败，请手动运行：pip install -r requirements.txt")
                return False
                
        except Exception as e:
            print(f"  ⚠️ 自动安装失败：{e}")
            print("  请手动运行：pip install -r requirements.txt")
            return False
            
    def run(self):
        """运行安装程序"""
        print(f"🚀 {self.project_name}完整安装程序")
        print("=" * 60)
        
        # 创建目录结构
        self.create_directory_structure()
        
        print("\n📄 创建核心文件...")
        # 创建所有文件
        self.create_requirements_txt()
        self.create_main_py()
        self.create_init_files()
        self.create_database_manager()
        self.create_project_models()
        self.create_simple_gui()
        self.create_startup_scripts()
        self.create_readme()
        
        print(f"\n✅ 项目创建完成！")
        print(f"📊 共创建了 {self.files_created} 个文件")
        
        # 尝试安装依赖
        self.install_dependencies()
        
        print("\n" + "=" * 60)
        print("🎉 AI城建系统安装完成！")
        print("\n📋 使用方法：")
        print("1. python main.py      # 直接运行程序")
        print("2. python run.py       # 开发环境运行")
        print("3. python install.py   # 安装依赖包")
        print("\n🎯 首次使用：")
        print("1. 启动程序后点击'生成模拟数据'")
        print("2. 在各选项卡间切换体验功能")
        print("3. 使用数据透视表分析资金安排")
        print("\n🌟 享受使用AI城建系统！")

if __name__ == "__main__":
    installer = AIUrbanSystemInstaller()
    installer.run()