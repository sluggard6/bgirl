# -*- coding:utf-8 -*-
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]
from datetime import datetime

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP
from luhu_sharper.flaskapp.orm.base import BaseModel
from luhu_sharper.flaskapp.orm.base import db

class PayObjRegister(BaseModel):
    __tablename__ = 'pay_obj_register'
    __table_args__ = {}

    class ObjectType(DisplayEnum):
        CHARGE = "charge"
        WIFI_CHARGE = "wifi_charge"
        BUYING = "buying"
        __display_cn__ = {
            CHARGE: u"充值",
            WIFI_CHARGE: u"WiFi充值",
            BUYING: u"疯狂抢购",
        }



    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    object_type = Column(u'object_type', VARCHAR(length=32), nullable=False)
    description = Column(u'description', VARCHAR(length=200), nullable=True)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @classmethod
    def get_pay_type(cls,object_name):
        reg = cls.query.filter_by(object_type=object_name).first()
        pay_types =  ObjPayType.query.filter_by(obj_type_id=reg.id).all() if reg else []
        return pay_types

    @property
    def pay_types(self):
        pay_types =  ObjPayType.query.filter_by(obj_type_id=self.id).all()
        return pay_types

    def _clear_all_pay_types(self):
        db.engine.execute('delete from obj_pay_type where obj_type_id=%s', self.id)


    def update_pay_types(self, pay_type_list):
        """
        批量更新权限到角色
        @param permission_id_list: 权限id列表
        @return:
        """
        self._clear_all_pay_types()
        if pay_type_list:
            for pid in pay_type_list:
                ObjPayType(
                                self.id,
                                pid
                            ).insert()


class ObjPayType(BaseModel):
    __tablename__ = 'obj_pay_type'
    __table_args__ = {}



    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    obj_type_id = Column(u'obj_type_id', INTEGER(), nullable=False)
    pay_type_id = Column(u'pay_type_id', INTEGER(), nullable=False)
    description = Column(u'description', VARCHAR(length=512), nullable=True)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    @property
    def pay_type(self):
        pay_type =  PayTypeInfo.query.filter_by(id=self.pay_type_id).first()
        return pay_type

class PayTypeInfo(BaseModel):
    __tablename__ = 'pay_type_info'
    __table_args__ = {}

    class PayType(DisplayEnum):
        IAPPPAY = "iapppay"
        ALIPAY = "alipay"
        FUZHIFU = "fuzhifu"
        YEEPAY_DEPOSIT = "yeepay_deposit"
        YEEPAY_CARD = "yeepay_card"
        SANXIAFU = "sanxiafu"
        TEST = "test"
        __display_cn__ = {
            IAPPPAY: u"爱贝",
            ALIPAY: u"支付宝",
            FUZHIFU: u"富支付",
            YEEPAY_DEPOSIT: u"易宝-储蓄卡",
            YEEPAY_CARD: u"易宝-充值卡",
            SANXIAFU: u"三峡付-wap支付",
            TEST: u"ceshi"
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    name = Column(u'name', VARCHAR(length=32), nullable=False)
    description = Column(u'description', VARCHAR(length=512), nullable=True)
    mobile_name = Column(u'mobile_name', VARCHAR(length=32), nullable=False)
    direct_name = Column(u'direct_name', VARCHAR(length=32), nullable=False)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)


