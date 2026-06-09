# -*- coding: utf-8 -*-
"""Service 层测试文件"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.employee_service import EmployeeService
from services.customer_service import CustomerService
from services.good_service import GoodService
from services.purchase_service import PurchaseService

from models.employee import Employee
from models.customer import Customer
from models.good import Good
from models.pay_main import PayMain
from models.pay_detail import PayDetail


def test_employee_service():
    service = EmployeeService()

    emp = Employee(
        eid='yg10010',
        ename='王五',
        epas='000000',
        elevel='20',
        etel_phone='13811112222',
        esalary=4200.00,
        other='service测试员工'
    )

    success, msg = service.add_employee(emp)
    print("新增员工：", success, msg)

    result = service.get_employee_by_id('yg10010')
    print("查询员工：", result)

    result_list = service.search_by_name('王')
    print("模糊查询员工：", result_list)


def test_customer_service():
    service = CustomerService()

    customer = Customer(
        cid='gys1008',
        ccompany_name='测试供应商A',
        ccompany_sname='供应A',
        ccompany_address='大连高新区',
        ccompany_phone='0411-8888888',
        cemail='suppliera@test.com',
        cname='赵六',
        ctel_phone='13911112222',
        other='service测试客户'
    )

    success, msg = service.add_customer(customer)
    print("新增客户：", success, msg)

    result = service.get_customer_by_id('gys1008')
    print("查询客户：", result)


def test_good_service():
    customer_service = CustomerService()
    good_service = GoodService()

    customer = Customer(
        cid='gys1009',
        ccompany_name='测试供应商B',
        ccompany_sname='供应B',
        ccompany_address='大连开发区',
        ccompany_phone='0411-6666666',
        cemail='supplierb@test.com',
        cname='孙七',
        ctel_phone='13933334444',
        other='测试'
    )
    customer_service.add_customer(customer)

    good = Good(
        gid='sp00000009',
        gname='雪碧',
        gpay=3.50,
        cid='gys1009',
        gintroduction='饮料',
        other='service测试商品'
    )

    success, msg = good_service.add_good(good)
    print("新增商品：", success, msg)

    result = good_service.get_good_by_id('sp00000009')
    print("查询商品：", result)

    result_list = good_service.search_by_price_range(1, 10)
    print("价格范围查询商品：", result_list)


def test_purchase_service():
    employee_service = EmployeeService()
    customer_service = CustomerService()
    good_service = GoodService()
    purchase_service = PurchaseService()

    # 1. 准备员工
    emp = Employee(
        eid='yg10011',
        ename='采购员A',
        epas='000000',
        elevel='20',
        etel_phone='13855556666',
        esalary=5000.00,
        other='采购测试员工'
    )
    employee_service.add_employee(emp)

    # 2. 准备供应商
    customer = Customer(
        cid='gys1010',
        ccompany_name='采购测试供应商',
        ccompany_sname='采购供',
        ccompany_address='测试地址',
        ccompany_phone='0411-5555555',
        cemail='cg@test.com',
        cname='联系人A',
        ctel_phone='13955556666',
        other='采购测试客户'
    )
    customer_service.add_customer(customer)

    # 3. 准备商品
    good = Good(
        gid='sp00000010',
        gname='矿泉水',
        gpay=2.00,
        cid='gys1010',
        gintroduction='饮用水',
        other='采购测试商品'
    )
    good_service.add_good(good)

    # 4. 新增采购主表
    pay_main = PayMain(
        eid='yg10011',
        pcount=0,
        ptotal=0.0,
        pdate='20260609',
        other='采购service测试主表'
    )
    success, msg, pid = purchase_service.create_pay_main(pay_main)
    print("新增采购主表：", success, msg, pid)

    if not success:
        return

    # 5. 新增采购明细
    detail1 = PayDetail(
        pid=pid,
        gid='sp00000010',
        pcount2=10,
        gpay=2.00,
        total=20.00,
        other='明细1'
    )
    success, msg, pdid1 = purchase_service.add_pay_detail(detail1)
    print("新增采购明细1：", success, msg, pdid1)

    # 6. 查询采购主表和明细
    pay_info = purchase_service.get_pay_main_with_details(pid)
    print("采购主表及明细：", pay_info)

    details = purchase_service.get_details_by_pid(pid)
    print("采购明细列表：", details)

    # 7. 按日期范围查询
    result_list = purchase_service.search_pay_main_by_date_range('20260101', '20261231')
    print("日期范围查询采购主表：", result_list)


if __name__ == '__main__':
    test_employee_service()
    test_customer_service()
    test_good_service()
    test_purchase_service()