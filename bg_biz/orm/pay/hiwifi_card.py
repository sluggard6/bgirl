# -*- coding:utf-8 -*-
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]

from datetime import datetime

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP
from luhu_sharper.flaskapp.orm.base import BaseModel
from luhu_biz.orm.user import User

class HiwifiCard(BaseModel):
    __tablename__ = 'hiwifi_card'
    __table_args__ = {}

    class Status(DisplayEnum):
        USED = 2
        NEW = 1
        __display_cn__ = {
            USED: u'已使用',
            NEW: u'未使用'
        }

    class Category(DisplayEnum):
        WIFI = 1
        __display_cn__ = {
            WIFI: u'购买上网权限',
        }



    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(u'user_id', INTEGER(), nullable=True)
    num = Column(u'num', INTEGER(), nullable=True)
    status = Column(u'status', INTEGER(), nullable=True, default=Status.NEW)
    category = Column(u'category', INTEGER(), nullable=True, default=Category.WIFI)
    pay_by = Column(u'pay_by', INTEGER(), nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @property
    def status_cn(self):
        return self.Status.get_display_cn(self.status)

    @property
    def user(self):
        return User.get(self.user_id) if self.user_id else None


