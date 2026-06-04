# -*- coding: utf-8 -*-
"""实体基类 - 提供通用方法"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class BaseEntity:
    """实体基类，提供通用转换方法"""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（排除 None 值）"""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def to_json(self) -> str:
        """转换为 JSON 字符串（供前端使用）"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEntity':
        """从字典创建实体对象"""
        # 过滤掉字典中不存在的字段
        valid_keys = cls.__dataclass_fields__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)
    
    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> 'BaseEntity':
        """从数据库查询结果行创建实体（处理字段名映射）"""
        # 将数据库字段名（如 Eid）转换为 Python 字段名（如 eid）
        mapping = {
            'Eid': 'eid', 'EName': 'ename', 'EPas': 'epas', 'Elevel': 'elevel',
            'EtelPhone': 'etel_phone', 'ESalary': 'esalary',
            'Cid': 'cid', 'CcompanyName': 'ccompany_name', 'CcompanySName': 'ccompany_sname',
            'CcompanyAddress': 'ccompany_address', 'CcompanyPhone': 'ccompany_phone',
            'Cemail': 'cemail', 'CName': 'cname', 'CtelPhone': 'ctel_phone',
            'Gid': 'gid', 'GName': 'gname', 'GPay': 'gpay', 'GIntroduction': 'gintroduction',
            'Pid': 'pid', 'Pcount': 'pcount', 'Ptotal': 'ptotal', 'Pdate': 'pdate',
            'PDid': 'pdid', 'Pcount2': 'pcount2', 'Gpay': 'gpay', 'total': 'total',
            'other': 'other'
        }
        
        mapped_data = {}
        for db_key, py_key in mapping.items():
            if db_key in row:
                mapped_data[py_key] = row[db_key]
        
        # 补充未映射的字段
        for key, value in row.items():
            if key not in mapping:
                mapped_data[key.lower()] = value
        
        return cls.from_dict(mapped_data)