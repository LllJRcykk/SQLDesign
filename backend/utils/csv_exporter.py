# -*- coding: utf-8 -*-
"""CSV 导出工具"""

import csv
import os
from typing import List


class CSVExporter:
    """CSV 导出工具类"""

    @staticmethod
    def ensure_dir(directory: str):
        """确保目录存在"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def export_to_csv(file_path: str, headers: List[str], rows: List[List]):
        """导出为 CSV 文件"""
        directory = os.path.dirname(file_path)
        if directory:
            CSVExporter.ensure_dir(directory)

        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        return file_path