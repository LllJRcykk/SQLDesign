# -*- coding: utf-8 -*-
"""采购业务逻辑层"""

from dao.employee_dao import EmployeeDAO
from dao.good_dao import GoodDAO
from dao.pay_main_dao import PayMainDAO
from dao.pay_detail_dao import PayDetailDAO

from models.pay_main import PayMain
from models.pay_detail import PayDetail


class PurchaseService:
    """采购业务逻辑"""

    def __init__(self):
        self.employee_dao = EmployeeDAO()
        self.good_dao = GoodDAO()
        self.pay_main_dao = PayMainDAO()
        self.pay_detail_dao = PayDetailDAO()

    def create_pay_main(self, pay_main: PayMain) -> tuple[bool, str, int | None]:
        """创建采购主表"""
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
        """修改采购主表"""
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
        """删除采购主表
        如果数据库外键设置了 ON DELETE CASCADE，则明细会自动删除
        """
        old = self.pay_main_dao.get_by_id(pid)
        if not old:
            return False, f"采购单号 {pid} 不存在"

        try:
            rows = self.pay_main_dao.delete(pid)
            return rows > 0, "采购主表删除成功" if rows > 0 else "采购主表删除失败"
        except Exception as e:
            return False, f"采购主表删除失败：{e}"

    def add_pay_detail(self, detail: PayDetail) -> tuple[bool, str, int | None]:
        """新增采购明细，并自动刷新主表汇总"""
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

        # 如果明细单价未给或不合理，可直接采用商品表单价
        if detail.gpay <= 0:
            detail.gpay = float(good.gpay)
            detail.calculate_total()

        try:
            pdid = self.pay_detail_dao.add_and_refresh(detail)
            return True, "采购明细新增成功", pdid
        except Exception as e:
            return False, f"采购明细新增失败：{e}", None

    def update_pay_detail(self, detail: PayDetail) -> tuple[bool, str]:
        """修改采购明细，并自动刷新主表汇总"""
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
        """删除采购明细，并自动刷新主表汇总"""
        old = self.pay_detail_dao.get_by_id(pdid)
        if not old:
            return False, f"采购明细号 {pdid} 不存在"

        try:
            rows = self.pay_detail_dao.delete(pdid)
            return rows > 0, "采购明细删除成功" if rows > 0 else "采购明细删除失败"
        except Exception as e:
            return False, f"采购明细删除失败：{e}"

    def get_pay_main_by_id(self, pid: int):
        """按主键查询采购主表"""
        return self.pay_main_dao.get_by_id(pid)

    def get_all_pay_main(self):
        """查询全部采购主表"""
        return self.pay_main_dao.get_all()

    def get_pay_detail_by_id(self, pdid: int):
        """按主键查询采购明细"""
        return self.pay_detail_dao.get_by_id(pdid)

    def get_details_by_pid(self, pid: int):
        """查询某采购单下全部明细"""
        return self.pay_detail_dao.get_by_pid(pid)

    def search_pay_main_by_date(self, pdate: str):
        """按日期精确查询采购主表"""
        return self.pay_main_dao.search_by_date(pdate)

    def search_pay_main_by_date_range(self, start_date: str, end_date: str):
        """按日期范围查询采购主表"""
        return self.pay_main_dao.search_by_date_range(start_date, end_date)

    def get_pay_main_with_details(self, pid: int):
        """获取采购主表及其明细"""
        pay_main = self.pay_main_dao.get_by_id(pid)
        if not pay_main:
            return None

        details = self.pay_detail_dao.get_by_pid(pid)
        pay_main.details = details
        return pay_main