# -*- coding: utf-8 -*-
"""数据库连接管理类（单例模式）"""

import pymysql
from config.db_config import DB_CONFIG

class DBConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        """单例模式，确保只有一个数据库连接实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """获取数据库连接"""
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(**DB_CONFIG)
        return self._connection
    
    def close(self):
        """关闭数据库连接"""
        if self._connection and self._connection.open:
            self._connection.close()
            self._connection = None
    
    def __del__(self):
        """析构函数，确保连接关闭"""
        self.close()