# -*- coding: utf-8 -*-
"""客户 DAO"""

from DAO.base_dao import BaseDAO
from models.customer import Customer


class CustomerDAO(BaseDAO):
    """客户数据访问对象"""

    def __init__(self):
        super().__init__(Customer)

    def add(self, customer: Customer) -> int:
        sql = """
        INSERT INTO tb_customer
        (Cid, CcompanyName, CcompanySName, CcompanyAddress, CcompanyPhone, Cemail, CName, CtelPhone, other)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self._update(sql, (
            customer.cid,
            customer.ccompany_name,
            customer.ccompany_sname,
            customer.ccompany_address,
            customer.ccompany_phone,
            customer.cemail,
            customer.cname,
            customer.ctel_phone,
            customer.other
        ))

    def update(self, customer: Customer) -> int:
        sql = """
        UPDATE tb_customer
        SET CcompanyName=%s, CcompanySName=%s, CcompanyAddress=%s,
            CcompanyPhone=%s, Cemail=%s, CName=%s, CtelPhone=%s, other=%s
        WHERE Cid=%s
        """
        return self._update(sql, (
            customer.ccompany_name,
            customer.ccompany_sname,
            customer.ccompany_address,
            customer.ccompany_phone,
            customer.cemail,
            customer.cname,
            customer.ctel_phone,
            customer.other,
            customer.cid
        ))

    def delete(self, cid: str) -> int:
        sql = "DELETE FROM tb_customer WHERE Cid=%s"
        return self._update(sql, (cid,))

    def get_by_id(self, cid: str):
        sql = "SELECT * FROM tb_customer WHERE Cid=%s"
        return self._query_one(sql, (cid,))

    def get_all(self):
        sql = "SELECT * FROM tb_customer ORDER BY Cid"
        return self._query_all(sql)

    def search_by_name(self, keyword: str):
        sql = "SELECT * FROM tb_customer WHERE CcompanyName LIKE %s ORDER BY Cid"
        return self._query_all(sql, (f"%{keyword}%",))

    def search_by_contact(self, keyword: str):
        sql = "SELECT * FROM tb_customer WHERE CName LIKE %s ORDER BY Cid"
        return self._query_all(sql, (f"%{keyword}%",))