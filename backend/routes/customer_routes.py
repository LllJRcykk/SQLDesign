# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from models.customer import Customer
from services.customer_service import CustomerService

customer_bp = Blueprint('customer', __name__)
service = CustomerService()


@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    data = service.get_all_customers()
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@customer_bp.route('/<cid>', methods=['GET'])
def get_customer_by_id(cid):
    data = service.get_customer_by_id(cid)
    if not data:
        return jsonify({'success': False, 'msg': '客户不存在'}), 404
    return jsonify({'success': True, 'data': data.to_dict()})


@customer_bp.route('/', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer = Customer.from_dict(data)
    success, msg = service.add_customer(customer)
    return jsonify({'success': success, 'msg': msg})


@customer_bp.route('/<cid>', methods=['PUT'])
def update_customer(cid):
    data = request.get_json()
    data['cid'] = cid
    customer = Customer.from_dict(data)
    success, msg = service.update_customer(customer)
    return jsonify({'success': success, 'msg': msg})


@customer_bp.route('/<cid>', methods=['DELETE'])
def delete_customer(cid):
    success, msg = service.delete_customer(cid)
    return jsonify({'success': success, 'msg': msg})


@customer_bp.route('/search/name', methods=['GET'])
def search_customer_by_name():
    keyword = request.args.get('keyword', '')
    data = service.search_by_name(keyword)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@customer_bp.route('/search/contact', methods=['GET'])
def search_customer_by_contact():
    keyword = request.args.get('keyword', '')
    data = service.search_by_contact(keyword)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})