# -*- coding: utf-8 -*-
"""DAO 基类"""

from dao.db_helper import DBHelper


class BaseDAO:
    """DAO 基类，封装通用查询方法"""

    def __init__(self, entity_class):
        self.entity_class = entity_class

    def _query_one(self, sql: str, params=None):
        """查询单个实体"""
        row = DBHelper.execute_query_one(sql, params)
        return self.entity_class.from_row(row) if row else None

    def _query_all(self, sql: str, params=None):
        """查询实体列表"""
        rows = DBHelper.execute_query_all(sql, params)
        return [self.entity_class.from_row(row) for row in rows]

    def _update(self, sql: str, params=None) -> int:
        """执行增删改"""
        return DBHelper.execute_update(sql, params)

    def _insert_return_id(self, sql: str, params=None) -> int:
        """执行插入并返回主键"""
        return DBHelper.execute_insert_return_id(sql, params)