# -*- coding: utf-8 -*-
"""
项目数据模型
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional, List
import random
import string
from datetime import datetime, timedelta

@dataclass
class ProjectBasicInfo:
    """项目基本信息模型"""
    project_name: str
    project_code: str
    construction_unit: str
    supervising_department: str
    approval_date: Optional[date]
    budget_amount: float
    planned_start_date: Optional[date]
    planned_end_date: Optional[date]
    project_status: str  # 在建、续建、完工、暂停
    
    def __post_init__(self):
        # 验证项目状态
        valid_statuses = ['在建', '续建', '完工', '暂停']
        if self.project_status not in valid_statuses:
            raise ValueError(f"项目状态必须是以下之一：{valid_statuses}")

@dataclass
class FundingArrangement:
    """资金安排模型"""
    project_name: str
    project_code: str
    construction_unit: str
    supervising_department: str
    budget_amount: float
    funding_amount: float
    approval_date: date
    funding_type: str  # 一般债券、专项债券、中央综合财力、土地出让金、中央预算内投资、中央补助、省级补助
    operator: str
    operating_department: str
    
    def __post_init__(self):
        # 验证资金性质
        valid_types = ['一般债券', '专项债券', '中央综合财力', '土地出让金', '中央预算内投资', '中央补助', '省级补助']
        if self.funding_type not in valid_types:
            raise ValueError(f"资金性质必须是以下之一：{valid_types}")

@dataclass
class KeyProject:
    """重点项目模型"""
    project_code: str
    project_name: str
    priority_level: int = 1
    key_features: Optional[str] = None
    strategic_importance: Optional[str] = None

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
        
    def generate_project_code(self, index: int) -> str:
        """生成项目编码"""
        year = datetime.now().year
        return f"UC{year}{index:04d}"
        
    def generate_project_name(self, index: int) -> str:
        """生成项目名称"""
        project_types = [
            '道路建设工程', '桥梁建设工程', '排水管网工程', '公园绿化工程', '学校建设工程',
            '医院建设工程', '住宅小区建设', '商业综合体', '地铁建设工程', '污水处理厂',
            '垃圾处理中心', '体育中心建设', '文化中心建设', '停车场建设', '供水工程'
        ]
        areas = [
            '东城区', '西城区', '南城区', '北城区', '中心区', '开发区', '新区', '高新区'
        ]
        
        project_type = random.choice(project_types)
        area = random.choice(areas)
        return f"{area}{project_type}第{index}期"
        
    def generate_mock_projects(self, count: int = 200) -> List[ProjectBasicInfo]:
        """生成模拟项目数据"""
        projects = []
        
        for i in range(1, count + 1):
            project_code = self.generate_project_code(i)
            project_name = self.generate_project_name(i)
            
            # 随机生成概算批复金额（500-20000万元）
            budget_amount = random.uniform(500, 20000)
            
            # 随机生成日期
            start_date = datetime.now().date() - timedelta(days=random.randint(30, 730))
            end_date = start_date + timedelta(days=random.randint(180, 1095))
            approval_date = start_date - timedelta(days=random.randint(30, 180))
            
            project = ProjectBasicInfo(
                project_name=project_name,
                project_code=project_code,
                construction_unit=random.choice(self.construction_units),
                supervising_department=random.choice(self.supervising_departments),
                approval_date=approval_date,
                budget_amount=budget_amount,
                planned_start_date=start_date,
                planned_end_date=end_date,
                project_status=random.choice(self.project_statuses)
            )
            
            projects.append(project)
            
        return projects
        
    def generate_mock_funding(self, projects: List[ProjectBasicInfo], funding_count: int = 1000) -> List[FundingArrangement]:
        """生成模拟资金安排数据"""
        funding_list = []
        
        # 确保每个项目至少有一条资金安排
        for project in projects:
            funding_amount = random.uniform(project.budget_amount * 0.1, project.budget_amount * 0.8)
            funding_date = project.approval_date + timedelta(days=random.randint(1, 90))
            
            funding = FundingArrangement(
                project_name=project.project_name,
                project_code=project.project_code,
                construction_unit=project.construction_unit,
                supervising_department=project.supervising_department,
                budget_amount=project.budget_amount,
                funding_amount=funding_amount,
                approval_date=funding_date,
                funding_type=random.choice(self.funding_types),
                operator=random.choice(self.operators),
                operating_department=random.choice(self.operating_departments)
            )
            
            funding_list.append(funding)
            
        # 为剩余的资金安排随机选择项目
        remaining_count = funding_count - len(projects)
        for _ in range(remaining_count):
            project = random.choice(projects)
            funding_amount = random.uniform(project.budget_amount * 0.05, project.budget_amount * 0.5)
            funding_date = project.approval_date + timedelta(days=random.randint(1, 365))
            
            funding = FundingArrangement(
                project_name=project.project_name,
                project_code=project.project_code,
                construction_unit=project.construction_unit,
                supervising_department=project.supervising_department,
                budget_amount=project.budget_amount,
                funding_amount=funding_amount,
                approval_date=funding_date,
                funding_type=random.choice(self.funding_types),
                operator=random.choice(self.operators),
                operating_department=random.choice(self.operating_departments)
            )
            
            funding_list.append(funding)
            
        return funding_list