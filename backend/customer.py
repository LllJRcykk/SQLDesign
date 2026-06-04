# -*- coding: utf-8 -*-
"""客户/供应商实体类"""

from dataclasses import dataclass
from typing import Optional
from models.base import BaseEntity

@dataclass
class Customer(BaseEntity):
    """客户实体"""
    cid: str = ''                      # 客户编号 (主键)
    ccompany_name: str = ''            # 客户真实姓名
    ccompany_sname: str = ''           # 客户简称
    ccompany_address: str = ''         # 通讯地址
    ccompany_phone: str = ''           # 公司座机电话
    cemail: str = ''                   # 邮件
    cname: str = ''                    # 联系人名字
    ctel_phone: str = ''               # 联系人移动电话
    other: str = ''                    # 备注
    
    def validate(self) -> tuple[bool, str]:
        """数据验证"""
        if not self.cid:
            return False, "客户编号不能为空"
        if not self.cid.startswith('gys'):
            return False, "客户编号必须以 gys 开头"
        if not self.ccompany_name:
            return False, "客户名称不能为空"
        if not self.cname:
            return False, "联系人不能为空"
        return True, "验证通过"