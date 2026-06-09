# -*- coding: utf-8 -*-
"""客户业务逻辑层"""

from dao.customer_dao import CustomerDAO
from dao.good_dao import GoodDAO
from models.customer import Customer


class CustomerService:
    """客户业务逻辑"""

    def __init__(self):
        self.customer_dao = CustomerDAO()
        self.good_dao = GoodDAO()

    def add_customer(self, customer: Customer) -> tuple[bool, str]:
        """新增客户"""
        valid, msg = customer.validate()
        if not valid:
            return False, msg

        old = self.customer_dao.get_by_id(customer.cid)
        if old:
            return False, f"客户编号 {customer.cid} 已存在"

        try:
            rows = self.customer_dao.add(customer)
            return rows > 0, "客户新增成功" if rows > 0 else "客户新增失败"
        except Exception as e:
            return False, f"客户新增失败：{e}"

    def update_customer(self, customer: Customer) -> tuple[bool, str]:
        """修改客户"""
        valid, msg = customer.validate()
        if not valid:
            return False, msg

        old = self.customer_dao.get_by_id(customer.cid)
        if not old:
            return False, f"客户编号 {customer.cid} 不存在"

        try:
            rows = self.customer_dao.update(customer)
            return rows > 0, "客户修改成功" if rows > 0 else "客户修改失败"
        except Exception as e:
            return False, f"客户修改失败：{e}"

    def delete_customer(self, cid: str) -> tuple[bool, str]:
        """删除客户
        若客户下面还有商品，不允许删除
        """
        old = self.customer_dao.get_by_id(cid)
        if not old:
            return False, f"客户编号 {cid} 不存在"

        goods = self.good_dao.get_by_customer_id(cid)
        if goods:
            return False, f"客户编号 {cid} 下存在商品数据，不能删除"

        try:
            rows = self.customer_dao.delete(cid)
            return rows > 0, "客户删除成功" if rows > 0 else "客户删除失败"
        except Exception as e:
            return False, f"客户删除失败：{e}"

    def get_customer_by_id(self, cid: str):
        """按编号查询客户"""
        return self.customer_dao.get_by_id(cid)

    def get_all_customers(self):
        """查询全部客户"""
        return self.customer_dao.get_all()

    def search_by_name(self, keyword: str):
        """按客户名称模糊查询"""
        return self.customer_dao.search_by_name(keyword)

    def search_by_contact(self, keyword: str):
        """按联系人模糊查询"""
        return self.customer_dao.search_by_contact(keyword)