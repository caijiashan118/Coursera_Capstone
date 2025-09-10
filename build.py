#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统打包脚本
使用PyInstaller将程序打包成可执行文件
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def create_spec_file():
    """创建PyInstaller的spec文件"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('assets', 'assets'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'pandas',
        'openpyxl',
        'matplotlib',
        'sqlite3',
        'numpy',
        'plotly'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AI城建系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'
)
"""
    
    with open('AI城建系统.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

def create_icon():
    """创建简单的图标文件"""
    # 这里创建一个简单的文本图标说明
    icon_info = """
图标文件说明：
由于无法直接生成.ico文件，请手动创建或下载一个合适的图标文件，
命名为icon.ico，放置在assets目录下。

建议图标尺寸：32x32, 48x48, 64x64像素
"""
    
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    with open(assets_dir / "icon_readme.txt", 'w', encoding='utf-8') as f:
        f.write(icon_info)

def build_executable():
    """构建可执行文件"""
    try:
        print("开始构建AI城建系统...")
        
        # 创建图标说明
        create_icon()
        
        # 创建spec文件
        create_spec_file()
        
        # 运行PyInstaller
        print("正在打包程序...")
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--windowed',
            '--name', 'AI城建系统',
            '--distpath', 'dist',
            '--workpath', 'build',
            '--specpath', '.',
            'main.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 程序打包成功！")
            print(f"可执行文件位置：{Path('dist').absolute()}")
            
            # 创建桌面快捷方式说明
            create_desktop_shortcut_info()
            
        else:
            print("✗ 打包失败！")
            print("错误信息：", result.stderr)
            
    except Exception as e:
        print(f"构建过程中出现错误：{e}")

def create_desktop_shortcut_info():
    """创建桌面快捷方式说明"""
    shortcut_info = """
桌面快捷方式创建说明：

Windows系统：
1. 右键点击dist目录下的"AI城建系统.exe"文件
2. 选择"发送到" -> "桌面快捷方式"
3. 或者复制exe文件到桌面，然后重命名为"AI城建系统"

Linux系统：
1. 创建desktop文件：
   [Desktop Entry]
   Name=AI城建系统
   Comment=AI城建系统 - 智能城市建设管理平台
   Exec=/path/to/AI城建系统
   Icon=/path/to/icon.png
   Terminal=false
   Type=Application
   Categories=Office;

2. 保存为AI城建系统.desktop，放置在桌面或/usr/share/applications/

macOS系统：
1. 将应用程序拖拽到桌面即可创建快捷方式
"""
    
    with open('desktop_shortcut_guide.txt', 'w', encoding='utf-8') as f:
        f.write(shortcut_info)
        
    print("✓ 桌面快捷方式创建说明已生成：desktop_shortcut_guide.txt")

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ['build', '__pycache__']
    files_to_clean = ['AI城建系统.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 已清理：{dir_name}")
            
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✓ 已清理：{file_name}")

if __name__ == "__main__":
    print("AI城建系统构建工具")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
    else:
        build_executable()
        
    print("=" * 50)
    print("构建完成！")