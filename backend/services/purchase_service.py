# -*- coding: utf-8 -*-
"""采购业务逻辑层"""

import os
from DAO.employee_dao import EmployeeDAO
from DAO.good_dao import GoodDAO
from DAO.pay_main_dao import PayMainDAO
from DAO.pay_detail_dao import PayDetailDAO

from models.pay_main import PayMain
from models.pay_detail import PayDetail
from utils.csv_exporter import CSVExporter


class PurchaseService:
    """采购业务逻辑"""

    def __init__(self):
        self.employee_dao = EmployeeDAO()
        self.good_dao = GoodDAO()
        self.pay_main_dao = PayMainDAO()
        self.pay_detail_dao = PayDetailDAO()

    def create_pay_main(self, pay_main: PayMain) -> tuple[bool, str, int | None]:
        valid, msg = pay_main.validate()
        if not valid:
            return False, msg, None

        employee = self.employee_dao.get_by_id(pay_main.eid)
        if not employee:
            return False, f"员工编号 {pay_main.eid} 不存在", None

        try:
            pid = self.pay_main_dao.add(pay_main)
            return True, "采购主表新增成功", pid
        except Exception as e:
            return False, f"采购主表新增失败：{e}", None

    def update_pay_main(self, pay_main: PayMain) -> tuple[bool, str]:
        valid, msg = pay_main.validate()
        if not valid:
            return False, msg

        old = self.pay_main_dao.get_by_id(pay_main.pid)
        if not old:
            return False, f"采购单号 {pay_main.pid} 不存在"

        employee = self.employee_dao.get_by_id(pay_main.eid)
        if not employee:
            return False, f"员工编号 {pay_main.eid} 不存在"

        try:
            rows = self.pay_main_dao.update(pay_main)
            return rows > 0, "采购主表修改成功" if rows > 0 else "采购主表修改失败"
        except Exception as e:
            return False, f"采购主表修改失败：{e}"

    def delete_pay_main(self, pid: int) -> tuple[bool, str]:
        old = self.pay_main_dao.get_by_id(pid)
        if not old:
            return False, f"采购单号 {pid} 不存在"

        try:
            rows = self.pay_main_dao.delete(pid)
            return rows > 0, "采购主表删除成功" if rows > 0 else "采购主表删除失败"
        except Exception as e:
            return False, f"采购主表删除失败：{e}"

    def add_pay_detail(self, detail: PayDetail) -> tuple[bool, str, int | None]:
        if detail.total <= 0:
            detail.calculate_total()

        valid, msg = detail.validate()
        if not valid:
            return False, msg, None

        pay_main = self.pay_main_dao.get_by_id(detail.pid)
        if not pay_main:
            return False, f"采购单号 {detail.pid} 不存在", None

        good = self.good_dao.get_by_id(detail.gid)
        if not good:
            return False, f"商品编号 {detail.gid} 不存在", None

        if detail.gpay <= 0:
            detail.gpay = float(good.gpay)
            detail.calculate_total()

        try:
            pdid = self.pay_detail_dao.add_and_refresh(detail)
            return True, "采购明细新增成功", pdid
        except Exception as e:
            return False, f"采购明细新增失败：{e}", None

    def update_pay_detail(self, detail: PayDetail) -> tuple[bool, str]:
        old = self.pay_detail_dao.get_by_id(detail.pdid)
        if not old:
            return False, f"采购明细号 {detail.pdid} 不存在"

        if detail.total <= 0:
            detail.calculate_total()

        valid, msg = detail.validate()
        if not valid:
            return False, msg

        pay_main = self.pay_main_dao.get_by_id(detail.pid)
        if not pay_main:
            return False, f"采购单号 {detail.pid} 不存在"

        good = self.good_dao.get_by_id(detail.gid)
        if not good:
            return False, f"商品编号 {detail.gid} 不存在"

        try:
            rows = self.pay_detail_dao.update_and_refresh(detail)
            return rows > 0, "采购明细修改成功" if rows > 0 else "采购明细修改失败"
        except Exception as e:
            return False, f"采购明细修改失败：{e}"

    def delete_pay_detail(self, pdid: int) -> tuple[bool, str]:
        old = self.pay_detail_dao.get_by_id(pdid)
        if not old:
            return False, f"采购明细号 {pdid} 不存在"

        try:
            rows = self.pay_detail_dao.delete(pdid)
            return rows > 0, "采购明细删除成功" if rows > 0 else "采购明细删除失败"
        except Exception as e:
            return False, f"采购明细删除失败：{e}"

    def get_pay_main_by_id(self, pid: int):
        return self.pay_main_dao.get_by_id(pid)

    def get_all_pay_main(self):
        return self.pay_main_dao.get_all()

    def get_pay_detail_by_id(self, pdid: int):
        return self.pay_detail_dao.get_by_id(pdid)

    def get_details_by_pid(self, pid: int):
        return self.pay_detail_dao.get_by_pid(pid)

    def search_pay_main_by_date(self, pdate: str):
        return self.pay_main_dao.search_by_date(pdate)

    def search_pay_main_by_date_range(self, start_date: str, end_date: str):
        return self.pay_main_dao.search_by_date_range(start_date, end_date)

    def get_pay_main_with_details(self, pid: int):
        pay_main = self.pay_main_dao.get_by_id(pid)
        if not pay_main:
            return None

        details = self.pay_detail_dao.get_by_pid(pid)
        pay_main.details = details
        return pay_main

    def export_pay_main_to_csv(self, file_path: str = 'exports/pay_main.csv') -> tuple[bool, str]:
        """导出采购主表到 CSV"""
        try:
            mains = self.pay_main_dao.get_all()
            headers = ['采购单号', '员工编号', '采购总数量', '采购总价', '采购日期', '备注']
            rows = []

            for m in mains:
                rows.append([
                    m.pid,
                    m.eid,
                    m.pcount,
                    m.ptotal,
                    m.pdate,
                    m.other
                ])

            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"采购主表导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"采购主表导出失败：{e}"

    def export_pay_detail_to_csv(self, file_path: str = 'exports/pay_detail.csv') -> tuple[bool, str]:
        """导出采购明细到 CSV"""
        try:
            details = self.pay_detail_dao.get_all()
            headers = ['采购明细号', '采购单号', '商品编号', '采购数量', '商品单价', '商品总价', '备注']
            rows = []

            for d in details:
                rows.append([
                    d.pdid,
                    d.pid,
                    d.gid,
                    d.pcount2,
                    d.gpay,
                    d.total,
                    d.other
                ])

            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"采购明细导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"采购明细导出失败：{e}"