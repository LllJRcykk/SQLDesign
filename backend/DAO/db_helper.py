# -*- coding: utf-8 -*-
"""数据库帮助类"""

import pymysql
from config.db_config import DB_CONFIG


class DBHelper:
    """数据库连接与通用操作帮助类"""

    @staticmethod
    def get_connection():
        """获取数据库连接"""
        return pymysql.connect(**DB_CONFIG.to_dict())

    @staticmethod
    def execute_update(sql: str, params=None) -> int:
        """执行 INSERT / UPDATE / DELETE"""
        conn = None
        try:
            conn = DBHelper.get_connection()
            with conn.cursor() as cursor:
                rows = cursor.execute(sql, params)
            conn.commit()
            return rows
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    @staticmethod
    def execute_insert_return_id(sql: str, params=None) -> int:
        """执行插入并返回自增主键"""
        conn = None
        try:
            conn = DBHelper.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                last_id = cursor.lastrowid
            conn.commit()
            return last_id
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    @staticmethod
    def execute_query_one(sql: str, params=None):
        """查询单条记录"""
        conn = None
        try:
            conn = DBHelper.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def execute_query_all(sql: str, params=None):
        """查询多条记录"""
        conn = None
        try:
            conn = DBHelper.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def execute_scalar(sql: str, params=None):
        """查询单个值"""
        row = DBHelper.execute_query_one(sql, params)
        if row:
            return list(row.values())[0]
        return None