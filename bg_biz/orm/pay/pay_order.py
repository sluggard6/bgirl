# -*- coding:utf-8 -*-
from luhu_sharper.flaskapp.orm.base import BaseModel
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum
import time
from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP, DATE, Table, ForeignKey
from datetime import datetime
from luhu_sharper.flaskapp.orm.kvdb_mixin import KvdbMixin


__author__ = [
    '"wufang" <wufang@hi-wifi.cn>'
]


class PayOrder(BaseModel):
    __tablename__ = "pay_order"
    __table_args__ = {}
    
    __bind_key__ = "mishi"
    
    class Status(DisplayEnum):
        NEW = 0
        GATEWAY = 1
        PAYED = 2
        FILED = 3
        __display_cn__ = {
            NEW : u"新建",
            GATEWAY : u"支付网关",
            PAYED : u"支付完成",
            FILED : u"支付失败",
        }
    
    class Way(DisplayEnum):
        UNKNOW = 0
        ALIPAY = 1
        YEEPAY = 2
        __display_cn__ = {
            UNKNOW : u"未指定",
            ALIPAY : u"支付宝",
            YEEPAY : u"易宝",
        }
    
    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(u'user_id', INTEGER(), nullable=True)
    pay_user_id = Column(u'pay_user_id', INTEGER(), nullable=True)
    way = Column(u'way', INTEGER(), nullable=True, default=Way.UNKNOW)
    product_id = Column(u'product_id', INTEGER(), nullable=False )
    count = Column(u'count', INTEGER(), nullable=False )
    all_price = Column(u'all_price', INTEGER(), nullable=False )
    status = Column(u'status', INTEGER(), nullable=False, default=Status.NEW)
    des = Column(u'des', VARCHAR(), nullable=True)
    create_time = Column(u'create_time', DATETIME(), nullable=False, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    
    @property
    def product_name(self):
        return u"测试产品"
    
    
    
class PayProduct(BaseModel, KvdbMixin):
    __tablename__ = "pay_product"
    __table_args__ = {}
    
    __bind_key__ = "mishi"
    
    class Category(DisplayEnum):
        ALL_DAY = 0
        __display_cn__ = {
            ALL_DAY : u'包天'
        }
        
    class Status(DisplayEnum):
        ACTIVE = 1
        INACTIVE = 0

        __display_cn__ = {
            ACTIVE: u'有效',
            INACTIVE: u'无效'
        }
    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    name = Column(u'name', VARCHAR(), nullable=False)
    company_id = Column(u'company_id', INTEGER(), nullable=False)
    category = Column(u'category', INTEGER(), nullable=False, default=Category.ALL_DAY)
    price = Column(u'price', INTEGER(), nullable=False, default=0)
    value = Column(u'value', INTEGER(), nullable=False, default=0)
    status = Column(u'status', INTEGER, nullable=False, default=Status.ACTIVE)
    des = Column(u'des', VARCHAR(), nullable=False)
    create_by = Column(u'create_by', INTEGER(), nullable=False)
    create_time = Column(u'create_time', DATETIME(), nullable=False, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    
    @property
    def display_value(self):
        return '%.2f' % (float(self.price)/100)
