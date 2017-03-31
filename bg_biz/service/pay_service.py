# -*- coding:utf-8 -*-
from flask import request
from bg_biz.orm.pay.transaction import Transaction, GatewayTransaction
from bg_biz.pay.callback.wifi_charge import WifiChargeExecutor

from bg_biz.pay.callback.charge import ChargeExecutor
from bg_biz.pay.callback.buying import BuyingExecutor
from sharper.flaskapp.logger import logger
from sharper.lib.error import AppError
from bg_biz.pay.alipay import Alipay, AlipayWap, AlipayAPP
from bg_biz.orm.user import User
from bg_biz.orm.sysconfig import SysConfig
import json
from bg_biz.pay.hiwifipay import Hiwifipay
from bg_biz.pay.applepay import ApplePay
from bg_biz.pay.weixinpay import WXpay

__author__ = [
    '"liubo" <liubo@51domi.com>'
]


class PayService(object):
    @classmethod
    def create_pay_url(cls, channel, amount, title, detail, object_id, callback,
                       object_type=Transaction.ObjectType.WIFI_CHARGE,
                       user_id=None):
        '''
        channel为支付类型，对应PaymentType
        object_id为关联的id，比如gift_book的id
        callback，回调地址，支付完成后，支付网关的跳转地址，用于展示支付结果信息
        '''
        trans = Transaction()
        trans.status = Transaction.Status.NEW

        trans.amount = amount
        trans.user_id = user_id
        trans.object_type = object_type
        trans.object_id = object_id
        trans.pay_type = channel
        trans.title = title
        trans.detail = detail
        trans.callback = callback
        trans.insert()

        return cls.get_pay_executor(trans).create_pay_url(trans)

    @classmethod
    def create_pay_url_new(cls, channel, amount, title, detail, object_id, callback,
                           object_type=Transaction.ObjectType.WIFI_CHARGE,
                           user_id=None, extra_arguments=[]):
        '''
        channel为支付类型，对应PaymentType
        object_id为关联的id，比如gift_book的id
        callback，回调地址，支付完成后，支付网关的跳转地址，用于展示支付结果信息
        '''
        # 如果存在未支付的同一类型交易，则先查询使用
        channel_num = channel.find('ios_')
        channel_back = channel
        if channel_num>=0:
            channel = channel[4:]

        trans = Transaction.query.filter_by(object_type=object_type).filter_by(
            object_id=object_id).first()
        print '---------trans-----',trans
        if trans and trans.status != Transaction.Status.NEW:
            raise AppError(u"请勿重复发起支付请求")
        if not trans:
            trans = Transaction()
        trans.status = Transaction.Status.NEW
        if user_id:
            user = User.get(user_id)
            ignore_phones = ['18621365260','13918778151','18916208830']
            if user.phone in ignore_phones:
                amount = 1
        trans.amount = amount
        trans.user_id = user_id
        trans.object_type = object_type
        trans.object_id = object_id
        trans.pay_type = channel_back
        trans.title = title
        trans.detail = detail
        trans.callback = callback
        if trans.id:
            trans.update()
        else:
            trans.insert()
        try:
            print '------------------------', channel
            if channel == 'alipay_app':
                print '------------------------', extra_arguments
                if extra_arguments:
                    url = cls.get_pay_executor(trans).create_pay_mobile(trans, extra_arguments)
                else:
                    url = cls.get_pay_executor(trans).create_pay_mobile(trans)
            elif channel == 'weixin_pay':
                url = cls.get_pay_executor(trans).get_pay_prepay_id(trans)
            elif channel == 'weixin_pay_foxconn':
                url = cls.get_pay_executor(trans).get_pay_prepay_id(trans,'foxconn')
            else:
                print '22222222222222222222',channel
                if extra_arguments:
                    url = cls.get_pay_executor(trans).create_pay_url(trans, extra_arguments)
                else:
                    url = cls.get_pay_executor(trans).create_pay_url(trans)
        except Exception, e:
            print '------------------------', channel
            trans.memo = e
            trans.update()
            url = ""
        return url, trans

    @classmethod
    def get_pay_executor(cls, trans):
        print 'trans===============',trans.pay_type
        channel = trans.pay_type
        channel_num = channel.find('ios_')
        if channel_num >= 0:
            channel = channel[4:]
        if channel == Transaction.PayType.ALIPAY_DIRECT:
            return Alipay()
        elif channel == Transaction.PayType.ALIPAY_WAP:
            return AlipayWap()
        #         elif trans.pay_type == Transaction.PayType.SANXIAFU_WAP:
        #             return SanxiaPayMobile()
        #         elif trans.pay_type == Transaction.PayType.SANXIAFU_DIRECT:
        #             return SanxiaPay()
        elif channel == Transaction.PayType.APPLE_PAY:
            return ApplePay()
        elif channel == Transaction.PayType.ALIPAY_APP:
            return AlipayAPP()
        elif channel == Transaction.PayType.WEIXIN_PAY:
            return WXpay()
        elif channel == Transaction.PayType.WEIXIN_PAY_FOXCONN:
            return WXpay()
        else:
            logger.error(u"无法识别的支付类型: %s" % trans.pay_type)
            raise AppError(u"系统错误")

    callback_executors = {
        Transaction.ObjectType.WIFI_CHARGE: WifiChargeExecutor(),
        Transaction.ObjectType.CHARGE: ChargeExecutor(),
        Transaction.ObjectType.BUYING: BuyingExecutor()
    }

    @classmethod
    def get_callback(cls, bill):
        return cls.callback_executors.get(bill.object_type)


class GateWay(object):
    @classmethod
    def create_pay_url(cls, channel, amount, title, detail, object_id, callback,
                       object_type=Transaction.ObjectType.WIFI_CHARGE,
                       user_id=None, extra_arguments=[]):
        '''
        channel为支付类型，对应PaymentType
        object_id为关联的id，比如gift_book的id
        callback，回调地址，支付完成后，支付网关的跳转地址，用于展示支付结果信息
        '''
        trans = Transaction()
        trans.status = Transaction.Status.NEW

        trans.amount = amount
        trans.user_id = user_id
        trans.object_type = object_type
        trans.object_id = object_id
        trans.pay_type = channel
        trans.title = title
        trans.detail = detail
        trans.callback = callback
        trans.insert()

        return Hiwifipay().create_pay_url(trans, extra_arguments=extra_arguments), trans

    @classmethod
    def create_notify_url(cls, trans):
        return Hiwifipay().create_notify_url(trans)

    @classmethod
    def create_external_pay_url(cls, channel, amount, title, detail, from_trade_no, callback, app_id,
                                user_id="", object_type=Transaction.ObjectType.WIFI_CHARGE, extra_arguments=[]):
        '''
        channel为支付类型，对应PaymentType
        object_id为关联的id，比如gift_book的id
        callback，回调地址，支付完成后，支付网关的跳转地址，用于展示支付结果信息
        '''
        # 如果存在未支付的同一类型交易，则先查询使用
        trans = GatewayTransaction.query.filter_by(object_type=object_type).filter_by(
            from_trade_no=from_trade_no).first()
        if trans and trans.status != GatewayTransaction.Status.NEW:
            raise AppError(u"请勿重复发起支付请求")
        if not trans:
            trans = GatewayTransaction()
        trans.status = GatewayTransaction.Status.NEW
        trans.amount = amount
        trans.app_id = app_id
        trans.object_type = object_type
        trans.from_trade_no = from_trade_no
        trans.pay_type = channel
        trans.title = title
        trans.detail = detail
        trans.callback = callback
        if trans.id:
            trans.update()
        else:
            trans.insert()
        if extra_arguments:
            return cls.get_pay_executor(trans).create_pay_url(trans, extra_arguments, source="gateway"), trans
        else:
            return cls.get_pay_executor(trans).create_pay_url(trans, source="gateway"), trans

    @classmethod
    def get_pay_executor(cls, trans):
        if trans.pay_type == GatewayTransaction.PayType.ALIPAY_DIRECT:
            return Alipay()
        elif trans.pay_type == GatewayTransaction.PayType.ALIPAY_WAP:
            return AlipayWap()
        elif trans.pay_type == GatewayTransaction.PayType.FUZHIFU:
            return Fuzhifu()
        elif trans.pay_type == GatewayTransaction.PayType.YEEPAY_CREDIT:
            return YeepayCredit()
        elif trans.pay_type == GatewayTransaction.PayType.YEEPAY_DEPOSIT:
            return YeepayDeposit()
        elif trans.pay_type == GatewayTransaction.PayType.YEEPAY_CARD:
            return YeepayCard()
        #         elif trans.pay_type == GatewayTransaction.PayType.SANXIAFU_WAP:
        #             return SanxiaPayMobile()
        #         elif trans.pay_type == GatewayTransaction.PayType.SANXIAFU_DIRECT:
        #             return SanxiaPay()
        else:
            logger.error(u"无法识别的支付类型: %s" % trans.pay_type)
            raise AppError(u"系统错误")

    callback_executors = {
        Transaction.ObjectType.WIFI_CHARGE: WifiChargeExecutor(),
        Transaction.ObjectType.CHARGE: ChargeExecutor(),
        Transaction.ObjectType.BUYING: BuyingExecutor()
    }

    @classmethod
    def get_callback(cls, bill):
        return cls.callback_executors.get(bill.object_type)
