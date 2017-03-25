# -*- coding:utf-8 -*-
import re
from bg_biz.orm.pay.charge import Charge
from bg_biz.orm.user import User
from sharper.flaskapp.orm.display_enum import DisplayEnum

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]
from datetime import datetime

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP, Text
from sharper.flaskapp.orm.base import BaseModel


class TransactionLog(BaseModel):
    __tablename__ = 'transaction_log'
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

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    transaction_id = Column(u'transaction_id', INTEGER(), nullable=False)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    user_id = Column(u'user_id', INTEGER(), nullable=True)
    amount = Column(u'amount', INTEGER(), nullable=True)
    pay_type = Column(u'pay_type', VARCHAR(length=32), nullable=False)
    object_type = Column(u'object_type', VARCHAR(length=32), nullable=False)
    object_id = Column(u'object_id', INTEGER(), nullable=False)
    status = Column(u'status', VARCHAR(length=32), nullable=False)
    memo = Column(u'memo', Text(), nullable=True)
    pay_time = Column(u'pay_time', TIMESTAMP(), nullable=False, default=datetime.now())
    out_serial_no = Column(u'out_serial_no', VARCHAR(length=128), nullable=True)
    title = Column(u'title', VARCHAR(length=128), nullable=True)
    detail = Column(u'detail', VARCHAR(length=1024), nullable=True)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)


class Transaction(BaseModel):
    __tablename__ = 'transaction'
    __table_args__ = {}

    class Status(DisplayEnum):
        FINISHED = 'finished'
        CANCELED = 'canceled'
        ERROR = 'error'
        NEW = 'new'
        __display_cn__ = {
            FINISHED: u'已完成',
            CANCELED: u'已取消',
            NEW: u'新建',
            ERROR: u'新建',
        }

    class ObjectType(DisplayEnum):
        CHARGE = "charge"
        WIFI_CHARGE = "wifi_charge"
        BUYING = "buying"
        __display_cn__ = {
            CHARGE: u"充值",
            WIFI_CHARGE: u"WiFi充值",
            BUYING: u"疯狂抢购",
        }

    class PayType(DisplayEnum):
        IAPPPAY = "iapppay"
        ALIPAY_DIRECT = "alipay_direct"
        ALIPAY_WAP = "alipay_wap"
        HIWIFI_CARD = "hiwifi_card"
        LOTTERY = "lottery"
        PRIZE = "prize"
        FUZHIFU = "fuzhifu"
        YEEPAY_DEPOSIT = "yeepay_deposit"
        YEEPAY_CREDIT = "yeepay_credit"
        YEEPAY_PHONE = "yeepay_phone"
        YEEPAY_CARD = "yeepay_card"
        SANXIAFU_WAP = "sanxiafu_wap"
        SANXIAFU_DIRECT = "sanxiafu_direct"
        APPLE_PAY = "apple_pay"
        ALIPAY_APP = "alipay_app"
        WEIXIN_PAY = "weixin_pay"
        WEIXIN_PAY_FOXCONN = "weixin_pay_foxconn"
        __display_cn__ = {
            IAPPPAY: u"爱贝",
            ALIPAY_DIRECT: u"支付宝-即时到账",
            ALIPAY_WAP: u"支付宝-wap支付",
            HIWIFI_CARD: u"Hi-WiFi 点卡充值",
            FUZHIFU: u"富支付",
            YEEPAY_DEPOSIT: u"易宝-储蓄卡",
            YEEPAY_CREDIT: u"易宝-信用卡",
            YEEPAY_PHONE: u"易宝-手机充值卡",
            YEEPAY_CARD: u"易宝-手机充值卡",
            LOTTERY: u"抽奖",
            SANXIAFU_WAP: u"三峡付-wap支付",
            SANXIAFU_DIRECT: u"三峡付-即时到账",
            APPLE_PAY: u"苹果支付",
            ALIPAY_APP:u"支付宝-移动支付",
            WEIXIN_PAY:u"微信钱包-微信支付",
            WEIXIN_PAY_FOXCONN:u"智联云网微信帐号",
            PRIZE: u"奖励"
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    user_id = Column(u'user_id', INTEGER(), nullable=True)
    amount = Column(u'amount', INTEGER(), nullable=True)
    pay_type = Column(u'pay_type', VARCHAR(length=32), nullable=False)
    object_type = Column(u'object_type', VARCHAR(length=32), nullable=False)
    object_id = Column(u'object_id', INTEGER(), nullable=False)
    origin_object_id = Column(u'origin_object_id', INTEGER(), nullable=False)
    status = Column(u'status', VARCHAR(length=32), nullable=False)
    memo = Column(u'memo', Text(), nullable=True)
    pay_time = Column(u'pay_time', TIMESTAMP(), nullable=False, default=datetime.now)
    out_serial_no = Column(u'out_serial_no', VARCHAR(length=128), nullable=True)
    title = Column(u'title', VARCHAR(length=128), nullable=True)
    callback = Column(u'callback', VARCHAR(length=512), nullable=True)
    detail = Column(u'detail', VARCHAR(length=1024), nullable=True)
    payment_account = Column(u'payment_account', VARCHAR(length=128), nullable=True)
    #pay_by = Column(u'pay_by', INTEGER(), nullable=True)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    def _after_insert(self):
        log = TransactionLog()
        for attr in ['user_id', 'amount', 'status', 'pay_type', 'object_type', 'object_id', 'memo', 'pay_time',
                     'object_id', 'out_serial_no', 'title', 'detail']:
            setattr(log, attr, getattr(self, attr))
        log.transaction_id = self.id
        log.insert()

    _after_update = _after_insert

    @property
    def object_type_cn(self):
        return self.ObjectType.get_display_cn(self.object_type)

    @property
    def pay_type_cn(self):
        return self.PayType.get_display_cn(self.pay_type)

    @property
    def status_info(self):
        info = self.Status.get_display_cn(self.status)
        error_config = {0:"销卡成功，订单成功",1:"销卡成功，订单失败",7:"卡号卡密或卡面额不符合规则",
                1002:"本张卡密您提交过于频繁，请您稍后再试",
                1003:"不支持的卡类型（比如电信地方卡）",
                1004:"密码错误或充值卡无效",
                1006:"充值卡无效",
                1007:"卡内余额不足",
                1008:"余额卡过期（有效期1个月）",
                1010:"此卡正在处理中",
                10000:"未知错误",
                2005:"此卡已使用",
                2006:"卡密在系统处理中",
                2007:"该卡为假卡",
                2008:"该卡种正在维护",
                2009:"浙江省移动维护",
                2010:"江苏省移动维护",
                2011:"福建省移动维护",
                2012:"辽宁省移动维护",
                2013:"该卡已被锁",
                2014:"系统繁忙,请稍后重试" }
        if self.pay_type == self.PayType.YEEPAY_CARD:
            if self.memo:
                card_status = re.search(r'p8_cardStatus\:(\d+)',self.memo)
                if card_status:
                    card_status = int(card_status.group(1))
                    info = info +"(%s)"%error_config.get(card_status)


        return info

    @property
    def user(self):
        return User.get(self.user_id)

    @property
    def charge(self):
        return Charge.get(self.object_id)


class TransactionExtraInfo(BaseModel):
    __tablename__ = 'transaction_extra_info'
    __table_args__ = {}



    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)
    transaction_ids = Column(u'transaction_ids', VARCHAR(length=200), nullable=False)
    real_amount = Column(u'real_amount', INTEGER(), nullable=True)
    detail = Column(u'detail', VARCHAR(length=1024), nullable=True)



class GatewayTransactionLog(BaseModel):
    __tablename__ = 'gateway_transaction_log'
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

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    transaction_id = Column(u'transaction_id', INTEGER(), nullable=False)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    app_id = Column(u'app_id', VARCHAR(length=32), nullable=False)
    amount = Column(u'amount', INTEGER(), nullable=True)
    pay_type = Column(u'pay_type', VARCHAR(length=32), nullable=False)
    object_type = Column(u'object_type', VARCHAR(length=32), nullable=False)
    from_trade_no = Column(u'from_trade_no', INTEGER(), nullable=False)
    status = Column(u'status', VARCHAR(length=32), nullable=False)
    memo = Column(u'memo', Text(), nullable=True)
    pay_time = Column(u'pay_time', TIMESTAMP(), nullable=False, default=datetime.now())
    out_serial_no = Column(u'out_serial_no', VARCHAR(length=128), nullable=True)
    title = Column(u'title', VARCHAR(length=128), nullable=True)
    detail = Column(u'detail', VARCHAR(length=1024), nullable=True)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)


class GatewayTransaction(BaseModel):
    __tablename__ = 'gateway_transaction'
    __table_args__ = {}

    class Status(DisplayEnum):
        FINISHED = 'finished'
        CANCELED = 'canceled'
        ERROR = 'error'
        NEW = 'new'
        __display_cn__ = {
            FINISHED: u'已完成',
            CANCELED: u'已取消',
            NEW: u'新建',
            ERROR: u'新建',
        }

    class ObjectType(DisplayEnum):
        CHARGE = "charge"
        WIFI_CHARGE = "wifi_charge"
        BUYING = "buying"
        __display_cn__ = {
            CHARGE: u"充值",
            WIFI_CHARGE: u"WiFi充值",
            BUYING: u"疯狂抢购",
        }

    class PayType(DisplayEnum):
        IAPPPAY = "iapppay"
        ALIPAY_DIRECT = "alipay_direct"
        ALIPAY_WAP = "alipay_wap"
        HIWIFI_CARD = "hiwifi_card"
        LOTTERY = "lottery"
        FUZHIFU = "fuzhifu"
        YEEPAY_DEPOSIT = "yeepay_deposit"
        YEEPAY_CREDIT = "yeepay_credit"
        YEEPAY_PHONE = "yeepay_phone"
        YEEPAY_CARD = "yeepay_card"
        SANXIAFU_WAP = "sanxiafu_wap"
        SANXIAFU_DIRECT = "sanxiafu_direct"
        __display_cn__ = {
            IAPPPAY: u"爱贝",
            ALIPAY_DIRECT: u"支付宝-即时到账",
            ALIPAY_WAP: u"支付宝-wap支付",
            HIWIFI_CARD: u"Hi-WiFi 点卡充值",
            FUZHIFU: u"富支付",
            YEEPAY_DEPOSIT: u"易宝-储蓄卡",
            YEEPAY_CREDIT: u"易宝-信用卡",
            YEEPAY_PHONE: u"易宝-手机充值卡",
            YEEPAY_CARD: u"易宝-游戏点卡",
            LOTTERY: u"抽奖",
            SANXIAFU_WAP: u"三峡付-wap支付",
            SANXIAFU_DIRECT: u"三峡付-即时到账",
        }

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    app_id = Column(u'app_id', VARCHAR(length=32), nullable=False)
    amount = Column(u'amount', INTEGER(), nullable=True)
    pay_type = Column(u'pay_type', VARCHAR(length=32), nullable=False)
    object_type = Column(u'object_type', VARCHAR(length=32), nullable=False)
    from_trade_no = Column(u'from_trade_no', INTEGER(), nullable=False)
    status = Column(u'status', VARCHAR(length=32), nullable=False)
    memo = Column(u'memo', Text(), nullable=True)
    pay_time = Column(u'pay_time', TIMESTAMP(), nullable=False, default=datetime.now)
    out_serial_no = Column(u'out_serial_no', VARCHAR(length=128), nullable=True)
    title = Column(u'title', VARCHAR(length=128), nullable=True)
    callback = Column(u'callback', VARCHAR(length=512), nullable=True)
    detail = Column(u'detail', VARCHAR(length=1024), nullable=True)
    payment_account = Column(u'payment_account', VARCHAR(length=128), nullable=True)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)

    def _after_insert(self):
        log = GatewayTransactionLog()
        for attr in ['app_id', 'amount', 'status', 'pay_type', 'object_type', 'from_trade_no', 'memo', 'pay_time', 'out_serial_no', 'title', 'detail']:
            setattr(log, attr, getattr(self, attr))
        log.transaction_id = self.id
        log.insert()

    _after_update = _after_insert

    @property
    def object_type_cn(self):
        return self.ObjectType.get_display_cn(self.object_type)

    @property
    def pay_type_cn(self):
        return self.PayType.get_display_cn(self.pay_type)


class GatewayTransactionExtraInfo(BaseModel):
    __tablename__ = 'gateway_transaction_extra_info'
    __table_args__ = {}



    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=False, default=datetime.now)
    create_time = Column(u'create_time', TIMESTAMP(), nullable=False, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)
    transaction_ids = Column(u'transaction_ids', VARCHAR(length=200), nullable=False)
    real_amount = Column(u'real_amount', INTEGER(), nullable=True)
    detail = Column(u'detail', VARCHAR(length=1024), nullable=True)

