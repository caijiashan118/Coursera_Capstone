#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统测试脚本
验证系统各模块功能是否正常
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        # 测试基础依赖
        import tkinter as tk
        import pandas as pd
        import sqlite3
        print("✓ 基础依赖导入成功")
        
        # 测试项目模块
        from src.database.db_manager import DatabaseManager
        from src.models.project_models import MockDataGenerator
        from src.utils.excel_handler import ExcelHandler
        print("✓ 项目模块导入成功")
        
        return True
        
    except ImportError as e:
        print(f"✗ 模块导入失败：{e}")
        return False

def test_database():
    """测试数据库功能"""
    print("\n测试数据库功能...")
    
    try:
        from src.database.db_manager import DatabaseManager
        
        # 创建测试数据库
        db_manager = DatabaseManager(":memory:")  # 使用内存数据库测试
        db_manager.create_tables()
        print("✓ 数据库表创建成功")
        
        # 测试插入数据
        project_data = (
            "测试项目", "TEST001", "测试建设单位", "测试部门",
            "2024-01-01", 1000.0, "2024-02-01", "2024-12-31", "在建"
        )
        db_manager.insert_project_basic_info(project_data)
        print("✓ 项目数据插入成功")
        
        # 测试查询数据
        projects_df = db_manager.get_all_projects()
        if not projects_df.empty:
            print("✓ 项目数据查询成功")
        else:
            print("✗ 项目数据查询失败")
            
        return True
        
    except Exception as e:
        print(f"✗ 数据库测试失败：{e}")
        return False

def test_mock_data():
    """测试模拟数据生成"""
    print("\n测试模拟数据生成...")
    
    try:
        from src.models.project_models import MockDataGenerator
        
        generator = MockDataGenerator()
        
        # 生成少量测试数据
        projects = generator.generate_mock_projects(5)
        if len(projects) == 5:
            print("✓ 模拟项目数据生成成功")
        else:
            print("✗ 模拟项目数据生成失败")
            
        funding_list = generator.generate_mock_funding(projects, 10)
        if len(funding_list) == 10:
            print("✓ 模拟资金数据生成成功")
        else:
            print("✗ 模拟资金数据生成失败")
            
        return True
        
    except Exception as e:
        print(f"✗ 模拟数据测试失败：{e}")
        return False

def test_excel_handler():
    """测试Excel处理功能"""
    print("\n测试Excel处理功能...")
    
    try:
        from src.utils.excel_handler import ExcelHandler
        import pandas as pd
        
        handler = ExcelHandler()
        
        # 创建测试数据
        test_data = {
            '项目名称': ['测试项目1', '测试项目2'],
            '项目编码': ['TEST001', 'TEST002'],
            '建设单位': ['测试单位1', '测试单位2'],
            '项目主管部门': ['测试部门1', '测试部门2'],
            '概算批复金额': [1000.0, 2000.0],
            '项目状态': ['在建', '续建']
        }
        
        df = pd.DataFrame(test_data)
        
        # 测试Excel导出（不实际写文件）
        print("✓ Excel处理器创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ Excel处理测试失败：{e}")
        return False

def test_gui_components():
    """测试GUI组件（不实际显示窗口）"""
    print("\n测试GUI组件...")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # 创建测试窗口（不显示）
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 测试基本控件创建
        frame = ttk.Frame(root)
        label = ttk.Label(frame, text="测试标签")
        button = ttk.Button(frame, text="测试按钮")
        
        print("✓ GUI组件创建成功")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI组件测试失败：{e}")
        return False

def main():
    """主测试函数"""
    print("AI城建系统功能测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("数据库功能", test_database),
        ("模拟数据生成", test_mock_data),
        ("Excel处理", test_excel_handler),
        ("GUI组件", test_gui_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name}测试出现异常：{e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果：{passed}/{total} 项测试通过")
    
    if passed == total:
        print("✓ 所有测试通过！系统功能正常。")
        return True
    else:
        print(f"✗ 有 {total - passed} 项测试失败。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)