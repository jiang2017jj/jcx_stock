# -*- coding = utf-8 -*-
"""
@project:stock
@author:Jiang ChengLong
@file:models.py
@time:2020-05-08 13:44:58
"""

from stock import db

class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}