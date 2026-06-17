# -*- coding: utf-8 -*-
"""DAO 测试文件"""

from DAO.employee_dao import EmployeeDAO
from DAO.customer_dao import CustomerDAO
from DAO.good_dao import GoodDAO
from DAO.pay_main_dao import PayMainDAO
from DAO.pay_detail_dao import PayDetailDAO

from models.employee import Employee
from models.customer import Customer
from models.good import Good
from models.pay_main import PayMain
from models.pay_detail import PayDetail


def test_employee():
    dao = EmployeeDAO()

    emp = Employee(
        eid='yg10005',
        ename='张三',
        epas='000000',
        elevel='20',
        etel_phone='13800000000',
        esalary=3500.00,
        other='测试员工'
    )

    try:
        dao.add(emp)
    except Exception as e:
        print("员工新增可能已存在：", e)

    result = dao.get_by_id('yg10005')
    print("员工查询结果：", result)


def test_customer():
    dao = CustomerDAO()

    customer = Customer(
        cid='gys1001',
        ccompany_name='大连供货商',
        ccompany_sname='大供',
        ccompany_address='大连市开发区',
        ccompany_phone='0411-1234567',
        cemail='test@test.com',
        cname='李四',
        ctel_phone='13900000000',
        other='测试客户'
    )

    try:
        dao.add(customer)
    except Exception as e:
        print("客户新增可能已存在：", e)

    result = dao.get_by_id('gys1001')
    print("客户查询结果：", result)


def test_good():
    dao = GoodDAO()

    good = Good(
        gid='sp00000001',
        gname='可乐',
        gpay=3.50,
        cid='gys1001',
        gintroduction='饮料',
        other='测试商品'
    )

    try:
        dao.add(good)
    except Exception as e:
        print("商品新增可能已存在：", e)

    result = dao.get_by_id('sp00000001')
    print("商品查询结果：", result)


def test_purchase():
    main_dao = PayMainDAO()
    detail_dao = PayDetailDAO()

    pay_main = PayMain(
        eid='yg10005',
        pcount=0,
        ptotal=0.0,
        pdate='20260605',
        other='测试采购单'
    )

    pid = main_dao.add(pay_main)
    print("新增采购主表成功，Pid =", pid)

    detail = PayDetail(
        pid=pid,
        gid='sp00000001',
        pcount2=10,
        gpay=3.50,
        total=35.00,
        other='测试明细'
    )

    pdid = detail_dao.add_and_refresh(detail)
    print("新增采购明细成功，PDid =", pdid)

    main_result = main_dao.get_by_id(pid)
    detail_result = detail_dao.get_by_pid(pid)

    print("采购主表：", main_result)
    print("采购明细：", detail_result)


if __name__ == '__main__':
    test_employee()
    test_customer()
    test_good()
    test_purchase()