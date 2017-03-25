# -*- coding:utf-8 -*-
from sharper.flaskapp.orm.display_enum import DisplayEnum

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]

from datetime import datetime

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP
from sharper.flaskapp.orm.base import BaseModel


class Consume(BaseModel):
    __tablename__ = 'consume'
    __table_args__ = {}

    class Status(DisplayEnum):
        FINISHED = 2
        CANCELED = 3
        NEW = 1
        __display_cn__ = {
            FINISHED: u'已完成',
            CANCELED: u'已取消',
            NEW: u'新建'
        }

    class Category(DisplayEnum):
        WIFI_CHARGE = 2
        OTHER_APP = 1
        BUY_SCORE = 3
        SALE_CHARGE = 4
        BUY_BOOK = 5
        PAY_THREAD = 6
        SYS = 999
        __display_cn__ = {
            WIFI_CHARGE: u"wifi包月",
            OTHER_APP: u"其他app",
            BUY_SCORE: u"购买Hi点",
            SYS: u"系统扣除",
            SALE_CHARGE:u"商城消费",
            BUY_BOOK:u"小说购买",
            PAY_THREAD:u"帖子付费"
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(u'user_id', INTEGER(), nullable=True)
    category = Column(u'category', INTEGER(), default=Category.OTHER_APP, nullable=True)
    total_price = Column(u'total_price', INTEGER(), nullable=True)
    quantity = Column(u'quantity', INTEGER(), nullable=True)
    price = Column(u'price', INTEGER(), nullable=True)
    app_id = Column(u'app_id', VARCHAR(length=32), nullable=True)
    subject = Column(u'subject', VARCHAR(length=128), nullable=True)
    desc = Column(u'desc', VARCHAR(length=512), nullable=True)
    out_trade_no = Column(u'out_trade_no', VARCHAR(length=64), nullable=True)
    consume_time = Column(u'consume_time', DATETIME(), nullable=True)
    status = Column(u'status', INTEGER(), nullable=True, default=1)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @property
    def status_cn(self):
        return self.Status.get_display_cn(self.status)

    @property
    def category_cn(self):
        return self.Category.get_display_cn(self.category)