# -*- coding: utf-8 -*-
"""员工实体类"""

class Employee:
    def __init__(self, eid='', ename='', epas='', elevel='', etel_phone='', esalary=0.0, other=''):
        self.eid = eid              # 员工编号
        self.ename = ename          # 员工姓名
        self.epas = epas            # 登录密码
        self.elevel = elevel        # 员工级别
        self.etel_phone = etel_phone  # 员工电话
        self.esalary = esalary      # 员工工资
        self.other = other          # 备注
    
    def __str__(self):
        return f"员工[{self.eid}]: {self.ename}, 级别:{self.elevel}, 工资:{self.esalary}"
    
    def to_dict(self):
        """转换为字典，方便前端使用"""
        return {
            'eid': self.eid,
            'ename': self.ename,
            'epas': self.epas,
            'elevel': self.elevel,
            'etel_phone': self.etel_phone,
            'esalary': self.esalary,
            'other': self.other
        }
    
    @staticmethod
    def from_dict(data):
        """从字典创建对象"""
        return Employee(
            eid=data.get('eid', ''),
            ename=data.get('ename', ''),
            epas=data.get('epas', ''),
            elevel=data.get('elevel', ''),
            etel_phone=data.get('etel_phone', ''),
            esalary=data.get('esalary', 0.0),
            other=data.get('other', '')
        )