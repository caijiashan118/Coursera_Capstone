#!/usr/bin/env python3
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
    traceback.print_exc()