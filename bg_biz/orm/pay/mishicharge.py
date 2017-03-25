# -*- coding:utf-8 -*-
from luhu_biz.orm.discount import DiscountRule
from luhu_biz.service.config_service import ConfigService
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]

from datetime import datetime

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP
from luhu_sharper.flaskapp.orm.base import BaseModel
from luhu_biz.orm.user import User

class Charge(BaseModel):
    __tablename__ = 'mishi_charge'
    __table_args__ = {}
    __bind_key__ = 'mishi'

    class AskStatus(DisplayEnum):
        NEW = 1
        PAYED = 2
        REJECT = 3
        __display_cn__ = {
            NEW: u'等待支付',
            PAYED: u'已支付',
            REJECT: u'已拒绝'
        }

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
        USER = 1
        SYSTEM = 2
        WIFI = 3
        __display_cn__ = {
            USER: u'用户',
            SYSTEM: u'系统',
            WIFI: u'购买上网权限',
        }

    class Source(DisplayEnum):
        WIFI = 1
        PORTAL_WIFI = 2
        THIRD_WIFI = 3
        __display_cn__ = {
            WIFI: u'购买上网权限',
            PORTAL_WIFI: u'portal购买上网时间',
            THIRD_WIFI: u'代理商充值上网时间'
        }


    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    phone = Column(u'phone', VARCHAR(32), nullable=True)
    amount = Column(u'amount', INTEGER(), nullable=True)
    paid = Column(u'paid', INTEGER(), nullable=True)
    status = Column(u'status', INTEGER(), nullable=True, default=Status.NEW)
    category = Column(u'category', INTEGER(), nullable=True, default=Category.USER)
    source = Column(u'source', INTEGER(), nullable=True)
    day = Column(u'day', INTEGER(), nullable=True)
    score = Column(u'score', INTEGER(), nullable=True)
    pay_by = Column(u'pay_by', INTEGER(), nullable=True)
    ask_for = Column(u'ask_for', INTEGER(), nullable=True)
    ask_for_status = Column(u'ask_for_status', INTEGER(), nullable=True)
    memo = Column(u'memo', VARCHAR(200), nullable=True)
    discount_info = Column(u'discount_info', VARCHAR(200), nullable=True)
    discount_id = Column(u'discount_id', INTEGER, nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @property
    def status_cn(self):
        return self.Status.get_display_cn(self.status)

    @property
    def ask_status_cn(self):
        return self.AskStatus.get_display_cn(self.ask_for_status)


    @property
    def source_cn(self):
        return self.Source.get_display_cn(self.source)

    @property
    def check_day(self):
        return ConfigService.get_wifi_day(self.amount/100,area_id=self.user.area_id)


    def _after_insert(self):
        """if self.discount_info:
            discount_rule = DiscountRule.query.filter_by(key=self.discount_info).first()
            if discount_rule and discount_rule.display_type!=DiscountRule.DisplayType.ALL:
                if discount_rule."""
        pass
class ChargeRecords(BaseModel):
    __tablename__ = 'mishi_charge_records'
    __table_args__ = {}
    __bind_key__ = 'mishi'

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
        USER = 1
        SYSTEM = 2
        WIFI = 3
        __display_cn__ = {
            USER: u'用户',
            SYSTEM: u'系统',
            WIFI: u'购买上网权限',
        }

    class ChargeType(DisplayEnum):
        WIFI = 1
        BALANCE = 2
        SCORE = 3
        __display_cn__ = {
            WIFI: u'上网时间',
            BALANCE: u'HI币',
            SCORE: u'HI点',
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    phone = Column(u'phone', INTEGER(), nullable=True)
    amount = Column(u'amount', INTEGER(), nullable=True)
    paid = Column(u'paid', INTEGER(), nullable=True)
    status = Column(u'status', INTEGER(), nullable=True, default=Status.NEW)
    category = Column(u'category', INTEGER(), nullable=True, default=Category.USER)
    charge_type = Column(u'charge_type', INTEGER(), nullable=True, default=ChargeType.BALANCE)
    source = Column(u'source', INTEGER(), nullable=True)
    charge_num = Column(u'charge_num', INTEGER(), nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @property
    def status_cn(self):
        return self.Status.get_display_cn(self.status)

