# -*- coding: utf-8 -*-
"""员工业务逻辑层"""

import os
from dao.employee_dao import EmployeeDAO
from models.employee import Employee
from utils.csv_exporter import CSVExporter


class EmployeeService:
    """员工业务逻辑"""

    def __init__(self):
        self.employee_dao = EmployeeDAO()

    def add_employee(self, employee: Employee) -> tuple[bool, str]:
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
        old = self.employee_dao.get_by_id(eid)
        if not old:
            return False, f"员工编号 {eid} 不存在"

        try:
            rows = self.employee_dao.delete(eid)
            return rows > 0, "员工删除成功" if rows > 0 else "员工删除失败"
        except Exception as e:
            return False, f"员工删除失败：{e}"

    def get_employee_by_id(self, eid: str):
        return self.employee_dao.get_by_id(eid)

    def get_all_employees(self):
        return self.employee_dao.get_all()

    def login(self, eid: str, epas: str) -> tuple[bool, str, Employee | None]:
        if not eid or not epas:
            return False, "账号和密码不能为空", None

        employee = self.employee_dao.login(eid, epas)
        if not employee:
            return False, "账号或密码错误", None

        return True, "登录成功", employee

    def search_by_name(self, keyword: str):
        return self.employee_dao.search_by_name(keyword)

    def search_by_level(self, elevel: str):
        return self.employee_dao.search_by_level(elevel)

    def search_by_salary_range(self, min_salary: float, max_salary: float):
        return self.employee_dao.search_by_salary_range(min_salary, max_salary)

    def export_employees_to_csv(self, file_path: str = 'exports/employees.csv') -> tuple[bool, str]:
        """导出员工数据到 CSV"""
        try:
            employees = self.employee_dao.get_all()
            headers = ['员工编号', '员工姓名', '登录密码', '员工级别', '员工电话', '员工工资', '备注']
            rows = []

            for e in employees:
                rows.append([
                    e.eid,
                    e.ename,
                    e.epas,
                    e.elevel,
                    e.etel_phone,
                    e.esalary,
                    e.other
                ])

            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"员工数据导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"员工数据导出失败：{e}"