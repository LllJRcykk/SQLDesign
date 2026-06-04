# -*- coding: utf-8 -*-
"""商品实体类"""

from dataclasses import dataclass
from typing import Optional
from models.base import BaseEntity

@dataclass
class Good(BaseEntity):
    """商品实体"""
    gid: str = ''                      # 商品编号 (主键)
    gname: str = ''                    # 商品名称
    gpay: float = 0.0                  # 商品单价
    cid: str = ''                      # 供应商编号 (外键)
    gintroduction: str = ''            # 商品简介
    other: str = ''                    # 备注
    
    def validate(self) -> tuple[bool, str]:
        """数据验证"""
        if not self.gid:
            return False, "商品编号不能为空"
        if not self.gid.startswith('sp'):
            return False, "商品编号必须以 sp 开头"
        if not self.gname:
            return False, "商品名称不能为空"
        if self.gpay <= 0:
            return False, "商品单价必须大于 0"
        if not self.cid:
            return False, "供应商编号不能为空"
        return True, "验证通过"