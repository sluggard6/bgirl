# -*- coding:utf-8 -*-
from datetime import datetime
from sharper.flaskapp.orm.display_enum import DisplayEnum

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP
from sharper.flaskapp.orm.base import BaseModel


__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class WifiCharge(BaseModel):
    __tablename__ = 'wifi_charge'
    __table_args__ = {}

    class Status(DisplayEnum):
        FINISHED = 2
        CANCELED = 3
        NEW = 1
        __display_cn__ = {
            FINISHED: u'已完成',
            CANCELED: u'已取消',
            NEW: u'未支付'
        }

    class Category(DisplayEnum):
        MONTH = 1
        DAY = 2

        __display_cn__ = {
            MONTH: u'包月',
            DAY: u'按天'
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(u'user_id', INTEGER(), nullable=True)
    amount = Column(u'amount', INTEGER(), nullable=True)
    category = Column(u'category', INTEGER(), nullable=True, default=Category.MONTH)
    account = Column(u'account', VARCHAR(length=32), nullable=False)
    month = Column(u'month', INTEGER(), nullable=True, default=1)
    day = Column(u'day', INTEGER(), nullable=True, default=1)
    status = Column(u'status', INTEGER(), nullable=True, default=1)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @property
    def status_cn(self):
        return self.Status.get_display_cn(self.status)


class WifiChargeRecord(BaseModel):
    __tablename__ = 'wifi_charge_record'
    __table_args__ = {}

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    wifi_account_id = Column(u'wifi_account_id', INTEGER(), nullable=True)
    amount = Column(u'amount', INTEGER(), nullable=True)
    month = Column(u'month', INTEGER(), nullable=True, default=1)
    net_start = Column(u'net_start', DATETIME(), nullable=True)
    net_end = Column(u'net_end', DATETIME(), nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)