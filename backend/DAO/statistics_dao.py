# -*- coding: utf-8 -*-
"""统计查询 DAO"""

from dao.db_helper import DBHelper


class StatisticsDAO:
    """统计查询数据访问对象"""

    # =========================
    # 员工统计
    # =========================

    def get_all_employees_raw(self):
        """查询所有员工信息"""
        sql = "SELECT * FROM tb_employee ORDER BY Eid"
        return DBHelper.execute_query_all(sql)

    def count_employees(self):
        """统计员工总人数"""
        sql = "SELECT COUNT(*) AS total_count FROM tb_employee"
        return DBHelper.execute_query_one(sql)

    def count_employees_by_level(self):
        """按员工级别统计人数"""
        sql = """
        SELECT Elevel, COUNT(*) AS level_count
        FROM tb_employee
        GROUP BY Elevel
        ORDER BY Elevel
        """
        return DBHelper.execute_query_all(sql)

    def salary_statistics(self):
        """工资统计"""
        sql = """
        SELECT
            IFNULL(SUM(ESalary), 0) AS total_salary,
            IFNULL(AVG(ESalary), 0) AS avg_salary,
            IFNULL(MAX(ESalary), 0) AS max_salary,
            IFNULL(MIN(ESalary), 0) AS min_salary
        FROM tb_employee
        """
        return DBHelper.execute_query_one(sql)

    # =========================
    # 商品统计
    # =========================

    def get_all_goods_raw(self):
        """查询所有商品信息"""
        sql = "SELECT * FROM tb_good ORDER BY Gid"
        return DBHelper.execute_query_all(sql)

    def count_goods(self):
        """统计商品总数"""
        sql = "SELECT COUNT(*) AS total_count FROM tb_good"
        return DBHelper.execute_query_one(sql)

    def price_statistics(self):
        """商品价格统计"""
        sql = """
        SELECT
            IFNULL(SUM(GPay), 0) AS total_price,
            IFNULL(AVG(GPay), 0) AS avg_price,
            IFNULL(MAX(GPay), 0) AS max_price,
            IFNULL(MIN(GPay), 0) AS min_price
        FROM tb_good
        """
        return DBHelper.execute_query_one(sql)

    def count_goods_by_customer(self):
        """按供应商统计商品数量"""
        sql = """
        SELECT
            c.Cid,
            c.CcompanyName,
            COUNT(g.Gid) AS goods_count
        FROM tb_customer c
        LEFT JOIN tb_good g ON c.Cid = g.Cid
        GROUP BY c.Cid, c.CcompanyName
        ORDER BY c.Cid
        """
        return DBHelper.execute_query_all(sql)

    # =========================
    # 采购统计
    # =========================

    def get_all_pay_main_raw(self):
        """查询所有采购主表信息"""
        sql = "SELECT * FROM tb_pay_main ORDER BY Pid DESC"
        return DBHelper.execute_query_all(sql)

    def count_pay_main(self):
        """统计采购单总数"""
        sql = "SELECT COUNT(*) AS total_count FROM tb_pay_main"
        return DBHelper.execute_query_one(sql)

    def pay_main_statistics(self):
        """采购主表汇总统计"""
        sql = """
        SELECT
            IFNULL(SUM(Pcount), 0) AS total_goods_count,
            IFNULL(SUM(Ptotal), 0) AS total_amount,
            IFNULL(AVG(Ptotal), 0) AS avg_amount,
            IFNULL(MAX(Ptotal), 0) AS max_amount,
            IFNULL(MIN(Ptotal), 0) AS min_amount
        FROM tb_pay_main
        """
        return DBHelper.execute_query_one(sql)

    def count_pay_by_employee(self):
        """按员工统计采购单数与采购金额"""
        sql = """
        SELECT
            e.Eid,
            e.EName,
            COUNT(pm.Pid) AS pay_count,
            IFNULL(SUM(pm.Ptotal), 0) AS total_amount
        FROM tb_employee e
        LEFT JOIN tb_pay_main pm ON e.Eid = pm.Eid
        GROUP BY e.Eid, e.EName
        ORDER BY e.Eid
        """
        return DBHelper.execute_query_all(sql)

    def pay_statistics_by_date_range(self, start_date: str, end_date: str):
        """按日期范围统计采购信息"""
        sql = """
        SELECT
            COUNT(*) AS pay_count,
            IFNULL(SUM(Pcount), 0) AS total_goods_count,
            IFNULL(SUM(Ptotal), 0) AS total_amount
        FROM tb_pay_main
        WHERE Pdate BETWEEN %s AND %s
        """
        return DBHelper.execute_query_one(sql, (start_date, end_date))

    def pay_detail_statistics(self):
        """采购明细统计"""
        sql = """
        SELECT
            COUNT(*) AS detail_count,
            IFNULL(SUM(Pcount2), 0) AS total_detail_count,
            IFNULL(SUM(total), 0) AS total_detail_amount
        FROM tb_pay_detail
        """
        return DBHelper.execute_query_one(sql)

    def count_goods_purchase_rank(self):
        """按商品统计采购数量排行"""
        sql = """
        SELECT
            g.Gid,
            g.GName,
            IFNULL(SUM(pd.Pcount2), 0) AS total_purchase_count,
            IFNULL(SUM(pd.total), 0) AS total_purchase_amount
        FROM tb_good g
        LEFT JOIN tb_pay_detail pd ON g.Gid = pd.Gid
        GROUP BY g.Gid, g.GName
        ORDER BY total_purchase_count DESC, g.Gid
        """
        return DBHelper.execute_query_all(sql)