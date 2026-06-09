# -*- coding: utf-8 -*-
"""员工业务逻辑层"""

from dao.employee_dao import EmployeeDAO
from models.employee import Employee


class EmployeeService:
    """员工业务逻辑"""

    def __init__(self):
        self.employee_dao = EmployeeDAO()

    def add_employee(self, employee: Employee) -> tuple[bool, str]:
        """新增员工"""
        valid, msg = employee.validate()
        if not valid:
            return False, msg

        old = self.employee_dao.get_by_id(employee.eid)
        if old:
            return False, f"员工编号 {employee.eid} 已存在"

        try:
            rows = self.employee_dao.add(employee)
            return rows > 0, "员工新增成功" if rows > 0 else "员工新增失败"
        except Exception as e:
            return False, f"员工新增失败：{e}"

    def update_employee(self, employee: Employee) -> tuple[bool, str]:
        """修改员工"""
        valid, msg = employee.validate()
        if not valid:
            return False, msg

        old = self.employee_dao.get_by_id(employee.eid)
        if not old:
            return False, f"员工编号 {employee.eid} 不存在"

        try:
            rows = self.employee_dao.update(employee)
            return rows > 0, "员工修改成功" if rows > 0 else "员工修改失败"
        except Exception as e:
            return False, f"员工修改失败：{e}"

    def delete_employee(self, eid: str) -> tuple[bool, str]:
        """删除员工"""
        old = self.employee_dao.get_by_id(eid)
        if not old:
            return False, f"员工编号 {eid} 不存在"

        try:
            rows = self.employee_dao.delete(eid)
            return rows > 0, "员工删除成功" if rows > 0 else "员工删除失败"
        except Exception as e:
            return False, f"员工删除失败：{e}"

    def get_employee_by_id(self, eid: str):
        """按编号查询员工"""
        return self.employee_dao.get_by_id(eid)

    def get_all_employees(self):
        """查询全部员工"""
        return self.employee_dao.get_all()

    def login(self, eid: str, epas: str) -> tuple[bool, str, Employee | None]:
        """员工登录"""
        if not eid or not epas:
            return False, "账号和密码不能为空", None

        employee = self.employee_dao.login(eid, epas)
        if not employee:
            return False, "账号或密码错误", None

        return True, "登录成功", employee

    def search_by_name(self, keyword: str):
        """按姓名模糊查询"""
        return self.employee_dao.search_by_name(keyword)

    def search_by_level(self, elevel: str):
        """按级别精确查询"""
        return self.employee_dao.search_by_level(elevel)

    def search_by_salary_range(self, min_salary: float, max_salary: float):
        """按工资范围查询"""
        return self.employee_dao.search_by_salary_range(min_salary, max_salary)