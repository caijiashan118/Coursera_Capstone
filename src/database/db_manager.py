# -*- coding: utf-8 -*-
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_code) REFERENCES project_basic_info (project_code)
                )
            ''')
            
            # 创建重点项目清单表
            cursor.execute('''
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
            ''')
            
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
            
    def insert_funding_arrangement(self, data):
        """插入资金安排信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
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
            
    def get_project_by_code(self, project_code):
        """根据项目编码获取项目信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM project_basic_info WHERE project_code = ?", (project_code,))
            return cursor.fetchone()
        finally:
            conn.close()
            
    def update_project_basic_info(self, project_code, data):
        """更新项目基本信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE project_basic_info 
                SET project_name=?, construction_unit=?, supervising_department=?, 
                    approval_date=?, budget_amount=?, planned_start_date=?, planned_end_date=?, 
                    project_status=?, updated_at=CURRENT_TIMESTAMP
                WHERE project_code=?
            ''', (*data, project_code))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def delete_project(self, project_code):
        """删除项目（包括相关的资金安排）"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 先删除相关的资金安排
            cursor.execute("DELETE FROM funding_arrangement WHERE project_code = ?", (project_code,))
            cursor.execute("DELETE FROM key_projects_list WHERE project_code = ?", (project_code,))
            # 再删除项目基本信息
            cursor.execute("DELETE FROM project_basic_info WHERE project_code = ?", (project_code,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def get_funding_pivot_table(self):
        """获取资金安排数据透视表"""
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
            conn.close()