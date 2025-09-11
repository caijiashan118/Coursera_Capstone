# AI城建系统完整安装指南

## 🏗️ 第一步：创建项目目录结构

### Windows系统：
```cmd
mkdir AI城建系统
cd AI城建系统
mkdir src
mkdir src\database
mkdir src\gui  
mkdir src\models
mkdir src\utils
mkdir assets
mkdir data
```

### Linux/macOS系统：
```bash
mkdir AI城建系统
cd AI城建系统
mkdir -p src/database src/gui src/models src/utils assets data
```

## 📁 第二步：目录结构确认

创建完成后，您的目录结构应该是：
```
AI城建系统/
├── src/
│   ├── database/
│   ├── gui/
│   ├── models/
│   └── utils/
├── assets/
└── data/
```

## 📄 第三步：创建文件

按照以下顺序创建所有文件：

### 1. 根目录文件
- requirements.txt
- main.py
- run.py
- install.py
- build.py
- test_system.py
- start.sh (Linux/macOS)
- start.bat (Windows)
- README.md

### 2. src目录文件
- src/__init__.py
- src/database/__init__.py
- src/database/db_manager.py
- src/gui/__init__.py
- src/gui/main_window.py
- src/gui/basic_data_module.py
- src/gui/visualization_module.py
- src/gui/report_module.py
- src/models/__init__.py
- src/models/project_models.py
- src/utils/__init__.py
- src/utils/excel_handler.py

## 🚀 第四步：安装依赖

### 方法1：自动安装（推荐）
```bash
python install.py
```

### 方法2：手动安装
```bash
pip install -r requirements.txt
```

### 方法3：逐个安装
```bash
pip install pandas openpyxl matplotlib numpy python-dateutil pyinstaller
```

## 🎯 第五步：运行程序

### 方法1：直接运行
```bash
python main.py
```

### 方法2：使用启动脚本
```bash
python run.py
```

### 方法3：使用系统脚本
```bash
# Linux/macOS
./start.sh

# Windows
start.bat
```

## 🧪 第六步：测试系统

运行测试脚本确认所有功能正常：
```bash
python test_system.py
```

## 📦 第七步：打包可执行文件（可选）

如果需要生成独立的exe文件：
```bash
python build.py
```

## ❗ 常见问题解决

### 问题1：缺少tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL  
sudo yum install tkinter
```

### 问题2：权限错误
```bash
# 给脚本添加执行权限
chmod +x start.sh
```

### 问题3：编码错误
确保所有Python文件都使用UTF-8编码保存。

## 🎉 安装完成！

安装成功后，您可以：
1. 生成200个模拟项目数据
2. 创建1000条资金安排记录
3. 使用8种可视化图表
4. 生成8种智慧报表
5. Excel数据导入导出
6. 数据透视表分析

享受使用AI城建系统！