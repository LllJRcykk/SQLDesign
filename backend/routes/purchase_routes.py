# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from models.pay_main import PayMain
from models.pay_detail import PayDetail
from services.purchase_service import PurchaseService

purchase_bp = Blueprint('purchase', __name__)
service = PurchaseService()


@purchase_bp.route('/main', methods=['GET'])
def get_all_pay_main():
    data = service.get_all_pay_main()
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@purchase_bp.route('/main/<int:pid>', methods=['GET'])
def get_pay_main_by_id(pid):
    data = service.get_pay_main_by_id(pid)
    if not data:
        return jsonify({'success': False, 'msg': '采购主表不存在'}), 404
    return jsonify({'success': True, 'data': data.to_dict()})


@purchase_bp.route('/main', methods=['POST'])
def create_pay_main():
    data = request.get_json()
    pay_main = PayMain.from_dict(data)
    success, msg, pid = service.create_pay_main(pay_main)
    return jsonify({'success': success, 'msg': msg, 'pid': pid})


@purchase_bp.route('/main/<int:pid>', methods=['PUT'])
def update_pay_main(pid):
    data = request.get_json()
    data['pid'] = pid
    pay_main = PayMain.from_dict(data)
    success, msg = service.update_pay_main(pay_main)
    return jsonify({'success': success, 'msg': msg})


@purchase_bp.route('/main/<int:pid>', methods=['DELETE'])
def delete_pay_main(pid):
    success, msg = service.delete_pay_main(pid)
    return jsonify({'success': success, 'msg': msg})


@purchase_bp.route('/detail/<int:pdid>', methods=['GET'])
def get_pay_detail_by_id(pdid):
    data = service.get_pay_detail_by_id(pdid)
    if not data:
        return jsonify({'success': False, 'msg': '采购明细不存在'}), 404
    return jsonify({'success': True, 'data': data.to_dict()})


@purchase_bp.route('/detail', methods=['POST'])
def add_pay_detail():
    data = request.get_json()
    detail = PayDetail.from_dict(data)
    success, msg, pdid = service.add_pay_detail(detail)
    return jsonify({'success': success, 'msg': msg, 'pdid': pdid})


@purchase_bp.route('/detail/<int:pdid>', methods=['PUT'])
def update_pay_detail(pdid):
    data = request.get_json()
    data['pdid'] = pdid
    detail = PayDetail.from_dict(data)
    success, msg = service.update_pay_detail(detail)
    return jsonify({'success': success, 'msg': msg})


@purchase_bp.route('/detail/<int:pdid>', methods=['DELETE'])
def delete_pay_detail(pdid):
    success, msg = service.delete_pay_detail(pdid)
    return jsonify({'success': success, 'msg': msg})


@purchase_bp.route('/details/<int:pid>', methods=['GET'])
def get_details_by_pid(pid):
    data = service.get_details_by_pid(pid)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@purchase_bp.route('/full/<int:pid>', methods=['GET'])
def get_pay_main_with_details(pid):
    data = service.get_pay_main_with_details(pid)
    if not data:
        return jsonify({'success': False, 'msg': '采购单不存在'}), 404
    result = data.to_dict()
    result['details'] = [item.to_dict() for item in data.details]
    return jsonify({'success': True, 'data': result})


@purchase_bp.route('/search/date', methods=['GET'])
def search_pay_main_by_date():
    pdate = request.args.get('pdate', '')
    data = service.search_pay_main_by_date(pdate)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@purchase_bp.route('/search/date-range', methods=['GET'])
def search_pay_main_by_date_range():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    data = service.search_pay_main_by_date_range(start_date, end_date)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})
