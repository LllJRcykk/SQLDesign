# -*- coding: utf-8 -*-
"""数据库配置文件"""

from dataclasses import dataclass
import pymysql
@dataclass
class DatabaseConfig:
    """数据库配置数据类"""
    host: str = 'localhost'
    port: int = 3306
    user: str = 'root'
    password: str = '123456'
    database: str = 'design'
    charset: str = 'utf8mb4'
    
    def to_dict(self) -> dict:
        """转换为字典格式，供 pymysql 使用"""
        return {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'charset': self.charset,
            'cursorclass': pymysql.cursors.DictCursor,  # 使用字典游标
            'autocommit': False
        }

# 全局配置实例
DB_CONFIG = DatabaseConfig()
