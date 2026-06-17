# -*- coding: utf-8 -*-
"""DAO 层统一导出"""

from dao.employee_dao import EmployeeDAO
from dao.customer_dao import CustomerDAO
from dao.good_dao import GoodDAO
from dao.pay_main_dao import PayMainDAO
from dao.pay_detail_dao import PayDetailDAO

__all__ = [
    'EmployeeDAO',
    'CustomerDAO',
    'GoodDAO',
    'PayMainDAO',
    'PayDetailDAO'
]