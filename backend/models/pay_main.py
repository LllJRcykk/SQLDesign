# -*- coding: utf-8 -*-
"""采购清单主表实体类"""

from dataclasses import dataclass
from typing import Optional, List
from models.base import BaseEntity

@dataclass
class PayMain(BaseEntity):
    """采购清单主表实体"""
    pid: int = 0                       # 采购清单号 (主键，自增)
    eid: str = ''                      # 员工编号 (外键)
    pcount: int = 0                    # 采购总数量
    ptotal: float = 0.0                # 采购总价
    pdate: str = ''                    # 采购时间 (8 位字符串)
    other: str = ''                    # 备注
    
    # 关联的采购明细列表（用于业务逻辑）
    details: List = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = []
    
    def validate(self) -> tuple[bool, str]:
        """数据验证"""
        if not self.eid:
            return False, "员工编号不能为空"
        if not self.pdate or len(self.pdate) != 8:
            return False, "采购时间必须是 8 位字符串 (如 20250101)"
        return True, "验证通过"
    
    def calculate_total(self, details: List) -> None:
        """根据明细计算总数量和总价"""
        self.pcount = sum(d.pcount2 for d in details)
        self.ptotal = sum(d.total for d in details)