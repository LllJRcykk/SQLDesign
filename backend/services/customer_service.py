# -*- coding: utf-8 -*-
"""客户业务逻辑层"""

import os
from dao.customer_dao import CustomerDAO
from dao.good_dao import GoodDAO
from models.customer import Customer
from utils.csv_exporter import CSVExporter


class CustomerService:
    """客户业务逻辑"""

    def __init__(self):
        self.customer_dao = CustomerDAO()
        self.good_dao = GoodDAO()

    def add_customer(self, customer: Customer) -> tuple[bool, str]:
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
        return self.customer_dao.get_by_id(cid)

    def get_all_customers(self):
        return self.customer_dao.get_all()

    def search_by_name(self, keyword: str):
        return self.customer_dao.search_by_name(keyword)

    def search_by_contact(self, keyword: str):
        return self.customer_dao.search_by_contact(keyword)

    def export_customers_to_csv(self, file_path: str = 'exports/customers.csv') -> tuple[bool, str]:
        """导出客户数据到 CSV"""
        try:
            customers = self.customer_dao.get_all()
            headers = ['客户编号', '客户名称', '客户简称', '地址', '公司电话', '邮箱', '联系人', '联系人电话', '备注']
            rows = []

            for c in customers:
                rows.append([
                    c.cid,
                    c.ccompany_name,
                    c.ccompany_sname,
                    c.ccompany_address,
                    c.ccompany_phone,
                    c.cemail,
                    c.cname,
                    c.ctel_phone,
                    c.other
                ])

            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"客户数据导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"客户数据导出失败：{e}"