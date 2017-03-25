# -*- coding:utf-8 -*-
import M2Crypto
import base64
import urllib
from flask import current_app

import hashlib
import urllib2
from sharper.flaskapp.template import decimal_pretty
from bg_biz.service.config_service import ConfigService
from bg_biz.pay.sign.rsa import RSASigner
import json
from sharper.util import encrypt_util
from bg_biz.orm.sysconfig import SysConfig
gateway = "https://m.hi-wifi.cn/pay/gateway"


gateway = "http://127.0.0.1:8281/pay/gateway"

#gateway = ConfigService.get_host(ConfigService.Host.MOBILE)+"/pay/gateway"


class Hiwifipay(object):
    def __init__(self):
        pass

    @classmethod
    def populateURLStr(cls, params):
        from bg_biz.pay.open_decorator import copy_params

        new_params = copy_params(params)
        ks = new_params.keys()
        ks.sort()
        rlt = ''
        for k in ks:
            new_params[k] = str(new_params[k])
            if new_params[k] is None or len(new_params[k]) == 0 \
                    or k == "sign" or k == "sign_type" or k == "key":
                continue
            rlt = "%s&%s=%s" % (rlt, k, new_params[k])
        return rlt[1:]


    @classmethod
    def create_pay_url(cls, trans,extra_arguments=[]):
        ''' Make sure using unicode or utf-8 as params
        '''
        # 价格在这里进行转换5

        amount = trans.amount
        params = dict(from_trade_id=str(trans.id), title=trans.title, detail=trans.detail
                      , amount=str(amount),app_id="luhu",object_type = trans.object_type,
                      pay_type = trans.pay_type,extra_arguments=json.dumps(extra_arguments),
                      return_url="%s/pay/%s/callback" % (ConfigService.get_host(ConfigService.Host.MOBILE), trans.id),
                      notify_url=ConfigService.get_host(ConfigService.Host.API) + "/pay/notify/hiwifipay")
        request_data = gateway + '?'
        for key in params:
            data = params[key]
            if type(data) is unicode:
                data = data.encode("utf-8")
            request_data += key + '=' + urllib2.quote(data)
            request_data += '&'

        sign = RSASigner("luhu").sign(cls.populateURLStr(params))
        params["sign"] = sign
        print json.dumps(params)
        print type(json.dumps(params))
        data = encrypt_util.aes_base64_encrypt(json.dumps(params).encode("utf-8"),SysConfig.get_json("luhu_keys")["aes"])
        request_data += 'sign=' + sign + '&data='+urllib2.quote(data)
        print request_data
        # 返回结果
        return request_data

    @classmethod
    def create_test_url(cls, params):
        ''' Make sure using unicode or utf-8 as params
        '''
        # 价格在这里进行转换5

        request_data = gateway + '?'
        request_data =  "http://127.0.0.1:8290/third/add_wifi?"
        for key in params:
            data = params[key]
            if type(data) is unicode:
                data = data.encode("utf-8")
            request_data += key + '=' + urllib2.quote(data)
            request_data += '&'

        sign = RSASigner("22740038").sign(cls.populateURLStr(params))
        params["sign"] = sign
        print json.dumps(params)
        print type(json.dumps(params))
        data = encrypt_util.aes_base64_encrypt(json.dumps(params),"3z7pni63vj8mhkx0")
        request_data += 'sign=' + sign + '&data='+urllib2.quote(data)
        print request_data
        # 返回结果
        return request_data


    @classmethod
    def create_notify_url(cls, trans):
        ''' Make sure using unicode or utf-8 as params
        '''
        # 价格在这里进行转换
        #params = dict(trade_no=str(trans.id), trade_status="1", real_amount=trans.amount,app_id=trans.app_id)
        params = dict(trade_no=str(100), trade_status="1", real_amount="10",app_id="luhu")
        #request_data = trans.notify_url + '?'
        request_data = "http://127.0.0.1:8283/notify/hiwifipay?"
        for key in params:
            data = params[key]
            if type(data) is unicode:
                data = data.encode("utf-8")
            request_data += key + '=' + urllib2.quote(data)
            request_data += '&'
        #sign = RSASigner(trans.app_id).sign(cls.populateURLStr(params))
        sign = RSASigner("luhu").sign(cls.populateURLStr(params))
        params["sign"] = sign
        print json.dumps(params)
        print type(json.dumps(params))
        """if trans.app_id == "luhu":
            aes_key = SysConfig.get_json("luhu_keys")["aes"]
        else:
            coop_app = CoopApp.get(trans.app_id)
            aes_key = coop_app.aes_key if coop_app else """""
        aes_key = SysConfig.get_json("luhu_keys")["aes"]
        data = encrypt_util.aes_base64_encrypt(json.dumps(params).encode("utf-8"),aes_key)
        request_data += 'sign=' + sign +'&data='+urllib2.quote(data)
        # 返回结果
        return request_data



