# -*- coding:utf-8 -*-
from sharper.flaskapp.orm.display_enum import DisplayEnum
from sharper.util import app_util
from bg_biz.orm.pay.consume import Consume

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]

from datetime import datetime

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP, func
from sharper.flaskapp.orm.base import BaseModel, db


class AccountDetail(BaseModel):
    __tablename__ = 'account_detail'
    __table_args__ = {}

    class Category(DisplayEnum):
        CHARGE = 1
        CONSUME = 2
        BUYING = 3
        __display_cn__ = {
            CHARGE: u"充值",
            CONSUME: u"消费",
	    BUYING: u"疯狂抢购",
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    category = Column(u'category', INTEGER(), nullable=False)
    user_id = Column(u'user_id', INTEGER(), nullable=True)
    ref_id = Column(u'ref_id', INTEGER(), nullable=True)
    amount = Column(u'amount', INTEGER(), nullable=True)
    balance_before = Column(u'balance_before', INTEGER(), nullable=True)
    balance_after = Column(u'balance_after', INTEGER(), nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=True, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @classmethod
    def get_balance(cls, user_id):
        return db.session.query(func.sum(AccountDetail.amount)).filter_by(user_id=user_id).scalar() or 0

    @property
    def get_desc(self):
        if self.category == self.Category.CHARGE:
            return u"充值%s" % app_util.get_balance_name()
        elif self.category == self.Category.CONSUME:
            return Consume.get(self.ref_id).subject
        else:
            return self.Category.get_display_cn(self.category)

