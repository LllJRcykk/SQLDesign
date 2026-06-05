# -*- coding: utf-8 -*-
"""商品 DAO"""

from dao.base_dao import BaseDAO
from models.good import Good


class GoodDAO(BaseDAO):
    """商品数据访问对象"""

    def __init__(self):
        super().__init__(Good)

    def add(self, good: Good) -> int:
        sql = """
        INSERT INTO tb_good
        (Gid, GName, GPay, Cid, GIntroduction, other)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self._update(sql, (
            good.gid,
            good.gname,
            good.gpay,
            good.cid,
            good.gintroduction,
            good.other
        ))

    def update(self, good: Good) -> int:
        sql = """
        UPDATE tb_good
        SET GName=%s, GPay=%s, Cid=%s, GIntroduction=%s, other=%s
        WHERE Gid=%s
        """
        return self._update(sql, (
            good.gname,
            good.gpay,
            good.cid,
            good.gintroduction,
            good.other,
            good.gid
        ))

    def delete(self, gid: str) -> int:
        sql = "DELETE FROM tb_good WHERE Gid=%s"
        return self._update(sql, (gid,))

    def get_by_id(self, gid: str):
        sql = "SELECT * FROM tb_good WHERE Gid=%s"
        return self._query_one(sql, (gid,))

    def get_all(self):
        sql = "SELECT * FROM tb_good ORDER BY Gid"
        return self._query_all(sql)

    def search_by_name(self, keyword: str):
        sql = "SELECT * FROM tb_good WHERE GName LIKE %s ORDER BY Gid"
        return self._query_all(sql, (f"%{keyword}%",))

    def search_by_price_range(self, min_price: float, max_price: float):
        sql = """
        SELECT * FROM tb_good
        WHERE GPay BETWEEN %s AND %s
        ORDER BY GPay
        """
        return self._query_all(sql, (min_price, max_price))

    def get_by_customer_id(self, cid: str):
        sql = "SELECT * FROM tb_good WHERE Cid=%s ORDER BY Gid"
        return self._query_all(sql, (cid,))