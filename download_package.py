#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统数据下载包
复制此脚本到您的本地计算机运行，将生成完全相同的Excel数据文件
"""

import csv
import random
import os
from datetime import datetime, timedelta

print("🎉 AI城建系统数据生成器")
print("=" * 50)
print("本脚本将在您的本地计算机生成完全相同的数据文件")
print("包含：200个项目 + 1000条资金安排 + 透视表分析")
print("=" * 50)

# 设置随机种子，确保每次生成相同的数据
random.seed(42)

class LocalDataGenerator:
    def __init__(self):
        self.project_statuses = ['在建', '续建', '完工', '暂停']
        self.funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助']
        
        self.construction_units = [
            '市政建设集团有限公司', '城市投资建设集团', '交通建设发展集团', '水务建设集团公司',
            '园林绿化建设集团', '教育建设投资公司', '医疗建设发展公司', '住房建设集团'
        ]
        
        self.supervising_departments = [
            '市发展和改革委员会', '市住房和城乡建设局', '市交通运输局', '市水利局',
            '市教育局', '市卫生健康委员会', '市生态环境局', '市园林绿化局'
        ]
        
        self.operators = [
            '张建华', '李明强', '王志远', '赵文博', '钱国强', '孙海涛', '周建军', '吴德华',
            '陈志刚', '刘建国', '杨文华', '黄志明', '朱建平', '林志强'
        ]
        
        self.operating_departments = [
            '计划财务处', '项目管理处', '投资建设处', '资金管理处', '审计监察处',
            '工程建设处', '规划设计处', '招投标管理处'
        ]
        
        self.project_types = [
            '道路建设工程', '桥梁建设工程', '隧道建设工程', '排水管网工程', '供水管网工程',
            '公园绿化工程', '广场建设工程', '学校建设工程', '医院建设工程', '住宅小区建设'
        ]
        
        self.areas = [
            '东城区', '西城区', '南城区', '北城区', '中心区', '开发区', '新区', '高新区'
        ]
    
    def generate_project_code(self, index):
        year = datetime.now().year
        return f"UC{year}{index:04d}"
    
    def generate_project_name(self, index):
        area = random.choice(self.areas)
        project_type = random.choice(self.project_types)
        phase = random.choice(['一期', '二期', '三期', '四期', '五期'])
        return f"{area}{project_type}{phase}"
    
    def generate_random_date(self, start_date, end_date):
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    def create_project_basic_info(self, count=200):
        print(f"📊 生成项目基本信息表（{count}个项目）...")
        projects = []
        
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '立项时间',
            '概算批复金额', '预计开工时间', '预计完工时间', '项目状态'
        ]
        projects.append(headers)
        
        for i in range(1, count + 1):
            project_code = self.generate_project_code(i)
            project_name = self.generate_project_name(i)
            budget_amount = round(random.uniform(500, 20000), 2)
            
            base_date = datetime(2023, 1, 1)
            approval_date = self.generate_random_date(base_date, datetime(2024, 6, 30))
            planned_start_date = approval_date + timedelta(days=random.randint(30, 180))
            planned_end_date = planned_start_date + timedelta(days=random.randint(180, 1095))
            
            project_row = [
                project_name, project_code,
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
        print(f"💰 生成资金安排表（{count}条记录）...")
        funding_records = []
        
        headers = [
            '项目名称', '项目编码', '建设单位', '项目主管部门', '概算批复金额',
            '资金批复金额', '批复日期', '资金性质', '经办人', '经办处室'
        ]
        funding_records.append(headers)
        
        projects_list = projects_data[1:]
        
        # 每个项目至少一条资金安排
        for project in projects_list:
            budget_amount = float(project[5])
            funding_amount = round(random.uniform(budget_amount * 0.1, budget_amount * 0.8), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_approval_date = approval_date + timedelta(days=random.randint(1, 90))
            
            funding_row = [
                project[0], project[1], project[2], project[3], budget_amount,
                funding_amount, funding_approval_date.strftime('%Y-%m-%d'),
                random.choice(self.funding_types),
                random.choice(self.operators),
                random.choice(self.operating_departments)
            ]
            funding_records.append(funding_row)
        
        # 生成剩余记录
        remaining_count = count - len(projects_list)
        for _ in range(remaining_count):
            project = random.choice(projects_list)
            budget_amount = float(project[5])
            funding_amount = round(random.uniform(budget_amount * 0.05, budget_amount * 0.5), 2)
            approval_date = datetime.strptime(project[4], '%Y-%m-%d')
            funding_approval_date = approval_date + timedelta(days=random.randint(1, 365))
            
            funding_row = [
                project[0], project[1], project[2], project[3], budget_amount,
                funding_amount, funding_approval_date.strftime('%Y-%m-%d'),
                random.choice(self.funding_types),
                random.choice(self.operators),
                random.choice(self.operating_departments)
            ]
            funding_records.append(funding_row)
        
        return funding_records
    
    def create_pivot_analysis(self, funding_data):
        print("🔄 生成数据透视表（债券资金合计分析）...")
        pivot_data = []
        
        headers = ['项目编码', '项目名称', '一般债券', '专项债券', '债券资金合计', '其他资金', '资金总计']
        pivot_data.append(headers)
        
        funding_list = funding_data[1:]
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
        
        for project_code, data in project_funding.items():
            general_bonds = data['一般债券']
            special_bonds = data['专项债券']
            other_funding = data['其他资金']
            bond_total = general_bonds + special_bonds
            total_funding = bond_total + other_funding
            
            pivot_row = [
                project_code, data['name'],
                f"{general_bonds:.2f}" if general_bonds > 0 else "0.00",
                f"{special_bonds:.2f}" if special_bonds > 0 else "0.00",
                f"{bond_total:.2f}" if bond_total > 0 else "0.00",
                f"{other_funding:.2f}" if other_funding > 0 else "0.00",
                f"{total_funding:.2f}"
            ]
            pivot_data.append(pivot_row)
        
        return pivot_data
    
    def save_to_csv(self, data, filename):
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print(f"  ✅ 已保存：{filename}")
    
    def generate_all_files(self):
        print("🏗️ 开始生成AI城建系统完整数据文件...")
        
        output_dir = "AI城建系统数据"
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 创建输出目录：{output_dir}")
        
        # 生成数据
        projects_data = self.create_project_basic_info(200)
        self.save_to_csv(projects_data, f"{output_dir}/01_项目基本信息表.csv")
        
        funding_data = self.create_funding_arrangement(projects_data, 1000)
        self.save_to_csv(funding_data, f"{output_dir}/02_资金安排表.csv")
        
        pivot_data = self.create_pivot_analysis(funding_data)
        self.save_to_csv(pivot_data, f"{output_dir}/03_数据透视表_债券资金合计.csv")
        
        # 创建使用说明
        readme_content = """# AI城建系统数据文件

## 📊 文件说明

1. **01_项目基本信息表.csv** - 200个模拟项目
   - 概算批复金额：500-20000万元
   - 项目状态：在建、续建、完工、暂停
   - 包含完整的项目基本信息

2. **02_资金安排表.csv** - 1000条资金安排记录
   - 通过项目编码与项目表关联
   - 资金性质：一般债券、专项债券、中央综合财力等7种类型
   - 包含经办人、经办处室等详细信息

3. **03_数据透视表_债券资金合计.csv** - 透视分析
   - 按项目编码分组统计
   - 一般债券、专项债券分别计算
   - 自动生成债券资金合计 = 一般债券 + 专项债券

## 🎯 使用方法

1. 直接在Excel中打开CSV文件
2. 支持数据筛选、排序、图表制作
3. 可以制作数据透视表进行深入分析
4. 支持导入到各种数据库系统

## 💡 特色功能

✅ 真实的项目名称和单位名称
✅ 符合实际业务场景的数据分布
✅ 完整的表间关联关系
✅ 债券资金合计自动计算

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(f"{output_dir}/README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  ✅ 已保存：{output_dir}/README.md")
        
        print("\n" + "=" * 50)
        print("🎉 AI城建系统数据文件生成完成！")
        print(f"📁 文件位置：{os.path.abspath(output_dir)}")
        print("\n📋 包含文件：")
        print(f"   • 项目基本信息表：{len(projects_data)-1} 条记录")
        print(f"   • 资金安排表：{len(funding_data)-1} 条记录")  
        print(f"   • 数据透视表：{len(pivot_data)-1} 条记录")
        print(f"   • README说明文档")
        print("\n💡 现在可以在Excel中打开这些文件使用了！")
        
        return output_dir

def main():
    """主函数"""
    try:
        generator = LocalDataGenerator()
        output_dir = generator.generate_all_files()
        
        print(f"\n🎊 恭喜！AI城建系统数据已成功生成到您的本地计算机！")
        print(f"📂 请查看目录：{os.path.abspath(output_dir)}")
        
        input("\n按回车键退出...")
        
    except Exception as e:
        print(f"\n❌ 生成过程中出现错误：{e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()