# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from services.statistics_service import StatisticsService

statistics_bp = Blueprint('statistics', __name__)
service = StatisticsService()


@statistics_bp.route('/employees', methods=['GET'])
def employee_statistics():
    data = service.get_employee_statistics()
    return jsonify({'success': True, 'data': data})


@statistics_bp.route('/goods', methods=['GET'])
def good_statistics():
    data = service.get_good_statistics()
    return jsonify({'success': True, 'data': data})


@statistics_bp.route('/purchases', methods=['GET'])
def purchase_statistics():
    data = service.get_purchase_statistics()
    return jsonify({'success': True, 'data': data})


@statistics_bp.route('/purchases/date-range', methods=['GET'])
def purchase_statistics_by_date_range():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    data = service.get_purchase_statistics_by_date_range(start_date, end_date)
    return jsonify({'success': True, 'data': data})
