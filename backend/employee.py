# -*- coding: utf-8 -*-
"""员工实体类"""

from dataclasses import dataclass
from typing import Optional
from models.base import BaseEntity

@dataclass
class Employee(BaseEntity):
    """员工实体"""
    eid: str = ''                    # 员工编号 (主键)
    ename: str = ''                  # 员工姓名
    epas: str = ''                   # 登录密码
    elevel: str = ''                 # 员工级别 (00/10/20)
    etel_phone: str = ''             # 员工电话
    esalary: float = 0.0             # 员工工资
    other: str = ''                  # 备注
    
    # 级别常量
    LEVEL_ADMIN = '00'       # 管理员
    LEVEL_MANAGER = '10'     # 主管
    LEVEL_ORDINARY = '20'    # 采购员
    
    def get_level_name(self) -> str:
        """获取级别中文名称"""
        level_map = {
            self.LEVEL_ADMIN: '管理员',
            self.LEVEL_MANAGER: '主管',
            self.LEVEL_ORDINARY: '采购员'
        }
        return level_map.get(self.elevel, '未知')
    
    def is_admin(self) -> bool:
        """判断是否为管理员"""
        return self.elevel == self.LEVEL_ADMIN
    
    def validate(self) -> tuple[bool, str]:
        """数据验证"""
        if not self.eid:
            return False, "员工编号不能为空"
        if not self.eid.startswith('yg'):
            return False, "员工编号必须以 yg 开头"
        if not self.ename:
            return False, "员工姓名不能为空"
        if not self.epas:
            return False, "密码不能为空"
        if self.elevel not in [self.LEVEL_ADMIN, self.LEVEL_MANAGER, self.LEVEL_ORDINARY]:
            return False, "员工级别必须是 00/10/20"
        if len(self.etel_phone) != 11:
            return False, "手机号必须是 11 位"
        return True, "验证通过"