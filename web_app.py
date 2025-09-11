#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统 - Web版本
基于Flask的在线版本
"""

from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
import json
import os
from datetime import datetime, date
import random
from pathlib import Path
import plotly.graph_objs as go
import plotly.utils
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'ai_urban_construction_system_2024'

# 数据库路径
DB_PATH = 'data/urban_construction_web.db'

class WebDatabaseManager:
    """Web版数据库管理器"""
    
    def __init__(self):
        self.db_path = DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """初始化数据库"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 创建项目基本信息表
            cursor.execute('''
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建资金安排表
            cursor.execute('''
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"数据库初始化失败：{e}")
        finally:
            conn.close()
    
    def get_projects(self):
        """获取所有项目"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM project_basic_info ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_funding(self):
        """获取所有资金安排"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM funding_arrangement ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            conn.close()
    
    def add_project(self, data):
        """添加项目"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO project_basic_info 
                (project_name, project_code, construction_unit, supervising_department,
                 approval_date, budget_amount, planned_start_date, planned_end_date, project_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def add_funding(self, data):
        """添加资金安排"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO funding_arrangement 
                (project_name, project_code, construction_unit, supervising_department,
                 budget_amount, funding_amount, approval_date, funding_type, operator, operating_department)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_statistics(self):
        """获取统计数据"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # 项目统计
            cursor.execute("SELECT COUNT(*) FROM project_basic_info")
            total_projects = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(budget_amount) FROM project_basic_info")
            total_budget = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT project_status, COUNT(*) FROM project_basic_info GROUP BY project_status")
            status_stats = dict(cursor.fetchall())
            
            # 资金统计
            cursor.execute("SELECT COUNT(*) FROM funding_arrangement")
            total_funding_records = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(funding_amount) FROM funding_arrangement")
            total_funding = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT funding_type, COUNT(*) FROM funding_arrangement GROUP BY funding_type")
            funding_type_stats = dict(cursor.fetchall())
            
            return {
                'total_projects': total_projects,
                'total_budget': total_budget,
                'total_funding_records': total_funding_records,
                'total_funding': total_funding,
                'status_stats': status_stats,
                'funding_type_stats': funding_type_stats
            }
        finally:
            conn.close()
    
    def get_pivot_data(self):
        """获取透视表数据"""
        conn = self.get_connection()
        try:
            query = '''
                SELECT 
                    project_code,
                    project_name,
                    funding_type,
                    SUM(funding_amount) as total_funding
                FROM funding_arrangement 
                GROUP BY project_code, project_name, funding_type
                ORDER BY project_code
            '''
            df = pd.read_sql_query(query, conn)
            
            if df.empty:
                return []
            
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
            
            # 转换为字典格式
            result = []
            for (project_code, project_name), row in pivot_df.iterrows():
                item = {
                    'project_code': project_code,
                    'project_name': project_name
                }
                for col in pivot_df.columns:
                    item[col] = float(row[col]) if pd.notna(row[col]) else 0
                result.append(item)
            
            return result
        finally:
            conn.close()

# 初始化数据库管理器
db_manager = WebDatabaseManager()

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
    
    def generate_mock_data(self, project_count=50, funding_count=200):
        """生成模拟数据"""
        projects = []
        
        # 生成项目数据
        for i in range(1, project_count + 1):
            project_code = f"WEB{datetime.now().year}{i:04d}"
            project_name = self.generate_project_name(i)
            budget_amount = random.uniform(500, 20000)
            
            # 生成日期
            approval_date = datetime.now().date()
            start_date = approval_date
            end_date = start_date
            
            project_data = (
                project_name, project_code, 
                random.choice(self.construction_units),
                random.choice(self.supervising_departments),
                approval_date, budget_amount, start_date, end_date,
                random.choice(self.project_statuses)
            )
            
            db_manager.add_project(project_data)
            projects.append({
                'code': project_code,
                'name': project_name,
                'budget': budget_amount
            })
        
        # 生成资金安排数据
        for i in range(funding_count):
            project = random.choice(projects)
            funding_amount = random.uniform(project['budget'] * 0.1, project['budget'] * 0.8)
            
            funding_data = (
                project['name'], project['code'],
                random.choice(self.construction_units),
                random.choice(self.supervising_departments),
                project['budget'], funding_amount,
                datetime.now().date(),
                random.choice(self.funding_types),
                random.choice(self.operators),
                random.choice(self.operating_departments)
            )
            
            db_manager.add_funding(funding_data)
    
    def generate_project_name(self, index):
        """生成项目名称"""
        project_types = [
            '道路建设工程', '桥梁建设工程', '排水管网工程', '公园绿化工程', '学校建设工程',
            '医院建设工程', '住宅小区建设', '商业综合体', '地铁建设工程', '污水处理厂'
        ]
        areas = ['东城区', '西城区', '南城区', '北城区', '中心区', '开发区']
        
        project_type = random.choice(project_types)
        area = random.choice(areas)
        return f"{area}{project_type}第{index}期"

mock_generator = MockDataGenerator()

# 路由定义
@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/api/statistics')
def get_statistics():
    """获取统计数据"""
    try:
        stats = db_manager.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/projects')
def get_projects():
    """获取项目列表"""
    try:
        projects = db_manager.get_projects()
        project_list = []
        for project in projects:
            project_list.append({
                'id': project['id'],
                'project_name': project['project_name'],
                'project_code': project['project_code'],
                'construction_unit': project['construction_unit'],
                'supervising_department': project['supervising_department'],
                'approval_date': project['approval_date'],
                'budget_amount': project['budget_amount'],
                'planned_start_date': project['planned_start_date'],
                'planned_end_date': project['planned_end_date'],
                'project_status': project['project_status']
            })
        
        return jsonify({
            'success': True,
            'data': project_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/funding')
def get_funding():
    """获取资金安排列表"""
    try:
        funding = db_manager.get_funding()
        funding_list = []
        for fund in funding:
            funding_list.append({
                'id': fund['id'],
                'project_name': fund['project_name'],
                'project_code': fund['project_code'],
                'construction_unit': fund['construction_unit'],
                'supervising_department': fund['supervising_department'],
                'budget_amount': fund['budget_amount'],
                'funding_amount': fund['funding_amount'],
                'approval_date': fund['approval_date'],
                'funding_type': fund['funding_type'],
                'operator': fund['operator'],
                'operating_department': fund['operating_department']
            })
        
        return jsonify({
            'success': True,
            'data': funding_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/pivot')
def get_pivot():
    """获取透视表数据"""
    try:
        pivot_data = db_manager.get_pivot_data()
        return jsonify({
            'success': True,
            'data': pivot_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/generate_mock_data', methods=['POST'])
def generate_mock_data():
    """生成模拟数据"""
    try:
        mock_generator.generate_mock_data(50, 200)
        return jsonify({
            'success': True,
            'message': '模拟数据生成成功！生成了50个项目和200条资金安排记录。'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/add_project', methods=['POST'])
def add_project():
    """添加项目"""
    try:
        data = request.json
        project_data = (
            data['project_name'],
            data['project_code'],
            data['construction_unit'],
            data['supervising_department'],
            data['approval_date'],
            float(data['budget_amount']),
            data['planned_start_date'],
            data['planned_end_date'],
            data['project_status']
        )
        
        project_id = db_manager.add_project(project_data)
        return jsonify({
            'success': True,
            'message': '项目添加成功',
            'id': project_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/add_funding', methods=['POST'])
def add_funding():
    """添加资金安排"""
    try:
        data = request.json
        funding_data = (
            data['project_name'],
            data['project_code'],
            data['construction_unit'],
            data['supervising_department'],
            float(data['budget_amount']),
            float(data['funding_amount']),
            data['approval_date'],
            data['funding_type'],
            data['operator'],
            data['operating_department']
        )
        
        funding_id = db_manager.add_funding(funding_data)
        return jsonify({
            'success': True,
            'message': '资金安排添加成功',
            'id': funding_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/chart_data/<chart_type>')
def get_chart_data(chart_type):
    """获取图表数据"""
    try:
        if chart_type == 'project_status':
            stats = db_manager.get_statistics()
            return jsonify({
                'success': True,
                'data': stats['status_stats']
            })
        elif chart_type == 'funding_type':
            stats = db_manager.get_statistics()
            return jsonify({
                'success': True,
                'data': stats['funding_type_stats']
            })
        else:
            return jsonify({
                'success': False,
                'error': '不支持的图表类型'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # 创建模板目录
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)