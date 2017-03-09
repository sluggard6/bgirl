# -*- coding:utf-8 -*-
"""
    util/sms.py
    ~~~~~~~~~~~~~~

    simple sms tools

"""
import base64
from datetime import datetime
import urllib
from sharper.flaskapp.orm.display_enum import DisplayEnum

from sharper.util.string import md5, random_number
from sharper.util.sms_util import send_sms


def gen_reg_vcode(default_length=4):
    return random_number(default_length)


class SmsSender(DisplayEnum):
    MEILIAN = 'meilian'

    def send(self, phone, c):
        pass

    def send_batch(self, phones, c):
        raise NotImplementedError

    __display_cn__ = {
        MEILIAN: u"美联"
    }


_DEFAULT_TIMEOUT_ = 5  # seconds

class MeiLianSender(SmsSender):
    def send(self, phone, c):
        apikey = "add1c1dffbe23016abb3356a3866aae5"
        url = 'http://m.5c.com.cn/api/send/index.php'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        encode = 'UTF-8'
        username = 'filter'  # 用户名
        password_md5 = '1ADBB3178591FD5BB0C248518F39BF6D'  # 32位MD5密码加密，不区分大小写
        values = {'username': username,
                  'password_md5': password_md5,
                  'apikey': apikey,
                  'mobile': phone,
                  'content': c,
                  'encode': encode}
        headers = {'User-Agent': user_agent}
        data = urllib.parse.urlencode(values)
        req = urllib.request.Request(url + '?' + data)
        response = urllib.request.urlopen(req)
        the_page = response.read()


__sms_sender_config__ = {
    SmsSender.ShuMi: ShuMiSmsSender,
    SmsSender.ChangTian: ChangTianSmsSender,
    SmsSender.ChuangLan: ChuangLanSmsSender,
    SmsSender.FanMeng: FMSmsSender,
    SmsSender.LianTong: LianTongSender,
    SmsSender.YunXin: YunXinSender
}


def send(phone, c, sender_type=SmsSender.ChangTian):
    sender = __sms_sender_config__.get(sender_type)()
    return sender.send(phone, c)


def send_batch(phone, c, sender_type=SmsSender.ChangTian):
    sender = __sms_sender_config__.get(sender_type)()
    return sender.send_batch(phone, c)

