#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统 - 命令行快速演示版
"""

import random
from datetime import datetime

def main():
    print("🏙️ AI城建系统 - 命令行演示版")
    print("=" * 50)
    
    # 模拟生成数据
    print("\n📊 生成模拟数据...")
    
    projects = []
    funding = []
    
    # 生成项目
    project_types = ['道路建设', '桥梁建设', '公园建设', '学校建设', '医院建设']
    areas = ['东城区', '西城区', '南城区', '北城区']
    statuses = ['在建', '续建', '完工', '暂停']
    
    for i in range(1, 11):  # 生成10个项目
        project = {
            'name': f"{random.choice(areas)}{random.choice(project_types)}第{i}期",
            'code': f"UC2024{i:04d}",
            'budget': random.uniform(1000, 10000),
            'status': random.choice(statuses)
        }
        projects.append(project)
    
    # 生成资金安排
    funding_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金']
    
    for project in projects:
        for _ in range(random.randint(1, 3)):
            fund = {
                'project_code': project['code'],
                'project_name': project['name'],
                'amount': random.uniform(project['budget'] * 0.1, project['budget'] * 0.5),
                'type': random.choice(funding_types)
            }
            funding.append(fund)
    
    print(f"✅ 生成了 {len(projects)} 个项目")
    print(f"✅ 生成了 {len(funding)} 条资金安排")
    
    # 显示项目列表
    print("\n📋 项目基本信息：")
    print("-" * 80)
    print(f"{'项目名称':<25} {'项目编码':<12} {'概算金额':<12} {'项目状态':<8}")
    print("-" * 80)
    
    for project in projects[:5]:  # 显示前5个
        print(f"{project['name']:<25} {project['code']:<12} {project['budget']:<12.2f} {project['status']:<8}")
    
    if len(projects) > 5:
        print(f"... 还有 {len(projects)-5} 个项目")
    
    # 显示资金安排
    print("\n💰 资金安排信息：")
    print("-" * 80)
    print(f"{'项目编码':<12} {'资金金额':<12} {'资金性质':<15}")
    print("-" * 80)
    
    for fund in funding[:8]:  # 显示前8条
        print(f"{fund['project_code']:<12} {fund['amount']:<12.2f} {fund['type']:<15}")
    
    if len(funding) > 8:
        print(f"... 还有 {len(funding)-8} 条资金安排")
    
    # 数据透视表 - 债券资金合计
    print("\n📊 数据透视表 - 债券资金合计：")
    print("-" * 60)
    print(f"{'项目编码':<12} {'一般债券':<12} {'专项债券':<12} {'债券合计':<12}")
    print("-" * 60)
    
    bond_summary = {}
    for fund in funding:
        if fund['type'] in ['一般债券', '专项债券']:
            code = fund['project_code']
            if code not in bond_summary:
                bond_summary[code] = {'一般债券': 0, '专项债券': 0}
            bond_summary[code][fund['type']] += fund['amount']
    
    for code, bonds in bond_summary.items():
        general = bonds['一般债券']
        special = bonds['专项债券']
        total = general + special
        print(f"{code:<12} {general:<12.2f} {special:<12.2f} {total:<12.2f}")
    
    # 统计信息
    print("\n📈 统计摘要：")
    print("-" * 30)
    
    total_budget = sum(p['budget'] for p in projects)
    total_funding = sum(f['amount'] for f in funding)
    
    status_stats = {}
    for project in projects:
        status = project['status']
        status_stats[status] = status_stats.get(status, 0) + 1
    
    funding_stats = {}
    for fund in funding:
        ftype = fund['type']
        funding_stats[ftype] = funding_stats.get(ftype, 0) + 1
    
    print(f"项目总数：{len(projects)} 个")
    print(f"概算总额：{total_budget:.2f} 万元")
    print(f"资金安排：{len(funding)} 条")
    print(f"资金总额：{total_funding:.2f} 万元")
    
    print(f"\n项目状态分布：")
    for status, count in status_stats.items():
        print(f"  {status}：{count} 个")
    
    print(f"\n资金性质分布：")
    for ftype, count in funding_stats.items():
        print(f"  {ftype}：{count} 条")
    
    # 债券资金统计
    bond_total = sum(bonds['一般债券'] + bonds['专项债券'] for bonds in bond_summary.values())
    print(f"\n💎 债券资金合计：{bond_total:.2f} 万元")
    
    print("\n" + "=" * 50)
    print("🎉 AI城建系统演示完成！")
    print("💡 这是命令行演示版本，完整功能请使用桌面版或Web版")

if __name__ == "__main__":
    main()