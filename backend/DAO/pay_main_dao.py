# -*- coding: utf-8 -*-
"""采购主表 DAO"""

from DAO.base_dao import BaseDAO
from models.pay_main import PayMain


class PayMainDAO(BaseDAO):
    """采购主表数据访问对象"""

    def __init__(self):
        super().__init__(PayMain)

    def add(self, pay_main: PayMain) -> int:
        sql = """
        INSERT INTO tb_pay_main
        (Eid, Pcount, Ptotal, Pdate, other)
        VALUES (%s, %s, %s, %s, %s)
        """
        return self._insert_return_id(sql, (
            pay_main.eid,
            pay_main.pcount,
            pay_main.ptotal,
            pay_main.pdate,
            pay_main.other
        ))

    def update(self, pay_main: PayMain) -> int:
        sql = """
        UPDATE tb_pay_main
        SET Eid=%s, Pcount=%s, Ptotal=%s, Pdate=%s, other=%s
        WHERE Pid=%s
        """
        return self._update(sql, (
            pay_main.eid,
            pay_main.pcount,
            pay_main.ptotal,
            pay_main.pdate,
            pay_main.other,
            pay_main.pid
        ))

    def delete(self, pid: int) -> int:
        sql = "DELETE FROM tb_pay_main WHERE Pid=%s"
        return self._update(sql, (pid,))

    def get_by_id(self, pid: int):
        sql = "SELECT * FROM tb_pay_main WHERE Pid=%s"
        return self._query_one(sql, (pid,))

    def get_all(self):
        sql = "SELECT * FROM tb_pay_main ORDER BY Pid DESC"
        return self._query_all(sql)

    def get_by_employee_id(self, eid: str):
        sql = "SELECT * FROM tb_pay_main WHERE Eid=%s ORDER BY Pid DESC"
        return self._query_all(sql, (eid,))

    def search_by_date(self, pdate: str):
        sql = "SELECT * FROM tb_pay_main WHERE Pdate=%s ORDER BY Pid DESC"
        return self._query_all(sql, (pdate,))

    def search_by_date_range(self, start_date: str, end_date: str):
        sql = """
        SELECT * FROM tb_pay_main
        WHERE Pdate BETWEEN %s AND %s
        ORDER BY Pid DESC
        """
        return self._query_all(sql, (start_date, end_date))