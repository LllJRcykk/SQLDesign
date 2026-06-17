# -*- coding: utf-8 -*-
"""DAO 层统一导出"""

from DAO.employee_dao import EmployeeDAO
from DAO.customer_dao import CustomerDAO
from DAO.good_dao import GoodDAO
from DAO.pay_main_dao import PayMainDAO
from DAO.pay_detail_dao import PayDetailDAO

__all__ = [
    'EmployeeDAO',
    'CustomerDAO',
    'GoodDAO',
    'PayMainDAO',
    'PayDetailDAO'
]