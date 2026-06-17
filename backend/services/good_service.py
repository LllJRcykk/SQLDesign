# -*- coding: utf-8 -*-
"""商品业务逻辑层"""

import os
from dao.good_dao import GoodDAO
from dao.customer_dao import CustomerDAO
from models.good import Good
from utils.csv_exporter import CSVExporter


class GoodService:
    """商品业务逻辑"""

    def __init__(self):
        self.good_dao = GoodDAO()
        self.customer_dao = CustomerDAO()

    def add_good(self, good: Good) -> tuple[bool, str]:
        valid, msg = good.validate()
        if not valid:
            return False, msg

        old = self.good_dao.get_by_id(good.gid)
        if old:
            return False, f"商品编号 {good.gid} 已存在"

        customer = self.customer_dao.get_by_id(good.cid)
        if not customer:
            return False, f"供应商编号 {good.cid} 不存在"

        try:
            rows = self.good_dao.add(good)
            return rows > 0, "商品新增成功" if rows > 0 else "商品新增失败"
        except Exception as e:
            return False, f"商品新增失败：{e}"

    def update_good(self, good: Good) -> tuple[bool, str]:
        valid, msg = good.validate()
        if not valid:
            return False, msg

        old = self.good_dao.get_by_id(good.gid)
        if not old:
            return False, f"商品编号 {good.gid} 不存在"

        customer = self.customer_dao.get_by_id(good.cid)
        if not customer:
            return False, f"供应商编号 {good.cid} 不存在"

        try:
            rows = self.good_dao.update(good)
            return rows > 0, "商品修改成功" if rows > 0 else "商品修改失败"
        except Exception as e:
            return False, f"商品修改失败：{e}"

    def delete_good(self, gid: str) -> tuple[bool, str]:
        old = self.good_dao.get_by_id(gid)
        if not old:
            return False, f"商品编号 {gid} 不存在"

        try:
            rows = self.good_dao.delete(gid)
            return rows > 0, "商品删除成功" if rows > 0 else "商品删除失败"
        except Exception as e:
            return False, f"商品删除失败：{e}"

    def get_good_by_id(self, gid: str):
        return self.good_dao.get_by_id(gid)

    def get_all_goods(self):
        return self.good_dao.get_all()

    def search_by_name(self, keyword: str):
        return self.good_dao.search_by_name(keyword)

    def search_by_price_range(self, min_price: float, max_price: float):
        return self.good_dao.search_by_price_range(min_price, max_price)

    def get_by_customer_id(self, cid: str):
        return self.good_dao.get_by_customer_id(cid)

    def export_goods_to_csv(self, file_path: str = 'exports/goods.csv') -> tuple[bool, str]:
        """导出商品数据到 CSV"""
        try:
            goods = self.good_dao.get_all()
            headers = ['商品编号', '商品名称', '商品单价', '供应商编号', '商品简介', '备注']
            rows = []

            for g in goods:
                rows.append([
                    g.gid,
                    g.gname,
                    g.gpay,
                    g.cid,
                    g.gintroduction,
                    g.other
                ])

            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"商品数据导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"商品数据导出失败：{e}"