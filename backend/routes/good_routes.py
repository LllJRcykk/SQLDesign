# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from models.good import Good
from services.good_service import GoodService

good_bp = Blueprint('good', __name__)
service = GoodService()


@good_bp.route('/', methods=['GET'])
def get_all_goods():
    data = service.get_all_goods()
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@good_bp.route('/<gid>', methods=['GET'])
def get_good_by_id(gid):
    data = service.get_good_by_id(gid)
    if not data:
        return jsonify({'success': False, 'msg': '商品不存在'}), 404
    return jsonify({'success': True, 'data': data.to_dict()})


@good_bp.route('/', methods=['POST'])
def add_good():
    data = request.get_json()
    good = Good.from_dict(data)
    success, msg = service.add_good(good)
    return jsonify({'success': success, 'msg': msg})


@good_bp.route('/<gid>', methods=['PUT'])
def update_good(gid):
    data = request.get_json()
    data['gid'] = gid
    good = Good.from_dict(data)
    success, msg = service.update_good(good)
    return jsonify({'success': success, 'msg': msg})


@good_bp.route('/<gid>', methods=['DELETE'])
def delete_good(gid):
    success, msg = service.delete_good(gid)
    return jsonify({'success': success, 'msg': msg})


@good_bp.route('/search/name', methods=['GET'])
def search_good_by_name():
    keyword = request.args.get('keyword', '')
    data = service.search_by_name(keyword)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@good_bp.route('/search/price', methods=['GET'])
def search_good_by_price():
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 99999999))
    data = service.search_by_price_range(min_price, max_price)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})


@good_bp.route('/customer/<cid>', methods=['GET'])
def get_goods_by_customer(cid):
    data = service.get_by_customer_id(cid)
    return jsonify({'success': True, 'data': [item.to_dict() for item in data]})
