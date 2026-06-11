# -*- coding: utf-8 -*-
"""统计查询测试"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.statistics_service import StatisticsService


def test_employee_statistics():
    service = StatisticsService()
    result = service.get_employee_statistics()

    print("========== 员工统计 ==========")
    print("员工总人数：", result['total_count'])
    print("员工级别统计：", result['level_statistics'])
    print("工资统计：", result['salary_statistics'])
    print("员工信息：", result['employees'])


def test_good_statistics():
    service = StatisticsService()
    result = service.get_good_statistics()

    print("========== 商品统计 ==========")
    print("商品总数：", result['total_count'])
    print("价格统计：", result['price_statistics'])
    print("供应商商品统计：", result['customer_statistics'])
    print("商品信息：", result['goods'])


def test_purchase_statistics():
    service = StatisticsService()
    result = service.get_purchase_statistics()

    print("========== 采购统计 ==========")
    print("采购单总数：", result['total_count'])
    print("采购主表统计：", result['main_statistics'])
    print("员工采购统计：", result['employee_statistics'])
    print("采购明细统计：", result['detail_statistics'])
    print("商品采购排行：", result['goods_purchase_rank'])
    print("采购主表信息：", result['pay_main_list'])


def test_purchase_statistics_by_date_range():
    service = StatisticsService()
    result = service.get_purchase_statistics_by_date_range('20200101', '20300101')

    print("========== 日期范围采购统计 ==========")
    print("起始日期：", result['start_date'])
    print("结束日期：", result['end_date'])
    print("统计结果：", result['date_statistics'])


if __name__ == '__main__':
    test_employee_statistics()
    test_good_statistics()
    test_purchase_statistics()
    test_purchase_statistics_by_date_range()