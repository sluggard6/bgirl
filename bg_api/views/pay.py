# -*- coding:utf-8 -*-
import base64
from datetime import datetime
#import httplib
#import httplib2
import json
import traceback
from flask import Blueprint, request,g, jsonify
from bg_biz.orm.pay.transaction import Transaction, TransactionExtraInfo
from bg_biz.pay.alipay import Alipay, AlipayWap,AlipayAPP
from bg_biz.service.pay_service import PayService
from bg_biz.service.user_service import UserService
from sharper.flaskapp.kvdb import kvdb
from sharper.lib.error import AppError
from lib.logger_client import logger_pay
from bg_biz.orm.pay.charge import Charge
from bg_biz.service.config_service import ConfigService
from bg_biz.pay.open_decorator import sort_params
from bg_biz.pay.sign.rsa import RSASigner
from bg_biz.pay.open_decorator import open_sign_verify
from sharper.util.string import md5
import urllib,urllib2
import xml.etree.ElementTree as ET
import os
from bg_biz.pay.weixinpay import WXpay

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]
PayView = Blueprint('pay', __name__)



@PayView.route('/notify/wxpay', methods=['POST', 'GET'])
#@open_sign_verify
def wx_pay_notify():
    logger_pay.error("\n=================wxpay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.data)

    print request.url
    print request.data

    try:
        print '-------------------------------------'
        xml = request.data
        if not xml:
            logger_pay.error("xml 空")
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return_code = array_data['return_code']
        print '1-',return_code
        if return_code=='SUCCESS':
            result_code = array_data['result_code']
            print '2-',result_code
            if result_code=='SUCCESS':
                return_sign=array_data['sign']
                del array_data['sign']
                sign = WXpay.getSign(array_data)
                print '3-',sign,'=======================',return_sign
                if sign == return_sign:
                    trans_id = array_data['out_trade_no']
                    trans = Transaction.get(trans_id)
                    if trans.status == Transaction.Status.NEW:
                        trans.memo = ', '.join("%s:%s" % (key, array_data[key]) for key in array_data)
                        trans.pay_time = array_data['time_end']
                        trans.payment_account = array_data['total_fee']
                        trans.out_serial_no = array_data['transaction_id']
                        PayService.get_callback(trans).execute(trans)
                        trans.update()
    except Exception as e:
        print '-error---------'
        logger_pay.error(e.message)
        return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
    return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"


@PayView.route('/notify/applepaynew', methods=['POST', 'GET'])
#@open_sign_verify
def apple_pay_notify_new():
    try:
        logger_pay.error("\n=================hiwifipay notify===========================\n")
        logger_pay.error(request.url)
        data = request.form or request.args
        trans_id = data.get('trade_no', None)
        print 'trans_id------------',trans_id
        logger_pay.error('apple------------'+trans_id)
        receipt_data = data.get('receipt-data', None)
        now = datetime.now()
        year = now.year
        month = now.month
        path = '/var/www/upload/apple'+os.sep+str(year)+os.sep+str(month)
        if not os.path.exists(path):
            os.makedirs(path)
        pj = file(path+os.sep+str(trans_id), 'w')
        pj.write(receipt_data)
        pj.close()
        #logger_pay.error('trans_id------------'+trans_id)
        token = data.get('token', None)
        print 'token==============', token
        #logger_pay.error('token=============='+token)
        out_serial_no = data.get('out_serial_no')
        #logger_pay.error('out_serial_no=============='+out_serial_no)
        print 'out_serial_no========================',out_serial_no
        if md5(trans_id+"qwertyuiopasdfghjklzxcvbnm")!=token:
            return jsonify(success=False,msg="token不对")
        trans = Transaction.get(trans_id)
        print '------------apple pay trans_id-------------------',trans_id
        if trans.status == Transaction.Status.FINISHED:
            return jsonify(success=True, msg="订单已支付！")
        if trans.status == Transaction.Status.NEW:
            memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form if key != 'receipt-data')
            memo +=',receipt-data:'+path+os.sep+str(trans_id)
            trans.memo = memo
            print '-------------------------------------------------',len(memo)
            trans.pay_time = now
            print 'update after----------------',trans_id
            trans.update()
            print 'usdfsdfsdf--------------------------'
            PayService.get_pay_executor(trans).check_pay_result(trans, receipt_data, out_serial_no)

            print 'update after----------------',trans_id
            return jsonify(success=True, msg="支付成功")
    except Exception as e:
        print 'pay--------------',e.message
        logger_pay.error('exception------------------'+trans_id)
        logger_pay.error(e.message)
        logger_pay.error('exception------------------ False')
@PayView.route('/notify/applepay', methods=['POST', 'GET'])
#@open_sign_verify
def apple_pay_notify():
    """url = "https://sandbox.itunes.apple.com/verifyReceipt"
    rec_data = request.form.get("receipt-data","") or request.args.get("receipt-data","")
    #rec_data = open("/home/ubuntu/Downloads/file/ReceiptData","r").read()
    print rec_data
    test_data = json.dumps({'receipt-data':base64.b64encode(rec_data)})
    print test_data
    http=httplib2.Http()
    response,content = http.request(uri=url,body=test_data)
    print content
    return content
    conn = httplib.HTTPConnection("test.api.hi-wifi.cn", 80, False)
    conn.request('get', url, body=test_data)
    res = conn.getresponse()
    print res.read()
    print cc"""
    logger_pay.error("\n=================hiwifipay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.args)
    try:

        data = request.form or request.args
        trade_status = data.get('trade_status', None)
        print trade_status
        if trade_status == "1":
            trans_id = data.get('trade_no', None)
            token = data.get('token', None)
            if md5(trans_id+"qwertyuiopasdfghjklzxcvbnm")!=token:
                return jsonify(success=False,msg="token不对")
            trans = Transaction.get(trans_id)
            print trans
            if trans.status == Transaction.Status.NEW:
                """receipt_data = data.get('receipt_data', None)
                url = "https://sandbox.itunes.apple.com/verifyReceipt"
                #url = "https://buy.itunes.apple.com/verifyReceipt"
                test_data = json.dumps({'receipt-data':receipt_data,'password':'18205144515'})
                conn = httplib.HTTPConnection("test.api.hi-wifi.cn", 80, False)
                conn.request('get', url, body=test_data)
                res = conn.getresponse()
                print res.read()"""

                trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                trans.pay_time = datetime.now()

                trans.out_serial_no = data.get('out_serial_no', None)

                real_amount = float(data.get('real_amount', 0)) * 100
                left_amount = int(real_amount - trans.amount)
                PayService.get_callback(trans).execute(trans)
                trans.update()
    except Exception as e:
        return jsonify(success=False)
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        return 'SUCCESS'
    return jsonify(success=True)

@PayView.route('/notify/iapppay', methods=['POST'])
def notify():
    logger_pay.error("\n=================iapppay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        trans_data = request.form.get('transdata')
        sign = request.form.get('sign')
        if IAppPay.verify(trans_data, sign):
            ret_json = json.loads(trans_data)
            status = ret_json.get('result')
            if status == 0:
                # 支付成功
                trans_id = ret_json.get('exorderno')
                out_serial_no = ret_json.get('transid')
                pay_time = ret_json.get('transtime')
                pay_type = ret_json.get('paytype')
                UserService.charge_success(trans_id=trans_id, out_serial_no=out_serial_no, pay_time=pay_time,
                                           pay_type=pay_type, memo=trans_data)
        else:
            return 'FAILURE'
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        return 'SUCCESS'
    return 'SUCCESS'


@PayView.route('/notify/alipay', methods=['POST'])
def alipay_back_notify():
    logger_pay.error("\n=================alipay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        trade_status = request.form.get('trade_status', None)
        if trade_status == u'TRADE_SUCCESS':
            verify_result = Alipay.verify_sign_md5(request.form)
            if verify_result:
                trans_id = request.form.get('out_trade_no', None)
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                    trans.pay_time = request.form.get('gmt_payment', datetime.now())
                    trans.payment_account = request.form.get('buyer_email', None)
                    trans.out_serial_no = request.form.get('trade_no', None)
                    PayService.get_callback(trans).execute(trans)
                    trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"支付宝回调失败")


@PayView.route('/notify/alipay_wap', methods=['POST'])
def alipay_wap_notify():
    logger_pay.error("\n=================alipay wap notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    notify_data = request.form.get("notify_data", None)

    import xml.etree.cElementTree as et

    tree = et.fromstring(notify_data)
    sign = request.form.get('sign', None)
    trade_status = tree.find('trade_status').text
    trans_id = tree.find('out_trade_no').text
    gmt_payment = tree.find('gmt_payment').text
    alipay_trade_no = tree.find('trade_no').text
    buyer_email = tree.find('buyer_email').text
    try:
        if trade_status == u'TRADE_FINISHED':
            need_sign_str = "service=%s&v=%s&sec_id=%s&notify_data=%s" % (
                request.form.get('service'), request.form.get('v'), request.form.get('sec_id'), notify_data)
            verify_result = AlipayWap.verify_sign_md5(need_sign_str, sign)
            if verify_result:
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                    trans.pay_time = gmt_payment
                    trans.out_serial_no = alipay_trade_no
                    trans.payment_account = buyer_email
                    PayService.get_callback(trans).execute(trans)
                    trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"支付宝回调失败")

@PayView.route('/notify/alipay_app', methods=['POST'])
def alipay_app_notify():
    logger_pay.error("\n=================alipay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        trade_status = request.form.get('trade_status', None)
        if trade_status == u'TRADE_SUCCESS':
            verify_result = Alipay.verify_sign_rsa(request.form)
            if verify_result:
                trans_id = request.form.get('out_trade_no', None)
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                    trans.pay_time = request.form.get('gmt_payment', datetime.now())
                    trans.payment_account = request.form.get('buyer_email', None)
                    trans.out_serial_no = request.form.get('trade_no', None)
                    PayService.get_callback(trans).execute(trans)
                    trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        print '-------------',e
        raise AppError(u"支付宝回调失败")

@PayView.route('/notify/auth/alipay_app', methods=['POST'])
def alipay_app_auth_notify():
    logger_pay.error("\n=================alipay notify auth===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        trade_status = request.form.get('trade_status', None)
        if trade_status == u'TRADE_SUCCESS':
            verify_result = Alipay.verify_sign_rsa(request.form)
            if verify_result:
                trans_id = request.form.get('out_trade_no', None)
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                    trans.pay_time = request.form.get('gmt_payment', datetime.now())
                    trans.payment_account = request.form.get('buyer_email', None)
                    trans.out_serial_no = request.form.get('trade_no', None)
                    PayService.get_callback(trans).execute(trans)
                    trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        print '-------------',e
        raise AppError(u"支付宝回调失败")


@PayView.route('/notify/fuzhifu', methods=['POST'])
def fuzhifu_notify():
    logger_pay.error("\n=================fuzhifu notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        ret = Fuzhifu().result_decrypt(request.form)
        if ret.get('status', 0) == 1:
            trans_id = ret.get('orderNo', 0)
            trans = Transaction.get(trans_id)
            if trans.status == Transaction.Status.NEW:
                trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                trans.pay_time = datetime.now()
                trans.out_serial_no = ret.get('payOrderNo', None)
                PayService.get_callback(trans).execute(trans)
                trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
    raise AppError(u"富支付回调失败")


@PayView.route('/notify/sanxiafu', methods=['POST'])
def sanxiafu_notify():
    logger_pay.error("\n=================sanxiafu notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        trade_code = request.form.get('trade_code', None)
        notify_type = request.form.get('notify_type', None)
        sign = request.form.get('sign', None)
        if trade_code == u'0000' and notify_type == u'0':
            verify_rsa = SanxiaPay().verify_sign_rsa(request.form,sign)
            dict = request.form.copy()
            del dict['sign']
            dict = sorted(dict.items(), key=lambda d: d[0])
            dict = "".join(map(lambda x: "%S=%S" % (x[0], x[1]), dict))
            verify_result = SanxiaPay().verify_sign_md5(dict, sign)
            if verify_result:
                trans_id = request.form.get('out_trade_no', None)
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                    trans.pay_time = datetime.now()

                    trans.out_serial_no = request.form.get('pay_order_no', None)
                    PayService.get_callback(trans).execute(trans)
                    trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"三峡付回调失败")
# @PayView.route('/notify/sanxiafu', methods=['POST'])
# def sanxiafu_notify():
#     logger_pay.error("\n=================sanxiafu notify===========================\n")
#     logger_pay.error(request.url)
#     logger_pay.error(request.form)
#     try:
#         trade_code = request.form.get('trade_code', None)
#         notify_type = request.form.get('notify_type', None)
#         sign = request.form.get('sign', None)
#         if trade_code == u'0000' and notify_type == u'0':
#             verify_rsa = SanxiaPay().verify_sign_rsa(request.form)
#             dict = request.form.copy()
#             del dict['sign']
#             dict = sorted(dict.items(), key=lambda d: d[0])
#             dict = "".join(map(lambda x: "%S=%S" % (x[0], x[1]), dict))
#             verify_result = SanxiaPay().verify_sign_md5(dict, sign)
#             if verify_result:
#                 trans_id = request.form.get('out_trade_no', None)
#                 trans = Transaction.get(trans_id)
#                 if trans.status == Transaction.Status.NEW:
#                     trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
#                     trans.pay_time = datetime.now()
#
#                     trans.out_serial_no = request.form.get('pay_order_no', None)
#                     PayService.get_callback(trans).execute(trans)
#                     trans.update()
#         return "success"
#     except Exception as e:
#         logger_pay.error(traceback.format_exc())
#         logger_pay.error(e)
#         raise AppError(u"三峡付回调失败")


@PayView.route('/notify/yeepay', methods=['POST', 'GET'])
def yeepay_notify():
    logger_pay.error("\n=================yeepay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.args)
    try:
        trade_code = request.args.get('r1_Code', None)
        hmac = request.args.get('hmac', None)

        if trade_code == "1":
            # dict =request.form.copy()
            dict = request.args.copy()
            del dict['r0_Cmd']
            del dict['r1_Code']
            del dict['r2_TrxId']
            del dict['hmac']
            dict = sorted(dict.items(), key=lambda d: d[0])
            dict.insert(0, ("r1_Code", request.args.get("r1_Code", "")))
            dict.insert(0, ("r0_Cmd", request.args.get("r0_Cmd", "")))
            dict = "".join(map(lambda x: x[1], dict))
            verify_result = YeepayCard().verify_sign(dict, hmac)
            if verify_result:
                trans_id = request.args.get('p2_Order', None)
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW or trans.status == Transaction.Status.ERROR:
                    if trans.memo:
                        trans.memo += ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
                    else:
                        trans.memo = ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
                    trans.pay_time = datetime.now()

                    trans.out_serial_no = request.args.get('r2_TrxId', None)

                    real_amount = float(request.args.get('p3_Amt', 0)) * 100
                    left_amount = int(real_amount - trans.amount)
                    """if amount_change < 0:
                        if trans.object_type == Transaction.ObjectType.CHARGE and str(trans.callback).strip().endswith("type=wifi"):
                            close_amount = ConfigService.get_close_wifi_fee(real_amount)
                            new_amount = close_amount if close_amount else int(real_amount)
                        else:
                            new_amount = int(real_amount)
                        trans.amount =  new_amount
                    else:
                        new_amount = trans.amount"""
                    if left_amount < 0:
                        if trans.object_type == Transaction.ObjectType.CHARGE:
                            charge = Charge.get(trans.object_id)
                            if charge.source == Charge.Source.PORTAL_WIFI or charge.source == Charge.Source.WIFI or 1:
                                charge_record = Charge()
                                charge_record.amount = int(real_amount)
                                charge_record.paid = int(real_amount)
                                #charge_record.user_id = trans.user_id
                                charge_record.user_id = charge.user_id
                                charge_record.status = Charge.Status.NEW
                                charge_record.score = 0
                                charge_record.source = charge.source
                                charge_record.ask_for = charge.ask_for
                                charge_record.ask_for_status = charge.ask_for_status
                                charge_record.pay_by = charge.pay_by
                                charge_record.insert()
                                trans.amount = charge_record.amount
                                trans.origin_object_id = trans.object_id
                                trans.object_id = charge_record.id
                                trans.update()
                                from bg_biz.pay.callback.charge import ChargeExecutor

                                ChargeExecutor().execute(trans)
                            else:
                                trans.status = Transaction.Status.ERROR
                                trans.update()
                        else:
                            trans.status = Transaction.Status.ERROR
                            trans.update()
                    else:
                        charge = Charge.get(
                            trans.object_id) if trans.object_type == Transaction.ObjectType.CHARGE else None
                        if charge and (charge.source == Charge.Source.PORTAL_WIFI or charge.source == Charge.Source.WIFI):
                            if left_amount > 0:
                                charge_record = Charge()
                                charge_record.amount = int(real_amount)
                                charge_record.paid = int(real_amount)
                                #charge_record.user_id = trans.user_id
                                charge_record.user_id = charge.user_id
                                charge_record.status = Charge.Status.NEW
                                charge_record.score = 0
                                charge_record.source = charge.source
                                charge_record.ask_for = charge.ask_for
                                charge_record.ask_for_status = charge.ask_for_status
                                charge_record.pay_by = charge.pay_by
                                charge_record.insert()
                                trans.amount = charge_record.amount
                                trans.origin_object_id = trans.object_id
                                trans.object_id = charge_record.id
                            trans.update()
                            PayService.get_callback(trans).execute(trans)
                        else:
                            channel = trans.pay_type
                            channel_num = channel.find('ios_')

                            trans.update()
                            PayService.get_callback(trans).execute(trans)
                            if left_amount > 0:
                                trans_extra = TransactionExtraInfo()
                                trans_extra.real_amount = real_amount
                                trans_extra.transaction_ids = trans.id
                                trans_extra.detail = "充值卡充值，金额%s" % real_amount
                                trans_extra.insert()

                                charge_record = Charge()
                                charge_record.amount = left_amount
                                charge_record.paid = left_amount
                                charge_record.user_id = trans.user_id
                                charge_record.status = Charge.Status.NEW
                                charge_record.score = 0
                                charge_record.insert()

                                new_trans = Transaction()
                                new_trans.status = Transaction.Status.NEW
                                new_trans.amount = charge_record.amount
                                new_trans.user_id = trans.user_id
                                new_trans.object_type = Transaction.ObjectType.CHARGE
                                new_trans.object_id = charge_record.id
                                if channel_num >= 0:
                                    new_trans.pay_type = 'ios_' + Transaction.PayType.YEEPAY_CARD
                                else:
                                    new_trans.pay_type = Transaction.PayType.YEEPAY_CARD
                                new_trans.title = u"充值卡剩余充值"
                                new_trans.detail = u"充值卡剩余充值 %s" % left_amount
                                new_trans.callback = ""
                                new_trans.insert()

                                from bg_biz.pay.callback.charge import ChargeExecutor

                                ChargeExecutor().execute(new_trans)
                                trans_extra.transaction_ids = trans_extra.transaction_ids + "," + str(new_trans.id)
                                trans_extra.update()

        else:
            trans_id = request.args.get('p2_Order', None)
            trans = Transaction.get(trans_id)
            if trans.memo:
                trans.memo += ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
            else:
                trans.memo = ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
            trans.status = Transaction.Status.ERROR
            trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"易宝回调失败")


@PayView.route('/notify/ofpay', methods=['POST'])
def ofpay_notify():
    logger_pay.error("\n=================ofpay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        trains_id = request.form.get('sporder_id')
        ret_code = request.form.get('ret_code')
        trans = CardCharge.get(trains_id)
        if trans.memo:
            trans.memo += ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
        else:
            trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
        if int(ret_code) == 1:
            ChargeService.get_callback(trans).execute(trans)
            trans.update()
        else:
            trans.status = CardCharge.Status.ERROR
            trans.update()
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        return 'SUCCESS'
    return 'SUCCESS'

@PayView.route('/notify/hypay', methods=['POST','GET'])
def hypay_notify():
    logger_pay.error("\n=================ofpay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.args)
    try:
        trains_id = request.args.get('bill_id')
        bill_status = request.args.get('bill_status')
        trans = CardCharge.get(trains_id)
        trans.memo += ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
        if bill_status == "成功":
            ChargeService.get_callback(trans).execute(trans)
            trans.update()
        else:
            trans.status = CardCharge.Status.ERROR
            trans.update()
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        return 'OK'
    return 'OK'

@PayView.route('/notify/hiwifipay', methods=['POST', 'GET'])
@open_sign_verify
def hiwifipay_notify():
    logger_pay.error("\n=================hiwifipay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.args)

    try:
        data = g.data
        trade_status = data.get('trade_status', None)
        print trade_status
        if trade_status == "1":
                trans_id = request.args.get('trade_no', None)
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW or trans.status == Transaction.Status.ERROR:
                    trans.memo = ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
                    trans.pay_time = datetime.now()

                    trans.out_serial_no = request.args.get('trade_no', None)

                    real_amount = float(request.args.get('real_amount', 0)) * 100
                    left_amount = int(real_amount - trans.amount)
                    """if amount_change < 0:
                        if trans.object_type == Transaction.ObjectType.CHARGE and str(trans.callback).strip().endswith("type=wifi"):
                            close_amount = ConfigService.get_close_wifi_fee(real_amount)
                            new_amount = close_amount if close_amount else int(real_amount)
                        else:
                            new_amount = int(real_amount)
                        trans.amount =  new_amount
                    else:
                        new_amount = trans.amount"""
                    if left_amount < 0:
                        if trans.object_type == Transaction.ObjectType.CHARGE:
                            charge = Charge.get(trans.object_id)
                            if charge.source == Charge.Source.PORTAL_WIFI:
                                charge_record = Charge()
                                charge_record.amount = int(real_amount)
                                charge_record.paid = int(real_amount)
                                charge_record.user_id = trans.user_id
                                charge_record.status = Charge.Status.NEW
                                charge_record.score = 0
                                charge_record.source = charge.source
                                charge_record.insert()
                                trans.amount = charge_record.amount
                                trans.origin_object_id = trans.object_id
                                trans.object_id = charge_record.id
                                trans.update()
                                from bg_biz.pay.callback.charge import ChargeExecutor

                                ChargeExecutor().execute(trans)
                            else:
                                trans.status = Transaction.Status.ERROR
                                trans.update()
                        else:
                            trans.status = Transaction.Status.ERROR
                            trans.update()
                    else:
                        charge = Charge.get(
                            trans.object_id) if trans.object_type == Transaction.ObjectType.CHARGE else None
                        if charge and charge.source == Charge.Source.PORTAL_WIFI:
                            if left_amount > 0:
                                charge_record = Charge()
                                charge_record.amount = int(real_amount)
                                charge_record.paid = int(real_amount)
                                charge_record.user_id = trans.user_id
                                charge_record.status = Charge.Status.NEW
                                charge_record.score = 0
                                charge_record.source = charge.source
                                charge_record.insert()
                                trans.amount = charge_record.amount
                                trans.origin_object_id = trans.object_id
                                trans.object_id = charge_record.id
                            trans.update()
                            PayService.get_callback(trans).execute(trans)
                        else:
                            channel = trans.pay_type
                            channel_num = channel.find('ios_')
                            trans.update()
                            PayService.get_callback(trans).execute(trans)
                            if left_amount > 0:
                                trans_extra = TransactionExtraInfo()
                                trans_extra.real_amount = real_amount
                                trans_extra.transaction_ids = trans.id
                                trans_extra.detail = "充值卡充值，金额%s" % real_amount
                                trans_extra.insert()

                                charge_record = Charge()
                                charge_record.amount = left_amount
                                charge_record.paid = left_amount
                                charge_record.user_id = trans.user_id
                                charge_record.status = Charge.Status.NEW
                                charge_record.score = 0
                                charge_record.insert()

                                new_trans = Transaction()
                                new_trans.status = Transaction.Status.NEW
                                new_trans.amount = charge_record.amount
                                new_trans.user_id = charge_record.user_id
                                new_trans.object_type = Transaction.ObjectType.CHARGE
                                new_trans.object_id = charge_record.id

                                if channel_num >= 0:
                                    new_trans.pay_type = 'ios_' + Transaction.PayType.YEEPAY_CARD
                                else:
                                    new_trans.pay_type = Transaction.PayType.YEEPAY_CARD

                                new_trans.title = u"充值卡剩余充值"
                                new_trans.detail = u"充值卡剩余充值 %s" % left_amount
                                new_trans.callback = ""
                                new_trans.insert()

                                from bg_biz.pay.callback.charge import ChargeExecutor

                                ChargeExecutor().execute(new_trans)
                                trans_extra.transaction_ids = trans_extra.transaction_ids + "," + str(new_trans.id)
                                trans_extra.update()

        else:
            trans_id = request.args.get('trade_no', None)
            trans = Transaction.get(trans_id)
            trans.memo = ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
            trans.status = Transaction.Status.ERROR
            trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"HI-WIFI回调失败")


@PayView.route('/notify/apple', methods=['POST', 'GET'])
@open_sign_verify
def apple_notify():
    logger_pay.error("\n=================hiwifipay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.args)
    try:
        data = g.data
        print data
        trade_status = data.get('trade_status', None)
        print trade_status
        if trade_status == "1":
                trans_id = request.args.get('trade_no', None)
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
                    trans.pay_time = datetime.now()
                    trans.out_serial_no = request.args.get('trade_no', None)
                    trans.update()
                    PayService.get_callback(trans).execute(trans)


        else:
            trans_id = request.args.get('trade_no', None)
            trans = Transaction.get(trans_id)
            trans.memo = ', '.join("%s:%s" % (key, request.args[key]) for key in request.args)
            trans.status = Transaction.Status.ERROR
            trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"HI-WIFI回调失败")


@PayView.route('/gateway/notify/alipay', methods=['POST'])
def gateway_alipay_back_notify():
    logger_pay.error("\n=================alipay notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    try:
        trade_status = request.form.get('trade_status', None)
        if trade_status == u'TRADE_SUCCESS':
            verify_result = Alipay.verify_sign_md5(request.form)
            if verify_result:
                trans_id = request.form.get('out_trade_no', None)
                trans = GatewayTransaction.get(trans_id)
                if trans.status == GatewayTransaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                    trans.pay_time = request.form.get('gmt_payment', datetime.now())
                    trans.payment_account = request.form.get('buyer_email', None)
                    trans.out_serial_no = request.form.get('trade_no', None)
                    trans.status = GatewayTransaction.Status.FINISHED
                    trans.update()
                    url = GateWay.creat
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"支付宝回调失败")


@PayView.route('/gateway/notify/alipay_wap', methods=['POST'])
def gateway_alipay_wap_notify():
    logger_pay.error("\n=================alipay wap notify===========================\n")
    logger_pay.error(request.url)
    logger_pay.error(request.form)
    notify_data = request.form.get("notify_data", None)

    import xml.etree.cElementTree as et

    tree = et.fromstring(notify_data)
    sign = request.form.get('sign', None)
    trade_status = tree.find('trade_status').text
    trans_id = tree.find('out_trade_no').text
    gmt_payment = tree.find('gmt_payment').text
    alipay_trade_no = tree.find('trade_no').text
    buyer_email = tree.find('buyer_email').text
    try:
        if trade_status == u'TRADE_FINISHED':
            need_sign_str = "service=%s&v=%s&sec_id=%s&notify_data=%s" % (
                request.form.get('service'), request.form.get('v'), request.form.get('sec_id'), notify_data)
            verify_result = AlipayWap.verify_sign_md5(need_sign_str, sign)
            if verify_result:
                trans = Transaction.get(trans_id)
                if trans.status == Transaction.Status.NEW:
                    trans.memo = ', '.join("%s:%s" % (key, request.form[key]) for key in request.form)
                    trans.pay_time = gmt_payment
                    trans.out_serial_no = alipay_trade_no
                    trans.payment_account = buyer_email
                    PayService.get_callback(trans).execute(trans)
                    trans.update()
        return "success"
    except Exception as e:
        logger_pay.error(traceback.format_exc())
        logger_pay.error(e)
        raise AppError(u"支付宝回调失败")
