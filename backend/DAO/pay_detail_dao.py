# -*- coding: utf-8 -*-
"""采购明细 DAO"""

from dao.base_dao import BaseDAO
from dao.db_helper import DBHelper
from models.pay_detail import PayDetail


class PayDetailDAO(BaseDAO):
    """采购明细数据访问对象"""

    def __init__(self):
        super().__init__(PayDetail)

    def add(self, detail: PayDetail) -> int:
        sql = """
        INSERT INTO tb_pay_detail
        (Pid, Gid, Pcount2, Gpay, total, other)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self._insert_return_id(sql, (
            detail.pid,
            detail.gid,
            detail.pcount2,
            detail.gpay,
            detail.total,
            detail.other
        ))

    def update(self, detail: PayDetail) -> int:
        sql = """
        UPDATE tb_pay_detail
        SET Pid=%s, Gid=%s, Pcount2=%s, Gpay=%s, total=%s, other=%s
        WHERE PDid=%s
        """
        return self._update(sql, (
            detail.pid,
            detail.gid,
            detail.pcount2,
            detail.gpay,
            detail.total,
            detail.other,
            detail.pdid
        ))

    def delete(self, pdid: int) -> int:
        detail = self.get_by_id(pdid)
        if not detail:
            return 0

        sql = "DELETE FROM tb_pay_detail WHERE PDid=%s"
        rows = self._update(sql, (pdid,))
        if rows > 0:
            self.refresh_main_total(detail.pid)
        return rows

    def get_by_id(self, pdid: int):
        sql = "SELECT * FROM tb_pay_detail WHERE PDid=%s"
        return self._query_one(sql, (pdid,))

    def get_all(self):
        sql = "SELECT * FROM tb_pay_detail ORDER BY PDid DESC"
        return self._query_all(sql)

    def get_by_pid(self, pid: int):
        sql = "SELECT * FROM tb_pay_detail WHERE Pid=%s ORDER BY PDid"
        return self._query_all(sql, (pid,))

    def get_by_gid(self, gid: str):
        sql = "SELECT * FROM tb_pay_detail WHERE Gid=%s ORDER BY PDid DESC"
        return self._query_all(sql, (gid,))

    def add_and_refresh(self, detail: PayDetail) -> int:
        """新增明细并同步更新主表汇总"""
        new_id = self.add(detail)
        self.refresh_main_total(detail.pid)
        return new_id

    def update_and_refresh(self, detail: PayDetail) -> int:
        """修改明细并同步更新主表汇总"""
        rows = self.update(detail)
        if rows > 0:
            self.refresh_main_total(detail.pid)
        return rows

    def refresh_main_total(self, pid: int) -> int:
        """根据明细重新统计主表总数量和总金额"""
        sql = """
        UPDATE tb_pay_main
        SET
            Pcount = (
                SELECT IFNULL(SUM(Pcount2), 0)
                FROM tb_pay_detail
                WHERE Pid = %s
            ),
            Ptotal = (
                SELECT IFNULL(SUM(total), 0)
                FROM tb_pay_detail
                WHERE Pid = %s
            )
        WHERE Pid = %s
        """
        return DBHelper.execute_update(sql, (pid, pid, pid))