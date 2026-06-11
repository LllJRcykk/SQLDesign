# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from services.employee_service import EmployeeService
from services.customer_service import CustomerService
from services.good_service import GoodService
from services.purchase_service import PurchaseService
from services.statistics_service import StatisticsService

export_bp = Blueprint('export', __name__)

employee_service = EmployeeService()
customer_service = CustomerService()
good_service = GoodService()
purchase_service = PurchaseService()
statistics_service = StatisticsService()


@export_bp.route('/employees', methods=['GET'])
def export_employees():
    success, msg = employee_service.export_employees_to_csv()
    return jsonify({'success': success, 'msg': msg})


@export_bp.route('/customers', methods=['GET'])
def export_customers():
    success, msg = customer_service.export_customers_to_csv()
    return jsonify({'success': success, 'msg': msg})


@export_bp.route('/goods', methods=['GET'])
def export_goods():
    success, msg = good_service.export_goods_to_csv()
    return jsonify({'success': success, 'msg': msg})


@export_bp.route('/pay-main', methods=['GET'])
def export_pay_main():
    success, msg = purchase_service.export_pay_main_to_csv()
    return jsonify({'success': success, 'msg': msg})


@export_bp.route('/pay-detail', methods=['GET'])
def export_pay_detail():
    success, msg = purchase_service.export_pay_detail_to_csv()
    return jsonify({'success': success, 'msg': msg})


@export_bp.route('/statistics/employees', methods=['GET'])
def export_employee_statistics():
    success, msg = statistics_service.export_employee_statistics_to_csv()
    return jsonify({'success': success, 'msg': msg})


@export_bp.route('/statistics/goods', methods=['GET'])
def export_good_statistics():
    success, msg = statistics_service.export_good_statistics_to_csv()
    return jsonify({'success': success, 'msg': msg})


@export_bp.route('/statistics/purchases', methods=['GET'])
def export_purchase_statistics():
    success, msg = statistics_service.export_purchase_statistics_to_csv()
    return jsonify({'success': success, 'msg': msg})
