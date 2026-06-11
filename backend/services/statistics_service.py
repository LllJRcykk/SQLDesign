# -*- coding: utf-8 -*-
"""统计查询业务逻辑层"""

import os
from utils.csv_exporter import CSVExporter
from dao.statistics_dao import StatisticsDAO


class StatisticsService:
    """统计查询业务逻辑"""

    def __init__(self):
        self.statistics_dao = StatisticsDAO()

    # =========================
    # 员工统计
    # =========================

    def get_employee_statistics(self) -> dict:
        """获取员工统计信息"""
        all_employees = self.statistics_dao.get_all_employees_raw()
        total_info = self.statistics_dao.count_employees()
        level_info = self.statistics_dao.count_employees_by_level()
        salary_info = self.statistics_dao.salary_statistics()

        return {
            'employees': all_employees,
            'total_count': total_info['total_count'],
            'level_statistics': level_info,
            'salary_statistics': salary_info
        }

    # =========================
    # 商品统计
    # =========================

    def get_good_statistics(self) -> dict:
        """获取商品统计信息"""
        all_goods = self.statistics_dao.get_all_goods_raw()
        total_info = self.statistics_dao.count_goods()
        price_info = self.statistics_dao.price_statistics()
        customer_info = self.statistics_dao.count_goods_by_customer()

        return {
            'goods': all_goods,
            'total_count': total_info['total_count'],
            'price_statistics': price_info,
            'customer_statistics': customer_info
        }

    # =========================
    # 采购统计
    # =========================

    def get_purchase_statistics(self) -> dict:
        """获取采购统计信息"""
        all_pay_main = self.statistics_dao.get_all_pay_main_raw()
        total_info = self.statistics_dao.count_pay_main()
        main_info = self.statistics_dao.pay_main_statistics()
        employee_info = self.statistics_dao.count_pay_by_employee()
        detail_info = self.statistics_dao.pay_detail_statistics()
        goods_rank = self.statistics_dao.count_goods_purchase_rank()

        return {
            'pay_main_list': all_pay_main,
            'total_count': total_info['total_count'],
            'main_statistics': main_info,
            'employee_statistics': employee_info,
            'detail_statistics': detail_info,
            'goods_purchase_rank': goods_rank
        }

    def get_purchase_statistics_by_date_range(self, start_date: str, end_date: str) -> dict:
        """按日期范围获取采购统计"""
        date_info = self.statistics_dao.pay_statistics_by_date_range(start_date, end_date)
        return {
            'start_date': start_date,
            'end_date': end_date,
            'date_statistics': date_info
        }
    def export_employee_statistics_to_csv(self, file_path: str = 'exports/employee_statistics.csv') -> tuple[bool, str]:
        """导出员工级别统计到 CSV"""
        try:
            data = self.statistics_dao.count_employees_by_level()
            headers = ['员工级别', '人数']
            rows = [[item['Elevel'], item['level_count']] for item in data]
            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"员工统计导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"员工统计导出失败：{e}"

    def export_good_statistics_to_csv(self, file_path: str = 'exports/good_statistics.csv') -> tuple[bool, str]:
        """导出供应商商品统计到 CSV"""
        try:
            data = self.statistics_dao.count_goods_by_customer()
            headers = ['供应商编号', '供应商名称', '商品数量']
            rows = [[item['Cid'], item['CcompanyName'], item['goods_count']] for item in data]
            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"商品统计导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"商品统计导出失败：{e}"

    def export_purchase_statistics_to_csv(self, file_path: str = 'exports/purchase_statistics.csv') -> tuple[bool, str]:
        """导出员工采购统计到 CSV"""
        try:
            data = self.statistics_dao.count_pay_by_employee()
            headers = ['员工编号', '员工姓名', '采购单数', '采购总金额']
            rows = [[item['Eid'], item['EName'], item['pay_count'], item['total_amount']] for item in data]
            CSVExporter.export_to_csv(file_path, headers, rows)
            return True, f"采购统计导出成功：{os.path.abspath(file_path)}"
        except Exception as e:
            return False, f"采购统计导出失败：{e}"