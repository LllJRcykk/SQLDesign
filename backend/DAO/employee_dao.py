# -*- coding: utf-8 -*-
"""员工 DAO"""

from DAO.base_dao import BaseDAO
from models.employee import Employee


class EmployeeDAO(BaseDAO):
    """员工数据访问对象"""

    def __init__(self):
        super().__init__(Employee)

    def add(self, employee: Employee) -> int:
        sql = """
        INSERT INTO tb_employee
        (Eid, EName, EPas, Elevel, EtelPhone, ESalary, other)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self._update(sql, (
            employee.eid,
            employee.ename,
            employee.epas,
            employee.elevel,
            employee.etel_phone,
            employee.esalary,
            employee.other
        ))

    def update(self, employee: Employee) -> int:
        sql = """
        UPDATE tb_employee
        SET EName=%s, EPas=%s, Elevel=%s, EtelPhone=%s, ESalary=%s, other=%s
        WHERE Eid=%s
        """
        return self._update(sql, (
            employee.ename,
            employee.epas,
            employee.elevel,
            employee.etel_phone,
            employee.esalary,
            employee.other,
            employee.eid
        ))

    def delete(self, eid: str) -> int:
        sql = "DELETE FROM tb_employee WHERE Eid=%s"
        return self._update(sql, (eid,))

    def get_by_id(self, eid: str):
        sql = "SELECT * FROM tb_employee WHERE Eid=%s"
        return self._query_one(sql, (eid,))

    def get_all(self):
        sql = "SELECT * FROM tb_employee ORDER BY Eid"
        return self._query_all(sql)

    def login(self, eid: str, epas: str):
        sql = "SELECT * FROM tb_employee WHERE Eid=%s AND EPas=%s"
        return self._query_one(sql, (eid, epas))

    def search_by_name(self, keyword: str):
        sql = "SELECT * FROM tb_employee WHERE EName LIKE %s ORDER BY Eid"
        return self._query_all(sql, (f"%{keyword}%",))

    def search_by_level(self, elevel: str):
        sql = "SELECT * FROM tb_employee WHERE Elevel=%s ORDER BY Eid"
        return self._query_all(sql, (elevel,))

    def search_by_salary_range(self, min_salary: float, max_salary: float):
        sql = """
        SELECT * FROM tb_employee
        WHERE ESalary BETWEEN %s AND %s
        ORDER BY ESalary
        """
        return self._query_all(sql, (min_salary, max_salary))