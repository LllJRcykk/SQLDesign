# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from models.employee import Employee
from services.employee_service import EmployeeService

employee_bp = Blueprint('employee', __name__)
service = EmployeeService()


@employee_bp.route('/', methods=['GET'])
def get_all_employees():
    data = service.get_all_employees()
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@employee_bp.route('/<eid>', methods=['GET'])
def get_employee_by_id(eid):
    data = service.get_employee_by_id(eid)
    if not data:
        return jsonify({'success': False, 'msg': '员工不存在'}), 404
    return jsonify({'success': True, 'data': data.to_dict()})


@employee_bp.route('/', methods=['POST'])
def add_employee():
    data = request.get_json()
    employee = Employee.from_dict(data)
    success, msg = service.add_employee(employee)
    return jsonify({'success': success, 'msg': msg})


@employee_bp.route('/<eid>', methods=['PUT'])
def update_employee(eid):
    data = request.get_json()
    data['eid'] = eid
    employee = Employee.from_dict(data)
    success, msg = service.update_employee(employee)
    return jsonify({'success': success, 'msg': msg})


@employee_bp.route('/<eid>', methods=['DELETE'])
def delete_employee(eid):
    success, msg = service.delete_employee(eid)
    return jsonify({'success': success, 'msg': msg})


@employee_bp.route('/search/name', methods=['GET'])
def search_employee_by_name():
    keyword = request.args.get('keyword', '')
    data = service.search_by_name(keyword)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@employee_bp.route('/search/level', methods=['GET'])
def search_employee_by_level():
    elevel = request.args.get('elevel', '')
    data = service.search_by_level(elevel)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@employee_bp.route('/search/salary', methods=['GET'])
def search_employee_by_salary():
    min_salary = float(request.args.get('min_salary', 0))
    max_salary = float(request.args.get('max_salary', 99999999))
    data = service.search_by_salary_range(min_salary, max_salary)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@employee_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    eid = data.get('eid', '')
    epas = data.get('epas', '')
    success, msg, employee = service.login(eid, epas)
    return jsonify({
        'success': success,
        'msg': msg,
        'data': employee.to_dict() if employee else None
    })