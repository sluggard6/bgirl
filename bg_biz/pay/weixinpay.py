# -*- coding:utf-8 -*-
import uuid
from bg_biz.service.config_service import ConfigService
from sharper.flaskapp.helper import get_client_ip
import xml.etree.ElementTree as ET
import time
import random
import urllib2
import hashlib
from urllib import quote
from bg_biz.pay.callback.charge import ChargeExecutor

__author__ = [
    '"John Chan" <chenfazhun@163.com>'
]

url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
key = 'bYnfpw4cVUNPDdyIxxBoYtrzp1OQlEGu'
hiwifi_appid = 'wx11eaa73053dd1666'
hiwifi_mch_id = '1254530101'
foxconn_appid = 'wxb866e7bbbcae3a4a'
foxconn_mch_id = '1364524902'


class WXpay(object):
    def __init__(self):
        pass

    @classmethod
    def get_pay_prepay_id(self, trans, source=None):

        notify_url = ConfigService.get_host(ConfigService.Host.API) + "/pay/notify/wxpay"


        # amount = decimal_pretty(float(trans.amount) / 100)
        params = dict(body=trans.title, out_trade_no=str(trans.id), total_fee=str(trans.amount),
                      spbill_create_ip=get_client_ip(), notify_url=notify_url, trade_type="APP")
        if source:
            appid = foxconn_appid
            mch_id = foxconn_mch_id
        else:
            appid = hiwifi_appid
            mch_id = hiwifi_mch_id
        params['appid'] = appid
        params['mch_id'] = mch_id
        params['nonce_str'] = self.createNoncestr()

        sign = self.getSign(params)
        params['sign'] = sign

        print '------------------weixin------------------', sign
        print '------------------', params
        xml = self.arrayToXml(params)
        res = urllib2.urlopen(url, xml).read()
        print 'res-----------------------------', res
        array = self.xmlToArray(res)
        print '---------------', array

        data = dict(appid=appid, partnerid=mch_id, prepayid=array['prepay_id'], package="Sign=WXPay",
                    noncestr=self.createNoncestr(), timestamp=int(time.time()))
        data_sign = self.getSign(data)
        data['sign'] = data_sign
        # data['callbackurl'] = '/pay/'+trans.id+'/callback'
        return str(data)

    @classmethod
    def queryOrderTest(self, trans, source=None):
        if source:
            appid = foxconn_appid
            mch_id = foxconn_mch_id
        else:
            appid = hiwifi_appid
            mch_id = hiwifi_mch_id
        info = {}
        url = 'https://api.mch.weixin.qq.com/pay/orderquery'
        params = dict(out_trade_no=trans.id)
        params['appid'] = appid
        params['mch_id'] = mch_id
        params['nonce_str'] = self.createNoncestr()

        sign = self.getSign(params)
        data = '''<xml>
                   <appid>%s</appid>
                   <mch_id>%s</mch_id>
                   <nonce_str>%s</nonce_str>
                   <out_trade_no>%s</out_trade_no>
                   <sign>%s</sign>
                   </xml>''' % (
            appid, mch_id, params['nonce_str'], params['out_trade_no'], sign)
        req = urllib2.Request(url=url, headers={'Content-Type': 'application/xml', 'charset': 'UTF-8'}, data=data)
        res = urllib2.urlopen(req)
        data_str = str(res.read())
        print data_str
        arry_data = self.xmlToArray(data_str)
        print 'data------------------', arry_data
        return_code = arry_data['return_code']
        result_code = arry_data['result_code']
        print return_code, result_code
        if return_code == 'SUCCESS' and result_code == 'SUCCESS':

            total_fee = arry_data['total_fee']
            print 'success-----------', total_fee, '------------', trans.amount
            if str(trans.amount) == str(total_fee):
                print 'total_fee-', total_fee
                # ChargeExecutor.execute(trans)
                info = {"id": trans.id, "amount": total_fee}
        return info

    @classmethod
    def arrayToXml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        print '-----------', arr
        for k, v in arr.iteritems():
            print k, v
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    @classmethod
    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    @classmethod
    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    @classmethod
    def createNoncestr(self, length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    @classmethod
    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    @classmethod
    def getSign(self, obj):
        """生成签名"""
        # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        # 签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String, key)
        # 签名步骤三：MD5加密
        String = hashlib.md5(String).hexdigest()
        # 签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_
