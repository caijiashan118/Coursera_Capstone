# -*- coding: utf-8 -*-
"""
Excel文件处理工具
"""

import pandas as pd
import openpyxl
from datetime import datetime, date
from pathlib import Path

class ExcelHandler:
    """Excel文件处理器"""
    
    def __init__(self):
        pass
        
    def import_project_data(self, file_path, db_manager):
        """从Excel导入项目基本信息数据"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 验证必要的列是否存在
            required_columns = ['项目名称', '项目编码', '建设单位', '项目主管部门', 
                              '概算批复金额', '项目状态']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Excel文件缺少必要的列：{missing_columns}")
                
            # 处理数据并插入数据库
            for _, row in df.iterrows():
                # 处理日期字段
                approval_date = self._parse_date(row.get('立项时间'))
                start_date = self._parse_date(row.get('预计开工时间'))
                end_date = self._parse_date(row.get('预计完工时间'))
                
                # 验证项目状态
                status = str(row['项目状态']).strip()
                if status not in ['在建', '续建', '完工', '暂停']:
                    raise ValueError(f"无效的项目状态：{status}")
                
                data = (
                    str(row['项目名称']).strip(),
                    str(row['项目编码']).strip(),
                    str(row['建设单位']).strip(),
                    str(row['项目主管部门']).strip(),
                    approval_date,
                    float(row['概算批复金额']),
                    start_date,
                    end_date,
                    status
                )
                
                db_manager.insert_project_basic_info(data)
                
        except Exception as e:
            raise Exception(f"导入项目数据失败：{str(e)}")
            
    def import_funding_data(self, file_path, db_manager):
        """从Excel导入资金安排数据"""
        try:
            df = pd.read_excel(file_path)
            
            required_columns = ['项目名称', '项目编码', '建设单位', '项目主管部门',
                              '概算批复金额', '资金批复金额', '批复日期', '资金性质',
                              '经办人', '经办处室']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Excel文件缺少必要的列：{missing_columns}")
                
            valid_funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', 
                                 '中央预算内投资', '中央补助', '省级补助']
            
            for _, row in df.iterrows():
                # 验证资金性质
                funding_type = str(row['资金性质']).strip()
                if funding_type not in valid_funding_types:
                    raise ValueError(f"无效的资金性质：{funding_type}")
                
                # 处理日期
                approval_date = self._parse_date(row['批复日期'])
                if not approval_date:
                    raise ValueError(f"无效的批复日期：{row['批复日期']}")
                
                data = (
                    str(row['项目名称']).strip(),
                    str(row['项目编码']).strip(),
                    str(row['建设单位']).strip(),
                    str(row['项目主管部门']).strip(),
                    float(row['概算批复金额']),
                    float(row['资金批复金额']),
                    approval_date,
                    funding_type,
                    str(row['经办人']).strip(),
                    str(row['经办处室']).strip()
                )
                
                db_manager.insert_funding_arrangement(data)
                
        except Exception as e:
            raise Exception(f"导入资金安排数据失败：{str(e)}")
            
    def export_project_data(self, df, file_path):
        """导出项目基本信息数据到Excel"""
        try:
            # 重命名列以便于理解
            column_mapping = {
                'project_name': '项目名称',
                'project_code': '项目编码', 
                'construction_unit': '建设单位',
                'supervising_department': '项目主管部门',
                'approval_date': '立项时间',
                'budget_amount': '概算批复金额(万元)',
                'planned_start_date': '预计开工时间',
                'planned_end_date': '预计完工时间',
                'project_status': '项目状态'
            }
            
            # 选择需要导出的列
            export_columns = ['project_name', 'project_code', 'construction_unit', 
                            'supervising_department', 'approval_date', 'budget_amount',
                            'planned_start_date', 'planned_end_date', 'project_status']
            
            export_df = df[export_columns].copy()
            export_df.rename(columns=column_mapping, inplace=True)
            
            # 导出到Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                export_df.to_excel(writer, sheet_name='项目基本信息', index=False)
                
                # 设置列宽
                worksheet = writer.sheets['项目基本信息']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                    
        except Exception as e:
            raise Exception(f"导出项目数据失败：{str(e)}")
            
    def export_funding_data(self, df, file_path):
        """导出资金安排数据到Excel"""
        try:
            column_mapping = {
                'project_name': '项目名称',
                'project_code': '项目编码',
                'construction_unit': '建设单位', 
                'supervising_department': '项目主管部门',
                'budget_amount': '概算批复金额(万元)',
                'funding_amount': '资金批复金额(万元)',
                'approval_date': '批复日期',
                'funding_type': '资金性质',
                'operator': '经办人',
                'operating_department': '经办处室'
            }
            
            export_columns = ['project_name', 'project_code', 'construction_unit',
                            'supervising_department', 'budget_amount', 'funding_amount',
                            'approval_date', 'funding_type', 'operator', 'operating_department']
            
            export_df = df[export_columns].copy()
            export_df.rename(columns=column_mapping, inplace=True)
            
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                export_df.to_excel(writer, sheet_name='资金安排', index=False)
                
                # 设置列宽
                worksheet = writer.sheets['资金安排']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                    
        except Exception as e:
            raise Exception(f"导出资金安排数据失败：{str(e)}")
            
    def export_pivot_table(self, pivot_df, file_path):
        """导出数据透视表到Excel"""
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                pivot_df.to_excel(writer, sheet_name='资金安排透视表', index=False)
                
                # 设置格式
                worksheet = writer.sheets['资金安排透视表']
                
                # 设置列宽
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                    
                # 设置数字格式（金额列）
                from openpyxl.styles import NamedStyle
                currency_style = NamedStyle(name="currency", number_format='#,##0.00"万元"')
                
                for row in worksheet.iter_rows(min_row=2):  # 跳过标题行
                    for cell in row[2:]:  # 跳过项目编码和项目名称列
                        if isinstance(cell.value, (int, float)):
                            cell.style = currency_style
                            
        except Exception as e:
            raise Exception(f"导出透视表失败：{str(e)}")
            
    def _parse_date(self, date_value):
        """解析日期值"""
        if pd.isna(date_value) or date_value is None:
            return None
            
        if isinstance(date_value, (date, datetime)):
            return date_value.date() if isinstance(date_value, datetime) else date_value
            
        # 尝试解析字符串日期
        try:
            if isinstance(date_value, str):
                date_value = date_value.strip()
                if not date_value:
                    return None
                    
                # 尝试多种日期格式
                date_formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日', '%m/%d/%Y']
                for fmt in date_formats:
                    try:
                        return datetime.strptime(date_value, fmt).date()
                    except ValueError:
                        continue
                        
            return None
            
        except Exception:
            return None
            
    def create_template_excel(self, file_path, template_type="project"):
        """创建Excel模板文件"""
        try:
            if template_type == "project":
                # 项目基本信息模板
                columns = ['项目名称', '项目编码', '建设单位', '项目主管部门', '立项时间',
                          '概算批复金额', '预计开工时间', '预计完工时间', '项目状态']
                
                # 创建示例数据
                sample_data = {
                    '项目名称': ['示例项目1', '示例项目2'],
                    '项目编码': ['UC20240001', 'UC20240002'],
                    '建设单位': ['市政建设集团', '城投建设公司'],
                    '项目主管部门': ['市发改委', '市住建局'],
                    '立项时间': ['2024-01-15', '2024-02-20'],
                    '概算批复金额': [5000.00, 8000.00],
                    '预计开工时间': ['2024-03-01', '2024-04-01'],
                    '预计完工时间': ['2025-12-31', '2026-06-30'],
                    '项目状态': ['在建', '续建']
                }
                
            elif template_type == "funding":
                # 资金安排模板
                columns = ['项目名称', '项目编码', '建设单位', '项目主管部门', '概算批复金额',
                          '资金批复金额', '批复日期', '资金性质', '经办人', '经办处室']
                
                sample_data = {
                    '项目名称': ['示例项目1', '示例项目1'],
                    '项目编码': ['UC20240001', 'UC20240001'],
                    '建设单位': ['市政建设集团', '市政建设集团'],
                    '项目主管部门': ['市发改委', '市发改委'],
                    '概算批复金额': [5000.00, 5000.00],
                    '资金批复金额': [2000.00, 1500.00],
                    '批复日期': ['2024-02-01', '2024-03-01'],
                    '资金性质': ['一般债券', '专项债券'],
                    '经办人': ['张三', '李四'],
                    '经办处室': ['计划财务处', '项目管理处']
                }
                
            df = pd.DataFrame(sample_data)
            df.to_excel(file_path, index=False)
            
        except Exception as e:
            raise Exception(f"创建模板文件失败：{str(e)}")