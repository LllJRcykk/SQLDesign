# -*- coding: utf-8 -*-
"""商品业务逻辑层"""

from dao.good_dao import GoodDAO
from dao.customer_dao import CustomerDAO
from models.good import Good


class GoodService:
    """商品业务逻辑"""

    def __init__(self):
        self.good_dao = GoodDAO()
        self.customer_dao = CustomerDAO()

    def add_good(self, good: Good) -> tuple[bool, str]:
        """新增商品"""
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
        """修改商品"""
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
        """删除商品"""
        old = self.good_dao.get_by_id(gid)
        if not old:
            return False, f"商品编号 {gid} 不存在"

        try:
            rows = self.good_dao.delete(gid)
            return rows > 0, "商品删除成功" if rows > 0 else "商品删除失败"
        except Exception as e:
            return False, f"商品删除失败：{e}"

    def get_good_by_id(self, gid: str):
        """按编号查询商品"""
        return self.good_dao.get_by_id(gid)

    def get_all_goods(self):
        """查询全部商品"""
        return self.good_dao.get_all()

    def search_by_name(self, keyword: str):
        """按商品名模糊查询"""
        return self.good_dao.search_by_name(keyword)

    def search_by_price_range(self, min_price: float, max_price: float):
        """按价格范围查询"""
        return self.good_dao.search_by_price_range(min_price, max_price)

    def get_by_customer_id(self, cid: str):
        """按供应商编号查询商品"""
        return self.good_dao.get_by_customer_id(cid)