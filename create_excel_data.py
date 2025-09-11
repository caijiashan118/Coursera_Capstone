#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统 - Excel数据文件生成器
生成包含基础数据、数据可视化、智慧报表的完整Excel文件
"""

import pandas as pd
import random
from datetime import datetime, timedelta, date
import os

class ExcelDataGenerator:
    """Excel数据生成器"""
    
    def __init__(self):
        self.project_statuses = ['在建', '续建', '完工', '暂停']
        self.funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助']
        
        # 基础数据
        self.construction_units = [
            '市政建设集团有限公司', '城市投资建设集团', '交通建设发展集团', '水务建设集团公司',
            '园林绿化建设集团', '教育建设投资公司', '医疗建设发展公司', '住房建设集团',
            '基础设施建设公司', '公共设施建设集团', '环保建设投资公司', '文化建设集团'
        ]
        
        self.supervising_departments = [
            '市发展和改革委员会', '市住房和城乡建设局', '市交通运输局', '市水利局',
            '市教育局', '市卫生健康委员会', '市生态环境局', '市园林绿化局',
            '市城市管理局', '市规划和自然资源局', '市文化和旅游局', '市体育局'
        ]
        
        self.operators = [
            '张建华', '李明强', '王志远', '赵文博', '钱国强', '孙海涛', '周建军', '吴德华',
            '陈志刚', '刘建国', '杨文华', '黄志明', '朱建平', '林志强', '马建设', '徐文军',
            '郭建华', '何志远', '高建国', '梁文博', '韩志刚', '曹建军', '邓文华', '彭志明'
        ]
        
        self.operating_departments = [
            '计划财务处', '项目管理处', '投资建设处', '资金管理处', '审计监察处',
            '工程建设处', '规划设计处', '招投标管理处', '质量安全处', '综合管理处'
        ]
        
        self.project_types = [
            '道路建设工程', '桥梁建设工程', '隧道建设工程', '排水管网工程', '供水管网工程',
            '公园绿化工程', '广场建设工程', '学校建设工程', '医院建设工程', '住宅小区建设',
            '商业综合体建设', '地铁建设工程', '公交站台建设', '污水处理厂建设', '垃圾处理中心建设',
            '体育中心建设', '文化中心建设', '图书馆建设', '博物馆建设', '停车场建设',
            '充电桩建设', '路灯照明工程', '景观亮化工程', '河道治理工程', '山体修复工程'
        ]
        
        self.areas = [
            '东城区', '西城区', '南城区', '北城区', '中心区', '开发区', '新区', '高新区',
            '经济技术开发区', '生态城区', '滨海新区', '山区', '工业园区', '科技园区'
        ]
    
    def generate_project_code(self, index):
        """生成项目编码"""
        year = datetime.now().year
        return f"UC{year}{index:04d}"
    
    def generate_project_name(self, index):
        """生成项目名称"""
        area = random.choice(self.areas)
        project_type = random.choice(self.project_types)
        phase = random.choice(['一期', '二期', '三期', '四期', '五期'])
        return f"{area}{project_type}{phase}"
    
    def generate_random_date(self, start_date, end_date):
        """生成随机日期"""
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    def create_project_basic_info(self, count=200):
        """创建项目基本信息表"""
        projects = []
        
        for i in range(1, count + 1):
            project_code = self.generate_project_code(i)
            project_name = self.generate_project_name(i)
            
            # 随机生成概算批复金额（500-20000万元）
            budget_amount = round(random.uniform(500, 20000), 2)
            
            # 随机生成日期
            base_date = datetime(2023, 1, 1)
            end_date = datetime(2024, 12, 31)
            
            approval_date = self.generate_random_date(base_date, datetime(2024, 6, 30))
            planned_start_date = approval_date + timedelta(days=random.randint(30, 180))
            planned_end_date = planned_start_date + timedelta(days=random.randint(180, 1095))
            
            project = {
                '项目名称': project_name,
                '项目编码': project_code,
                '建设单位': random.choice(self.construction_units),
                '项目主管部门': random.choice(self.supervising_departments),
                '立项时间': approval_date.strftime('%Y-%m-%d'),
                '概算批复金额': budget_amount,
                '预计开工时间': planned_start_date.strftime('%Y-%m-%d'),
                '预计完工时间': planned_end_date.strftime('%Y-%m-%d'),
                '项目状态': random.choice(self.project_statuses)
            }
            
            projects.append(project)
        
        return pd.DataFrame(projects)
    
    def create_funding_arrangement(self, projects_df, count=1000):
        """创建资金安排表"""
        funding_records = []
        projects_list = projects_df.to_dict('records')
        
        # 确保每个项目至少有一条资金安排
        for project in projects_list:
            funding_amount = round(random.uniform(project['概算批复金额'] * 0.1, project['概算批复金额'] * 0.8), 2)
            approval_date = datetime.strptime(project['立项时间'], '%Y-%m-%d')
            funding_approval_date = approval_date + timedelta(days=random.randint(1, 90))
            
            funding = {
                '项目名称': project['项目名称'],
                '项目编码': project['项目编码'],
                '建设单位': project['建设单位'],
                '项目主管部门': project['项目主管部门'],
                '概算批复金额': project['概算批复金额'],
                '资金批复金额': funding_amount,
                '批复日期': funding_approval_date.strftime('%Y-%m-%d'),
                '资金性质': random.choice(self.funding_types),
                '经办人': random.choice(self.operators),
                '经办处室': random.choice(self.operating_departments)
            }
            
            funding_records.append(funding)
        
        # 生成剩余的资金安排记录
        remaining_count = count - len(projects_list)
        for _ in range(remaining_count):
            project = random.choice(projects_list)
            funding_amount = round(random.uniform(project['概算批复金额'] * 0.05, project['概算批复金额'] * 0.5), 2)
            approval_date = datetime.strptime(project['立项时间'], '%Y-%m-%d')
            funding_approval_date = approval_date + timedelta(days=random.randint(1, 365))
            
            funding = {
                '项目名称': project['项目名称'],
                '项目编码': project['项目编码'],
                '建设单位': project['建设单位'],
                '项目主管部门': project['项目主管部门'],
                '概算批复金额': project['概算批复金额'],
                '资金批复金额': funding_amount,
                '批复日期': funding_approval_date.strftime('%Y-%m-%d'),
                '资金性质': random.choice(self.funding_types),
                '经办人': random.choice(self.operators),
                '经办处室': random.choice(self.operating_departments)
            }
            
            funding_records.append(funding)
        
        return pd.DataFrame(funding_records)
    
    def create_key_projects_list(self, projects_df):
        """创建重点项目清单表"""
        # 随机选择30%的项目作为重点项目
        key_projects_count = int(len(projects_df) * 0.3)
        key_projects_sample = projects_df.sample(n=key_projects_count)
        
        key_projects = []
        priority_levels = [1, 2, 3]  # 1-最高优先级，3-一般优先级
        key_features_options = [
            '重大民生工程', '基础设施建设', '生态环保项目', '科技创新项目', 
            '文化教育项目', '医疗卫生项目', '交通枢纽工程', '城市更新项目',
            '产业发展项目', '智慧城市建设', '绿色低碳项目', '乡村振兴项目'
        ]
        strategic_importance_options = [
            '提升城市综合承载能力', '改善民生福祉', '促进经济高质量发展',
            '推动生态文明建设', '增强城市竞争力', '完善基础设施体系',
            '提高公共服务水平', '优化城市空间布局', '推进新型城镇化建设',
            '支撑产业转型升级'
        ]
        
        for _, project in key_projects_sample.iterrows():
            key_project = {
                '项目编码': project['项目编码'],
                '项目名称': project['项目名称'],
                '优先级': random.choice(priority_levels),
                '关键特征': random.choice(key_features_options),
                '战略重要性': random.choice(strategic_importance_options)
            }
            key_projects.append(key_project)
        
        return pd.DataFrame(key_projects)
    
    def create_data_visualization_sheet(self, projects_df, funding_df):
        """创建数据可视化工作表"""
        # 项目状态统计
        status_stats = projects_df['项目状态'].value_counts()
        
        # 资金性质统计
        funding_type_stats = funding_df['资金性质'].value_counts()
        
        # 部门项目统计
        department_stats = projects_df['项目主管部门'].value_counts()
        
        # 概算金额分布统计
        budget_ranges = ['500-2000万', '2000-5000万', '5000-10000万', '10000-15000万', '15000-20000万']
        budget_distribution = {range_name: 0 for range_name in budget_ranges}
        
        for budget in projects_df['概算批复金额']:
            if budget <= 2000:
                budget_distribution['500-2000万'] += 1
            elif budget <= 5000:
                budget_distribution['2000-5000万'] += 1
            elif budget <= 10000:
                budget_distribution['5000-10000万'] += 1
            elif budget <= 15000:
                budget_distribution['10000-15000万'] += 1
            else:
                budget_distribution['15000-20000万'] += 1
        
        # 创建可视化数据表
        viz_data = []
        
        # 项目状态分布
        viz_data.append(['图表类型', '项目状态分布图（饼图）', '', ''])
        viz_data.append(['状态', '数量', '占比', ''])
        for status, count in status_stats.items():
            percentage = f"{count/len(projects_df)*100:.1f}%"
            viz_data.append([status, count, percentage, ''])
        viz_data.append(['', '', '', ''])
        
        # 资金性质分布
        viz_data.append(['图表类型', '资金性质分析图（条形图）', '', ''])
        viz_data.append(['资金性质', '金额(万元)', '笔数', ''])
        for funding_type, count in funding_type_stats.items():
            amount = funding_df[funding_df['资金性质'] == funding_type]['资金批复金额'].sum()
            viz_data.append([funding_type, f"{amount:.2f}", count, ''])
        viz_data.append(['', '', '', ''])
        
        # 概算金额分布
        viz_data.append(['图表类型', '概算金额分布图（直方图）', '', ''])
        viz_data.append(['金额范围', '项目数量', '', ''])
        for range_name, count in budget_distribution.items():
            viz_data.append([range_name, count, '', ''])
        
        return pd.DataFrame(viz_data, columns=['指标', '数值1', '数值2', '备注'])
    
    def create_smart_reports_sheet(self, projects_df, funding_df, key_projects_df):
        """创建智慧报表生成工作表"""
        reports_data = []
        
        # 报表1：项目总览报表
        reports_data.append(['报表类型', '项目总览报表', '', '', ''])
        reports_data.append(['统计项', '数值', '单位', '占比', '备注'])
        
        total_projects = len(projects_df)
        total_budget = projects_df['概算批复金额'].sum()
        avg_budget = projects_df['概算批复金额'].mean()
        
        reports_data.append(['项目总数', total_projects, '个', '100%', ''])
        reports_data.append(['概算总额', f"{total_budget:.2f}", '万元', '100%', ''])
        reports_data.append(['平均概算', f"{avg_budget:.2f}", '万元', '', ''])
        reports_data.append(['重点项目数', len(key_projects_df), '个', f"{len(key_projects_df)/total_projects*100:.1f}%", ''])
        reports_data.append(['', '', '', '', ''])
        
        # 报表2：资金安排报表
        reports_data.append(['报表类型', '资金安排报表', '', '', ''])
        reports_data.append(['统计项', '数值', '单位', '占比', '备注'])
        
        total_funding_records = len(funding_df)
        total_funding_amount = funding_df['资金批复金额'].sum()
        avg_funding = funding_df['资金批复金额'].mean()
        
        reports_data.append(['资金安排笔数', total_funding_records, '笔', '100%', ''])
        reports_data.append(['资金安排总额', f"{total_funding_amount:.2f}", '万元', '100%', ''])
        reports_data.append(['平均资金金额', f"{avg_funding:.2f}", '万元', '', ''])
        reports_data.append(['', '', '', '', ''])
        
        # 报表3：债券资金专项报表
        reports_data.append(['报表类型', '债券资金专项报表', '', '', ''])
        reports_data.append(['债券类型', '金额(万元)', '笔数', '占比', '备注'])
        
        general_bonds = funding_df[funding_df['资金性质'] == '一般债券']['资金批复金额'].sum()
        special_bonds = funding_df[funding_df['资金性质'] == '专项债券']['资金批复金额'].sum()
        total_bonds = general_bonds + special_bonds
        
        general_count = len(funding_df[funding_df['资金性质'] == '一般债券'])
        special_count = len(funding_df[funding_df['资金性质'] == '专项债券'])
        
        reports_data.append(['一般债券', f"{general_bonds:.2f}", general_count, f"{general_bonds/total_bonds*100:.1f}%" if total_bonds > 0 else '0%', ''])
        reports_data.append(['专项债券', f"{special_bonds:.2f}", special_count, f"{special_bonds/total_bonds*100:.1f}%" if total_bonds > 0 else '0%', ''])
        reports_data.append(['债券资金合计', f"{total_bonds:.2f}", general_count + special_count, '100%', '重点统计项'])
        reports_data.append(['', '', '', '', ''])
        
        # 报表4：部门统计报表
        reports_data.append(['报表类型', '部门统计报表', '', '', ''])
        reports_data.append(['主管部门', '项目数量', '概算总额(万元)', '资金安排总额(万元)', '备注'])
        
        for dept in projects_df['项目主管部门'].unique():
            dept_projects = projects_df[projects_df['项目主管部门'] == dept]
            dept_funding = funding_df[funding_df['项目主管部门'] == dept]
            
            project_count = len(dept_projects)
            dept_budget = dept_projects['概算批复金额'].sum()
            dept_funding_amount = dept_funding['资金批复金额'].sum()
            
            reports_data.append([dept, project_count, f"{dept_budget:.2f}", f"{dept_funding_amount:.2f}", ''])
        
        return pd.DataFrame(reports_data, columns=['项目', '指标1', '指标2', '指标3', '说明'])
    
    def create_pivot_analysis(self, funding_df):
        """创建数据透视分析表"""
        # 按项目编码和资金性质创建透视表
        pivot_data = funding_df.groupby(['项目编码', '项目名称', '资金性质'])['资金批复金额'].sum().unstack(fill_value=0)
        
        # 计算债券资金合计
        bond_columns = ['一般债券', '专项债券']
        available_bond_columns = [col for col in bond_columns if col in pivot_data.columns]
        
        if available_bond_columns:
            pivot_data['债券资金合计'] = pivot_data[available_bond_columns].sum(axis=1)
        
        # 重置索引
        pivot_data = pivot_data.reset_index()
        
        return pivot_data
    
    def generate_excel_file(self, filename='AI城建系统数据.xlsx'):
        """生成完整的Excel文件"""
        print("🏗️ 开始生成AI城建系统Excel数据文件...")
        
        # 生成基础数据
        print("📊 生成项目基本信息表（200个项目）...")
        projects_df = self.create_project_basic_info(200)
        
        print("💰 生成资金安排表（1000条记录）...")
        funding_df = self.create_funding_arrangement(projects_df, 1000)
        
        print("⭐ 生成重点项目清单表...")
        key_projects_df = self.create_key_projects_list(projects_df)
        
        print("📈 生成数据可视化分析...")
        visualization_df = self.create_data_visualization_sheet(projects_df, funding_df)
        
        print("📋 生成智慧报表数据...")
        reports_df = self.create_smart_reports_sheet(projects_df, funding_df, key_projects_df)
        
        print("🔄 生成数据透视表...")
        pivot_df = self.create_pivot_analysis(funding_df)
        
        # 创建Excel文件
        print("📁 创建Excel文件...")
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 基础数据工作表
            projects_df.to_excel(writer, sheet_name='项目基本信息表', index=False)
            funding_df.to_excel(writer, sheet_name='资金安排表', index=False)
            key_projects_df.to_excel(writer, sheet_name='重点项目清单', index=False)
            
            # 数据可视化工作表
            visualization_df.to_excel(writer, sheet_name='数据可视化', index=False)
            
            # 智慧报表工作表
            reports_df.to_excel(writer, sheet_name='智慧报表生成', index=False)
            
            # 数据透视表工作表
            pivot_df.to_excel(writer, sheet_name='数据透视表', index=False)
            
            # 设置列宽
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
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
        
        print("✅ Excel文件生成完成！")
        print(f"📄 文件名：{filename}")
        print(f"📊 包含工作表：")
        print(f"   • 项目基本信息表：{len(projects_df)} 条记录")
        print(f"   • 资金安排表：{len(funding_df)} 条记录")
        print(f"   • 重点项目清单：{len(key_projects_df)} 条记录")
        print(f"   • 数据可视化：图表数据分析")
        print(f"   • 智慧报表生成：多维度统计报表")
        print(f"   • 数据透视表：债券资金合计分析")
        
        return filename

def main():
    """主函数"""
    generator = ExcelDataGenerator()
    filename = generator.generate_excel_file()
    
    print("\n🎉 AI城建系统Excel数据文件生成完成！")
    print(f"📍 文件位置：{os.path.abspath(filename)}")
    print("\n📋 文件内容说明：")
    print("1. 项目基本信息表 - 200个模拟项目，概算金额500-20000万元")
    print("2. 资金安排表 - 1000条资金安排，通过项目编码关联")
    print("3. 重点项目清单 - 约60个重点项目（30%比例）")
    print("4. 数据可视化 - 图表数据和统计分析")
    print("5. 智慧报表生成 - 多种专业报表数据")
    print("6. 数据透视表 - 债券资金合计分析")
    print("\n💡 可以直接在Excel中打开使用，支持数据筛选、排序、图表制作等功能")

if __name__ == "__main__":
    main()