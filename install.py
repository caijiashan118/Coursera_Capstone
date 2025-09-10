#!/usr/bin/env python3
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
    print("\n安装依赖包...")
    
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

def check_gui_support():
    """检查GUI支持"""
    print("\n检查GUI支持...")
    
    try:
        import tkinter as tk
        
        # 尝试创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        root.destroy()
        
        print("✓ GUI支持正常")
        return True
        
    except ImportError:
        print("✗ tkinter不可用，请安装GUI支持")
        print("Ubuntu/Debian: sudo apt-get install python3-tk")
        print("CentOS/RHEL: sudo yum install tkinter")
        print("macOS: GUI支持应该已内置")
        return False
        
    except Exception as e:
        print(f"✗ GUI测试失败：{e}")
        print("可能是在无显示环境中运行，桌面环境下应该正常")
        return True  # 在无显示环境下不算错误

def create_directories():
    """创建必要的目录"""
    print("\n创建必要目录...")
    
    directories = ["data", "assets", "dist", "build"]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"✓ 目录已创建：{dir_name}")
    
    return True

def run_system_test():
    """运行系统测试"""
    print("\n运行系统测试...")
    
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                               capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✓ 系统测试通过")
            return True
        else:
            print("✗ 系统测试失败")
            if result.stderr:
                print("错误信息：", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ 系统测试出错：{e}")
        return False

def main():
    """主安装函数"""
    print("AI城建系统安装程序")
    print("=" * 50)
    
    steps = [
        ("检查Python版本", check_python_version),
        ("安装依赖包", install_dependencies),
        ("检查GUI支持", check_gui_support),
        ("创建必要目录", create_directories),
        ("运行系统测试", run_system_test)
    ]
    
    for step_name, step_func in steps:
        print(f"\n正在执行：{step_name}")
        if not step_func():
            print(f"\n✗ 安装失败于步骤：{step_name}")
            return False
    
    print("\n" + "=" * 50)
    print("✓ AI城建系统安装完成！")
    print("\n使用方法：")
    print("1. 开发环境运行：python3 run.py")
    print("2. 打包可执行文件：python3 build.py")
    print("3. 查看帮助：查看README.md文件")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n安装过程中遇到问题，请检查错误信息并重新运行安装程序。")
        sys.exit(1)
    else:
        print("\n安装成功！现在可以使用AI城建系统了。")
        sys.exit(0)