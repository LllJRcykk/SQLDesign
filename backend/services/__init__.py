# -*- coding: utf-8 -*-
"""Service 层统一导出"""

from services.employee_service import EmployeeService
from services.customer_service import CustomerService
from services.good_service import GoodService
from services.purchase_service import PurchaseService

__all__ = [
    'EmployeeService',
    'CustomerService',
    'GoodService',
    'PurchaseService'
]