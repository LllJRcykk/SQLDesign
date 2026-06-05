# -*- coding: utf-8 -*-
"""实体类测试"""

from models.employee import Employee
from models.customer import Customer
from models.good import Good
from models.pay_main import PayMain
from models.pay_detail import PayDetail

def test_employee():
    """测试员工实体"""
    emp = Employee(
        eid='yg10001',
        ename='张三',
        epas='000000',
        elevel='00',
        etel_phone='13800138000',
        esalary=5000.00,
        other='管理员'
    )
    
    print(f"员工信息：{emp}")
    print(f"级别名称：{emp.get_level_name()}")
    print(f"是否管理员：{emp.is_admin()}")
    
    is_valid, msg = emp.validate()
    print(f"验证结果：{msg}")
    
    # 转换为字典
    print(f"字典格式：{emp.to_dict()}")
    
    # 转换为 JSON
    print(f"JSON 格式：{emp.to_json()}")

def test_pay_detail():
    """测试采购明细实体"""
    detail = PayDetail(
        pid=1,
        gid='sp00000001',
        pcount2=10,
        gpay=25.5
    )
    
    detail.calculate_total()
    print(f"明细总价：{detail.total}")  # 应该是 255.0
    
    is_valid, msg = detail.validate()
    print(f"验证结果：{msg}")

if __name__ == '__main__':
    print("=" * 50)
    print("测试员工实体")
    print("=" * 50)
    test_employee()
    
    print("\n" + "=" * 50)
    print("测试采购明细实体")
    print("=" * 50)
    test_pay_detail()