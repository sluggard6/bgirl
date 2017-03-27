# -*- coding:utf-8 -*-
import M2Crypto
import base64
import urllib
from datetime import timedelta
from flask import current_app

import hashlib
import urllib2
from sharper.flaskapp.template import decimal_pretty
from bg_biz.service.config_service import ConfigService


gateway = "https://www.alipay.com/cooperate/gateway.do"


class Alipay(object):
    ALIPAY_RSA_PRIVATE = 'MIIEpQIBAAKCAQEA2ujHGXxEmbv5N0kjodcqSxHGNmo+qy86KnnOdrzxEbuvHQwYHluQ5zur0rIEP3g6p2fekcKI22CFD1h9sKhm5pFtVvzY+aXBLWDSZXetEgZxX3nSre6KU80EWAPAgxZXOOeL7QTH8BbH2W6sxUt0j1BR8GmnkEeXNVnRTh1T9cJ+HFCvPoVDa6Mx2TPG/OBHBsL+J689S5BX/5IehKLkfqZQsD8DI7GV0XaxuBHek04A1aAKIaLvL56+Yr16sMozxfdH4yduixPT7gboCHt8I4orYZozwlZvkrccFOSUJW05ZqalmutElRJOHAR1lZlm7u1FqbN1SfJ0caOhmSp7rQIDAQABAoIBAQCJ6/19XiEupxMmtQshLZp0/7bdk+T2H+RK3MGrZ/GO1axH5dXQUqqiNaNVNVmdz5dM4BGHzoRBi7dp6rwOMJvciyXTl6zw5XEnsQf+a/98CtklaXDGqzM2B0bEWWDSdqHvtVsgs1FxQDkcEjICgD7pCJcHnNm4+pIXSAaqa6n5fSzY7kr00FBGvHvDGh1hn6WUwYt2u1WuqmIj3t164OFOwbYpr3q6tGtIa46oEw0IHK1ostVKUZuaRROoaMzbwZrSR2blt/7nuqih3Gc7XC5vD+6tDtzcvIoA+ZWa50YsnT+rs9o+O6/GxIwTL5UCm/nCoZITKHQtqvIAm6yjCfKhAoGBAPzqhwmEkWKDRqPKy4o/FbDtAUC3zYgUM7de1+Ov3dXtc04FbdbdC5vV+mF4xR11Nbd6wKELjFJE9eE9nGoBGKXJVd50l4P9EwMagAe81QMwl0+ao7Ml1CcDqThUvtmboKuRPJNTkAJ/duz/QbVQUrzLjd2a4z1KLOjRS1eUNQB1AoGBAN2UGT4LeTNahZICGE4gpHF7RJy+RkFYqtJfzuxC684b7ZWe+Ka9zaMnXpWgXG1TLiG6pbCDralcT9vKWoYwhLUKbIT4mO1Qu3e2QC8w0IcTu0DUU5gnpQElKzL9CySc730bS92nSbZd66mtd++H/9pwFPwWnAtlcwCEC1pjjadZAoGBAL4Z2h5BUrXlTndWut7SxA8UVdi7TvV1mdm+pC8zxV5C+GQwmHrj8xHTKDuTdzXJH/MlhRyHfZVo2BfRI3xaDpiuWKi4ohpHYr72cD1gpgubvl/LMDg7utcIXW1F5Z3S6FWM+ScTrC70eANzaYRLN6VIqv1iqmMrGc51YlgVwjDxAoGAQ2SRDOL2eR0WNSN3+wNIoM9qPfZNbgCm7BeB2zA7glPSPki8vhJKok4OIZpFombDSDT5wic6waE3FNWGFPxa0Kmb+hGWic+dRTrkaLYDJqJkuMIbrtKYCDIi4n4+TmOBH98WgxMng1UroU8GhI8rzWd7qnTB/2FayhRfU52l7vkCgYEA9EanJNrSyibkle8OlP0wQcNuGSTYaoprFOD/SjpEdnvLgY8j7PrnUtDsJVh/gGFt3lxeknWBZz+BxbrnnMgwt2iabq8iYyYOUmMLl5a1s1Q7L1HqQsp86e+NFOzL1E2wmY+uLW8PcAIwHs1vQbtsfzmPyrxJjSgNBedduYGvzNI='
    account = "2810396709@qq.com"

    @classmethod
    def sign_rsa(cls, data):
        if isinstance(data, unicode):
            data = data.encode("utf-8")
        key = M2Crypto.RSA.load_key_string(cls.ALIPAY_RSA_PRIVATE)
        m = M2Crypto.EVP.MessageDigest('sha1')
        m.update(data)
        digest = m.final()
        signature = key.sign(digest, "sha1")
        return urllib.quote_plus(base64.b64encode(signature))

    alipay_rsa_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2ujHGXxEmbv5N0kjodcqSxHGNmo+qy86KnnOdrzxEbuvHQwYHluQ5zur0rIEP3g6p2fekcKI22CFD1h9sKhm5pFtVvzY+aXBLWDSZXetEgZxX3nSre6KU80EWAPAgxZXOOeL7QTH8BbH2W6sxUt0j1BR8GmnkEeXNVnRTh1T9cJ+HFCvPoVDa6Mx2TPG/OBHBsL+J689S5BX/5IehKLkfqZQsD8DI7GV0XaxuBHek04A1aAKIaLvL56+Yr16sMozxfdH4yduixPT7gboCHt8I4orYZozwlZvkrccFOSUJW05ZqalmutElRJOHAR1lZlm7u1FqbN1SfJ0caOhmSp7rQIDAQAB'
    partner = "2016080300154007"
    key = "evXk728NyjEEV2jmb6agRA=="

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
    def sign(cls, params):
        sign = hashlib.md5(cls.populateURLStr(params) + cls.key).hexdigest()
        return sign

    '''
      校验支付宝返回的参数，交易成功的通知回调.
      检查签名是否正确.
      
      params为支付宝传回的数据。
    '''

    @classmethod
    def verify_sign_md5(cls, params, verify=True, transport="http"):
        sign = params.get('sign')
        locSign = cls.sign(params)
        if sign is None or locSign != sign:
            return False
        else:
            return True

    @classmethod
    def create_pay_url(cls, trans, sign_type='MD5', source=None):
        ''' Make sure using unicode or utf-8 as params
        '''
        # 价格在这里进行转换
        if source == "gateway":
            return_url = "%s/pay/gateway/%s/callback" % (ConfigService.get_host(ConfigService.Host.MOBILE), trans.id)
            notify_url = ConfigService.get_host(ConfigService.Host.API) + "/pay/gateway/notify/alipay"
        else:
            #return_url = "%s/pay/%s/callback" % (ConfigService.get_host(ConfigService.Host.MOBILE), trans.id)
            #notify_url = ConfigService.get_host(ConfigService.Host.API) + "/pay/notify/alipay"
            return_url = "%s/pay/%s/callback" % ('http://192.168.1.105', trans.id)
            notify_url = 'http://192.168.1.105'+ "/pay/notify/alipay"
        amount = decimal_pretty(float(trans.amount) / 100)
        params = dict(out_trade_no=str(trans.id), subject=trans.title, body=trans.detail, _input_charset="utf-8",
                      service='create_direct_pay_by_user', total_fee=str(amount), payment_type="1",
                      seller_id=cls.partner,
                      return_url=return_url,
                      notify_url=notify_url)

        params['partner'] = cls.partner
        sign = cls.sign(params)
        request_data = gateway + '?'
        for key in params:
            data = params[key]
            if type(data) is unicode:
                data = data.encode(params['_input_charset'])
            request_data += key + '=' + urllib2.quote(data)
            request_data += '&'
        request_data += 'sign=' + sign + '&sign_type=' + sign_type
        # 返回结果
        return request_data

    @classmethod
    def create_account_data_url(cls, start_date, end_date):
        '''
        start_date和end_date为str，格式为“yyyy-MM-dd HH:mm:ss”
        '''
        params = dict(partner=cls.partner, gmt_create_start=start_date, gmt_create_end=end_date,
                      _input_charset="utf-8",
                      service='export_trade_account_report')

        sign = cls.sign(params)
        request_data = gateway + '?'
        for key in params:
            data = params[key]
            if type(data) is unicode:
                data = data.encode(params['_input_charset'])
            request_data += key + '=' + urllib2.quote(data)
            request_data += '&'
        request_data += 'sign=' + sign + '&sign_type=MD5'
        return request_data

    @classmethod
    def single_trade_check(cls, trans):
        start_date = trans.create_time + timedelta(seconds=-800)
        end_date = trans.create_time + timedelta(seconds=800)
        start_date = "%s" % start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date = "%s" % end_date.strftime("%Y-%m-%d %H:%M:%S")
        url = Alipay().create_account_data_url(start_date, end_date)
        print url
        resp = urllib2.urlopen(url).read()
        ret = {}
        alipay_trans_map = {}
        if resp:
            import xml.etree.cElementTree as et

            tree = et.fromstring(resp)
            content = tree.findtext('response/csv_result/csv_data')
            if content.find("<![CDATA[") == 0:
                content = content["<![CDATA[".__len__():-("]]>".__len__())]
            if content:
                for line in content.split("\n")[1:]:

                    # 外部订单号,账户余额（元）,时间,流水号,支付宝交易号,交易对方Email,交易对方,用户编号,收入（元）,支出（元）,交易场所,商品名称,类型,说明,
                    infos = line.split(",")
                    #if int(infos[0])==check_trans_id:
                    #    print "yesy",trans_id
                    if infos.__len__() > 8 and infos[8]:
                        if int(infos[0])==int(trans.id):
                            trans_id = int(infos[0])
                            amount = int(round(float(infos[8]) * 100))
                            create_time = infos[2]
                            ali_trade = infos[4]


                            ret[trans_id] = {"amount": amount, "fee": 0,"create_time":create_time,"ali_trade":ali_trade}
                            break


        return ret


    @classmethod
    def create_pay_str_mobile(cls, trans):
        amount = decimal_pretty(float(trans.amount) / 100)
        detail = trans.detail.replace("\n", "")
        params = {
            "out_trade_no": str(trans.id),
            "subject": trans.title,
            "body": detail,
            "total_fee": str(amount),
            'seller': cls.account,
            'notify_url': ConfigService.get_host(ConfigService.Host.API) + "/notify/alipay",
            'partner': cls.partner
        }

        before_sign_str = '''partner="%s"&seller="%s"&out_trade_no="%s"&subject="%s"&body="%s"&total_fee="%s"&notify_url="%s"''' \
                          % (
            params['partner'], params['seller'], params['out_trade_no'], params['subject'], params['body'],
            params['total_fee'], params['notify_url'])
        sign = cls.sign_rsa(before_sign_str)
        request_data = '%s&sign="%s"&sign_type="RSA"' % (before_sign_str, sign)

        return request_data.encode("utf-8")

    @classmethod
    def verify_sign_rsa_a(cls, msg, signature):
        if isinstance(msg, unicode):
            msg = msg.encode("utf-8")
        if isinstance(signature, unicode):
            signature = signature.encode("utf-8")

        from M2Crypto import BIO, RSA, EVP
        import base64

        bio = BIO.MemoryBuffer(cls.alipay_rsa_public_key)
        rsa = RSA.load_pub_key_bio(bio)

        pubkey = EVP.PKey()
        pubkey.assign_rsa(rsa)
        pubkey.reset_context()
        pubkey.verify_init()

        pubkey.verify_update(msg)
        #print pubkey
        s = base64.decodestring(signature)
        #print s
        print '00000000000000000000',pubkey.verify_final(s)
        if pubkey.verify_final(s) == 1:
            print '1111111111111111',pubkey.verify_final(s)
            return True
        print '222222',pubkey.verify_final(s)
        return False


    @classmethod
    def verify_sign_rsa(cls,params):
        sign = params.get('sign')
        print 'sign--------------',sign
        sort_str = cls.populateURLStr(params)
        print 'sort_str==============',sort_str
        #locSign = cls.sign_rsa(sort_str)
        return cls.verify_sign_rsa_a(sort_str,sign)

    @classmethod
    def decrypted_rsa(cls, msg):
        from M2Crypto import BIO, RSA

        bio = BIO.MemoryBuffer(cls.ALIPAY_RSA_PRIVATE)
        rsa = RSA.load_key_bio(bio)

        msg = base64.decodestring(msg)
        i = 0
        ret = []
        while (i < msg.__len__()):
            ret.append(rsa.private_decrypt(msg[i:i + 128], RSA.pkcs1_padding))
            i += 128
        return "".join(ret)


class AlipayWap(Alipay):
    GATEWAY_URL = "http://wappaygw.alipay.com/service/rest.htm"  # 支付宝wap支付接口地址
    SIGN_TYPE = "MD5"  # 签名方式，0001为RSA

    @classmethod
    def get_token(cls, trans, merchant_url="http://m.hi-wifi.cn", source=None):
        '''
        获取token
        '''
        if source == "gateway":
            return_url = "%s/pay/gateway/%s/callback" % (ConfigService.get_host(ConfigService.Host.MOBILE), trans.id)
            notify_url = ConfigService.get_host(ConfigService.Host.API) + "/pay/gateway/notify/alipay"
        else:
            return_url = "%s/pay/%s/callback" % (ConfigService.get_host(ConfigService.Host.MOBILE), trans.id)
            notify_url = ConfigService.get_host(ConfigService.Host.API) + "/pay/notify/alipay_wap"
        amount = decimal_pretty(float(trans.amount) / 100)
        params = {}
        params['format'] = 'xml'
        params['v'] = '2.0'
        params['req_data'] = '''
        <direct_trade_create_req>
            <subject>%s</subject>
            <out_trade_no>%s</out_trade_no>
            <total_fee>%s</total_fee>
            <seller_account_name>%s</seller_account_name>
            <call_back_url>%s</call_back_url>
            <notify_url>%s</notify_url>
            <out_user>%s</out_user>
            <merchant_url>%s</merchant_url>
            <pay_expire>3600</pay_expire>
        </direct_trade_create_req>
        ''' % (
            trans.title, trans.id, str(amount), cls.account,
            return_url,
            notify_url, trans.user_id or 0, merchant_url)

        params['req_data'] = params['req_data'].replace("\n", "").replace(" ", "").replace("\t", "")
        params['service'] = 'alipay.wap.trade.create.direct'
        params['sec_id'] = cls.SIGN_TYPE
        params['partner'] = cls.partner
        params['req_id'] = trans.id  # 支付流水

        params['sign'] = Alipay.sign(params)

        ret_params = urllib2.urlopen(
            "%s?%s" % (cls.GATEWAY_URL, "&".join(["%s=%s" % (k, params[k]) for k in params.keys()]))).read()

        params = {}
        for pair in ret_params.split("&"):
            k, v = pair.split('=')
            params[k] = urllib.unquote_plus(v)

        ret_data = params['res_data']

        request_token = ""
        if "<request_token>" in ret_data:
            start = ret_data.find("<request_token>") + "<request_token>".__len__()
            end = ret_data.find("</request_token>")
            request_token = ret_data[start:end].strip()

        return request_token

    @classmethod
    def create_pay_url(cls, trans, source=None):
        token = cls.get_token(trans, merchant_url=trans.callback, source=source)
        deal_params = dict()
        deal_params['format'] = 'xml'
        deal_params['v'] = '2.0'
        deal_params['service'] = 'alipay.wap.auth.authAndExecute'
        deal_params['sec_id'] = cls.SIGN_TYPE
        deal_params['partner'] = cls.partner
        deal_params['req_data'] = '''
        <auth_and_execute_req>
            <request_token>
                %s
            </request_token>
        </auth_and_execute_req>
        ''' % (token)
        deal_params['req_data'] = deal_params['req_data'].replace("\n", "").replace(" ", "").replace("\t", "")

        deal_params['sign'] = Alipay.sign(deal_params)
        return "%s?%s" % (cls.GATEWAY_URL, "&".join(["%s=%s" % (k, deal_params[k]) for k in deal_params.keys()]))


    @classmethod
    def verify_sign_md5(cls, need_sign_str, sign):
        if sign == hashlib.md5(need_sign_str + cls.key).hexdigest():
            return True
        return False

class AlipayAPP(Alipay):
    GATEWAY_URL = "http://wappaygw.alipay.com/service/rest.htm"  # 支付宝wap支付接口地址
    SIGN_TYPE = "RSA"  # 签名方式，0001为RSA

    @classmethod
    def create_pay_mobile(cls, trans, sign_type='RSA', source=None):
        ''' Make sure using unicode or utf-8 as params
        '''
        # 价格在这里进行转换
        print '--------source--------',source
        if source == "gateway":
            return_url = "%s/pay/gateway/%s/callback" % (ConfigService.get_host(ConfigService.Host.MOBILE), trans.id)
            notify_url = ConfigService.get_host(ConfigService.Host.API) + "/pay/gateway/notify/alipay_app"
        else:
            return_url = "%s/pay/%s/callback" % (ConfigService.get_host(ConfigService.Host.MOBILE), trans.id)
            notify_url = ConfigService.get_host(ConfigService.Host.API) + "/pay/notify/alipay_app"
        amount = decimal_pretty(float(trans.amount) / 100)
        print '--------amount--------',amount
        params = {
            "service": "mobile.securitypay.pay",
            "partner": cls.partner,
            "notify_url": notify_url,
            "out_trade_no": str(trans.id),
            "subject": trans.title,
            "seller_id": cls.account,
            "total_fee":str(amount),
            "body":trans.detail
        }
        print '--------service--------',params['service']
        before_sign_str = '''service="%s"&partner="%s"&_input_charset="utf-8"&notify_url="%s"&out_trade_no="%s"&subject="%s"&payment_type="1"&seller_id="%s"&total_fee="%s"&body="%s"''' \
                          % (
            params['service'], params['partner'], params['notify_url'], params['out_trade_no'], params['subject'],params['seller_id'], params['total_fee'],params['body'])
        print '--------before sign str--------',before_sign_str
        sign = cls.sign_rsa(before_sign_str)
        request_data = '%s&sign="%s"&sign_type="RSA"' % (before_sign_str, sign)
        print '--------request data--------',request_data
        return request_data.encode("utf-8")

