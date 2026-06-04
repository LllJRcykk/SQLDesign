# -*- coding: utf-8 -*-
"""采购明细表实体类"""

from dataclasses import dataclass
from typing import Optional
from models.base import BaseEntity

@dataclass
class PayDetail(BaseEntity):
    """采购明细表实体"""
    pdid: int = 0                      # 采购明细号 (主键，自增)
    pid: int = 0                       # 采购清单号 (外键)
    gid: str = ''                      # 商品编号 (外键)
    pcount2: int = 0                   # 采购数量
    gpay: float = 0.0                  # 商品单价
    total: float = 0.0                 # 商品总价 (单价×数量)
    other: str = ''                    # 备注
    
    def validate(self) -> tuple[bool, str]:
        """数据验证"""
        if self.pid <= 0:
            return False, "采购清单号必须大于 0"
        if not self.gid:
            return False, "商品编号不能为空"
        if self.pcount2 <= 0:
            return False, "采购数量必须大于 0"
        if self.gpay <= 0:
            return False, "商品单价必须大于 0"
        return True, "验证通过"
    
    def calculate_total(self) -> None:
        """计算总价"""
        self.total = round(self.pcount2 * self.gpay, 2)