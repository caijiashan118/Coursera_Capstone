#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统 - Excel数据文件生成器（纯Python版本）
不依赖pandas，使用CSV格式生成数据文件
"""

import csv
import random
from datetime import datetime, timedelta
import os

class SimpleExcelDataGenerator:
    """简单Excel数据生成器"""
    
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
            '体育中心建设', '文化中心建设', '图书馆建设', '博物馆建设', '停车场建设'
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
        
        # 表头
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '立项时间',
            '概算批复金额', '预计开工时间', '预计完工时间', '项目状态'
        ]
        projects.append(headers)
        
        for i in range(1, count + 1):
            project_code = self.generate_project_code(i)
            project_name = self.generate_project_name(i)
            
            # 随机生成概算批复金额（500-20000万元）
            budget_amount = round(random.uniform(500, 20000), 2)
            
            # 随机生成日期
            base_date = datetime(2023, 1, 1)
            
            approval_date = self.generate_random_date(base_date, datetime(2024, 6, 30))
            planned_start_date = approval_date + timedelta(days=random.randint(30, 180))
            planned_end_date = planned_start_date + timedelta(days=random.randint(180, 1095))
            
            project_row = [
                project_name,
                project_code,
                random.choice(self.construction_units),
                random.choice(self.supervising_departments),
                approval_date.strftime('%Y-%m-%d'),
                budget_amount,
                planned_start_date.strftime('%Y-%m-%d'),
                planned_end_date.strftime('%Y-%m-%d'),
                random.choice(self.project_statuses)
            ]
            
            projects.append(project_row)
        
        return projects
    
    def create_funding_arrangement(self, projects_data, count=1000):
        """创建资金安排表"""
        funding_records = []
        
        # 表头
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '概算批复金额',
            '资金批复金额', '批复日期', '资金性质', '经办人', '经办处室'
        ]
        funding_records.append(headers)
        
        # 跳过表头，获取项目数据
        projects_list = projects_data[1:]
        
        # 确保每个项目至少有一条资金安排
        for project in projects_list:
            budget_amount = float(project[5])
            funding_amount = round(random.uniform(budget_amount * 0.1, budget_amount * 0.8), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_approval_date = approval_date + timedelta(days=random.randint(1, 90))
            
            funding_row = [
                project[0],  # 项目名称
                project[1],  # 项目编码
                project[2],  # 建设单位
                project[3],  # 项目主管部门
                budget_amount,  # 概算批复金额
                funding_amount,  # 资金批复金额
                funding_approval_date.strftime('%Y-%m-%d'),  # 批复日期
                random.choice(self.funding_types),  # 资金性质
                random.choice(self.operators),  # 经办人
                random.choice(self.operating_departments)  # 经办处室
            ]
            
            funding_records.append(funding_row)
        
        # 生成剩余的资金安排记录
        remaining_count = count - len(projects_list)
        for _ in range(remaining_count):
            project = random.choice(projects_list)
            budget_amount = float(project[5])
            funding_amount = round(random.uniform(budget_amount * 0.05, budget_amount * 0.5), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_approval_date = approval_date + timedelta(days=random.randint(1, 365))
            
            funding_row = [
                project[0],  # 项目名称
                project[1],  # 项目编码
                project[2],  # 建设单位
                project[3],  # 项目主管部门
                budget_amount,  # 概算批复金额
                funding_amount,  # 资金批复金额
                funding_approval_date.strftime('%Y-%m-%d'),  # 批复日期
                random.choice(self.funding_types),  # 资金性质
                random.choice(self.operators),  # 经办人
                random.choice(self.operating_departments)  # 经办处室
            ]
            
            funding_records.append(funding_row)
        
        return funding_records
    
    def create_key_projects_list(self, projects_data):
        """创建重点项目清单表"""
        key_projects = []
        
        # 表头
        headers = ['项目编码', '项目名称', '优先级', '关键特征', '战略重要性']
        key_projects.append(headers)
        
        # 随机选择30%的项目作为重点项目
        projects_list = projects_data[1:]  # 跳过表头
        key_projects_count = int(len(projects_list) * 0.3)
        key_projects_sample = random.sample(projects_list, key_projects_count)
        
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
        
        for project in key_projects_sample:
            key_project_row = [
                project[1],  # 项目编码
                project[0],  # 项目名称
                random.choice(priority_levels),  # 优先级
                random.choice(key_features_options),  # 关键特征
                random.choice(strategic_importance_options)  # 战略重要性
            ]
            key_projects.append(key_project_row)
        
        return key_projects
    
    def create_data_visualization_sheet(self, projects_data, funding_data):
        """创建数据可视化工作表"""
        viz_data = []
        
        # 表头
        headers = ['图表类型', '指标', '数值', '占比', '备注']
        viz_data.append(headers)
        
        # 项目状态统计
        projects_list = projects_data[1:]  # 跳过表头
        status_stats = {}
        for project in projects_list:
            status = project[8]  # 项目状态
            status_stats[status] = status_stats.get(status, 0) + 1
        
        viz_data.append(['项目状态分布图（饼图）', '', '', '', ''])
        for status, count in status_stats.items():
            percentage = f"{count/len(projects_list)*100:.1f}%"
            viz_data.append(['', status, count, percentage, ''])
        viz_data.append(['', '', '', '', ''])
        
        # 资金性质统计
        funding_list = funding_data[1:]  # 跳过表头
        funding_type_stats = {}
        funding_amount_stats = {}
        
        for funding in funding_list:
            funding_type = funding[7]  # 资金性质
            amount = float(funding[5])  # 资金批复金额
            
            funding_type_stats[funding_type] = funding_type_stats.get(funding_type, 0) + 1
            funding_amount_stats[funding_type] = funding_amount_stats.get(funding_type, 0) + amount
        
        viz_data.append(['资金性质分析图（条形图）', '', '', '', ''])
        for funding_type, count in funding_type_stats.items():
            amount = funding_amount_stats[funding_type]
            viz_data.append(['', funding_type, f"{amount:.2f}万元", f"{count}笔", ''])
        viz_data.append(['', '', '', '', ''])
        
        # 债券资金统计
        general_bonds = funding_amount_stats.get('一般债券', 0)
        special_bonds = funding_amount_stats.get('专项债券', 0)
        total_bonds = general_bonds + special_bonds
        
        viz_data.append(['债券资金统计图（堆叠图）', '', '', '', ''])
        viz_data.append(['', '一般债券', f"{general_bonds:.2f}万元", f"{general_bonds/total_bonds*100:.1f}%" if total_bonds > 0 else '0%', ''])
        viz_data.append(['', '专项债券', f"{special_bonds:.2f}万元", f"{special_bonds/total_bonds*100:.1f}%" if total_bonds > 0 else '0%', ''])
        viz_data.append(['', '债券资金合计', f"{total_bonds:.2f}万元", '100%', '重点统计项'])
        
        return viz_data
    
    def create_smart_reports_sheet(self, projects_data, funding_data, key_projects_data):
        """创建智慧报表生成工作表"""
        reports_data = []
        
        # 表头
        headers = ['报表类型', '统计项', '数值', '单位', '备注']
        reports_data.append(headers)
        
        projects_list = projects_data[1:]  # 跳过表头
        funding_list = funding_data[1:]  # 跳过表头
        key_projects_list = key_projects_data[1:]  # 跳过表头
        
        # 项目总览报表
        total_projects = len(projects_list)
        total_budget = sum(float(project[5]) for project in projects_list)
        avg_budget = total_budget / total_projects if total_projects > 0 else 0
        
        reports_data.append(['项目总览报表', '', '', '', ''])
        reports_data.append(['', '项目总数', total_projects, '个', ''])
        reports_data.append(['', '概算总额', f"{total_budget:.2f}", '万元', ''])
        reports_data.append(['', '平均概算', f"{avg_budget:.2f}", '万元', ''])
        reports_data.append(['', '重点项目数', len(key_projects_list), '个', ''])
        reports_data.append(['', '', '', '', ''])
        
        # 资金安排报表
        total_funding_records = len(funding_list)
        total_funding_amount = sum(float(funding[5]) for funding in funding_list)
        avg_funding = total_funding_amount / total_funding_records if total_funding_records > 0 else 0
        
        reports_data.append(['资金安排报表', '', '', '', ''])
        reports_data.append(['', '资金安排笔数', total_funding_records, '笔', ''])
        reports_data.append(['', '资金安排总额', f"{total_funding_amount:.2f}", '万元', ''])
        reports_data.append(['', '平均资金金额', f"{avg_funding:.2f}", '万元', ''])
        reports_data.append(['', '', '', '', ''])
        
        # 债券资金专项报表
        general_bonds = sum(float(funding[5]) for funding in funding_list if funding[7] == '一般债券')
        special_bonds = sum(float(funding[5]) for funding in funding_list if funding[7] == '专项债券')
        total_bonds = general_bonds + special_bonds
        
        reports_data.append(['债券资金专项报表', '', '', '', ''])
        reports_data.append(['', '一般债券', f"{general_bonds:.2f}", '万元', ''])
        reports_data.append(['', '专项债券', f"{special_bonds:.2f}", '万元', ''])
        reports_data.append(['', '债券资金合计', f"{total_bonds:.2f}", '万元', '重点统计项'])
        
        return reports_data
    
    def create_pivot_analysis(self, funding_data):
        """创建数据透视分析表"""
        pivot_data = []
        
        # 表头
        headers = ['项目编码', '项目名称', '一般债券', '专项债券', '债券资金合计', '其他资金', '资金总计']
        pivot_data.append(headers)
        
        funding_list = funding_data[1:]  # 跳过表头
        
        # 按项目编码分组统计
        project_funding = {}
        
        for funding in funding_list:
            project_code = funding[1]
            project_name = funding[0]
            funding_type = funding[7]
            amount = float(funding[5])
            
            if project_code not in project_funding:
                project_funding[project_code] = {
                    'name': project_name,
                    '一般债券': 0,
                    '专项债券': 0,
                    '其他资金': 0
                }
            
            if funding_type == '一般债券':
                project_funding[project_code]['一般债券'] += amount
            elif funding_type == '专项债券':
                project_funding[project_code]['专项债券'] += amount
            else:
                project_funding[project_code]['其他资金'] += amount
        
        # 生成透视表数据
        for project_code, data in project_funding.items():
            general_bonds = data['一般债券']
            special_bonds = data['专项债券']
            other_funding = data['其他资金']
            bond_total = general_bonds + special_bonds
            total_funding = bond_total + other_funding
            
            pivot_row = [
                project_code,
                data['name'],
                f"{general_bonds:.2f}" if general_bonds > 0 else "0.00",
                f"{special_bonds:.2f}" if special_bonds > 0 else "0.00",
                f"{bond_total:.2f}" if bond_total > 0 else "0.00",
                f"{other_funding:.2f}" if other_funding > 0 else "0.00",
                f"{total_funding:.2f}"
            ]
            
            pivot_data.append(pivot_row)
        
        return pivot_data
    
    def save_to_csv(self, data, filename):
        """保存数据到CSV文件"""
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    
    def generate_data_files(self):
        """生成所有数据文件"""
        print("🏗️ 开始生成AI城建系统数据文件...")
        
        # 创建输出目录
        output_dir = "AI城建系统数据"
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成基础数据
        print("📊 生成项目基本信息表（200个项目）...")
        projects_data = self.create_project_basic_info(200)
        self.save_to_csv(projects_data, f"{output_dir}/01_项目基本信息表.csv")
        
        print("💰 生成资金安排表（1000条记录）...")
        funding_data = self.create_funding_arrangement(projects_data, 1000)
        self.save_to_csv(funding_data, f"{output_dir}/02_资金安排表.csv")
        
        print("⭐ 生成重点项目清单表...")
        key_projects_data = self.create_key_projects_list(projects_data)
        self.save_to_csv(key_projects_data, f"{output_dir}/03_重点项目清单.csv")
        
        print("📈 生成数据可视化分析...")
        visualization_data = self.create_data_visualization_sheet(projects_data, funding_data)
        self.save_to_csv(visualization_data, f"{output_dir}/04_数据可视化.csv")
        
        print("📋 生成智慧报表数据...")
        reports_data = self.create_smart_reports_sheet(projects_data, funding_data, key_projects_data)
        self.save_to_csv(reports_data, f"{output_dir}/05_智慧报表生成.csv")
        
        print("🔄 生成数据透视表...")
        pivot_data = self.create_pivot_analysis(funding_data)
        self.save_to_csv(pivot_data, f"{output_dir}/06_数据透视表.csv")
        
        # 生成使用说明
        readme_content = """# AI城建系统数据文件说明

## 文件列表

1. **01_项目基本信息表.csv** - 200个模拟项目
   - 项目名称、项目编码、建设单位、项目主管部门
   - 立项时间、概算批复金额（500-20000万元）
   - 预计开工时间、预计完工时间、项目状态

2. **02_资金安排表.csv** - 1000条资金安排记录
   - 通过项目编码与项目基本信息表关联
   - 包含资金批复金额、批复日期、资金性质
   - 经办人、经办处室等信息

3. **03_重点项目清单.csv** - 约60个重点项目（30%比例）
   - 项目编码、项目名称、优先级
   - 关键特征、战略重要性

4. **04_数据可视化.csv** - 图表数据分析
   - 项目状态分布统计
   - 资金性质分析统计
   - 债券资金专项统计

5. **05_智慧报表生成.csv** - 多维度统计报表
   - 项目总览报表数据
   - 资金安排报表数据
   - 债券资金专项报表数据

6. **06_数据透视表.csv** - 债券资金合计分析
   - 按项目编码分组
   - 一般债券、专项债券分别统计
   - 自动计算债券资金合计

## 数据特点

- ✅ 真实性强：符合实际业务场景
- ✅ 关联性好：通过项目编码实现表间关联
- ✅ 完整性高：涵盖项目全生命周期数据
- ✅ 可扩展性：支持进一步数据分析和处理

## 使用方法

1. 可以直接在Excel中打开CSV文件
2. 支持数据筛选、排序、透视表制作
3. 可导入数据库系统进行进一步分析
4. 支持各种数据可视化工具

## 注意事项

- CSV文件使用UTF-8编码，确保中文正常显示
- 金额单位为万元
- 日期格式为YYYY-MM-DD
- 项目编码为唯一标识，用于表间关联
"""
        
        with open(f"{output_dir}/README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ 数据文件生成完成！")
        print(f"📁 输出目录：{os.path.abspath(output_dir)}")
        print(f"📄 包含文件：")
        print(f"   • 项目基本信息表：{len(projects_data)-1} 条记录")
        print(f"   • 资金安排表：{len(funding_data)-1} 条记录")
        print(f"   • 重点项目清单：{len(key_projects_data)-1} 条记录")
        print(f"   • 数据可视化：图表数据分析")
        print(f"   • 智慧报表生成：多维度统计报表")
        print(f"   • 数据透视表：债券资金合计分析")
        print(f"   • README.md：使用说明文档")
        
        return output_dir

def main():
    """主函数"""
    generator = SimpleExcelDataGenerator()
    output_dir = generator.generate_data_files()
    
    print("\n🎉 AI城建系统数据文件生成完成！")
    print(f"📍 文件位置：{os.path.abspath(output_dir)}")
    print("\n📋 数据说明：")
    print("✅ 200个模拟项目，概算金额500-20000万元")
    print("✅ 1000条资金安排，通过项目编码关联")
    print("✅ 约60个重点项目（30%比例）")
    print("✅ 完整的数据可视化分析")
    print("✅ 多维度智慧报表数据")
    print("✅ 债券资金合计透视分析")
    print("\n💡 可以在Excel中打开CSV文件，支持所有Excel功能")
    print("💡 文件使用UTF-8编码，确保中文正常显示")

if __name__ == "__main__":
    main()