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
    ShuMi = 'shumi'
    ChangTian = 'changtian'
    ChuangLan = 'chuanglan'
    FanMeng = 'fanmeng'
    LianTong = 'liantong'
    YunXin = 'yunxin'

    def send(self, phone, c):
        pass

    def send_batch(self, phones, c):
        raise NotImplementedError

    __display_cn__ = {
        ShuMi: u"数米",
        ChangTian: u"畅天",
        ChuangLan: u"创蓝",
        FanMeng: u"泛盟",
        LianTong: u"联通",
        YunXin: u"云信"
    }


_DEFAULT_TIMEOUT_ = 5  # seconds


class ShuMiSmsSender(SmsSender):
    def send(self, phone, c):
        if isinstance(c, unicode):
            c = c.encode('utf8')
        c = c.decode("utf8").encode(encoding="gbk")
        c = base64.standard_b64encode(c)
        url = "http://api.shumi365.com:8090/sms/send.do"
        pwd = '983461'
        timespan = datetime.now().strftime("%Y%m%d%H%M%S")
        params = {
            'userid': '410045',
            'pwd': md5("%s%s" % (pwd, timespan)).upper(),
            'mobile': phone,
            'timespan': timespan,
            'ext': 1,
            'content': c,
        }
        import socket

        socket.setdefaulttimeout(_DEFAULT_TIMEOUT_)
        res = urllib.urlopen(url, data=urllib.urlencode(params)).read()
        return res


class ChangTianSmsSender(SmsSender):
    def send(self, phone, msg):
        xml = send_sms(phone, msg)
        import xml.etree.cElementTree as et
        new_xml = xml.replace("gb2312", "utf-8")
        new_xml = unicode(new_xml, encoding='GB2312').encode('utf-8')
        tree = et.fromstring(new_xml)
        return tree.find('Result').text

    def send_batch(self, phones, msg):
        if isinstance(msg, unicode):
            msg = msg.replace(u'\xa0', u" ")
        msg = msg.encode(encoding="gb2312")

        url = "http://si.800617.com:4400/SendLenSmsGroups.aspx"

        params = {
            'un': 'shjpm-2',
            'pwd': '037756',
            'mobile': ",".join(phones),
            'msg': msg
        }

        xml = urllib.urlopen(url, data=urllib.urlencode(params)).read()

        import xml.etree.cElementTree as et

        new_xml = xml.replace("gb2312", "utf-8")
        new_xml = unicode(new_xml, encoding='GB2312').encode('utf-8')
        tree = et.fromstring(new_xml)
        return tree.find('Result').text


class ChuangLanSmsSender(SmsSender):
    def send(self, phone, msg):
        if isinstance(msg, unicode):
            msg = msg.encode('utf8')
        url = "http://www.clcjsms.com/msg/HttpSendSM"
        params = {
            'account': 'jiapingmi',
            'pswd': 'Tch123456',
            'mobile': phone,
            'msg': msg,
            'needstatus': 'true'
        }
        import socket

        socket.setdefaulttimeout(_DEFAULT_TIMEOUT_)
        params = urllib.urlencode(params)
        res = urllib.urlopen(url, data=params).read()
        status_code = res.split("\n")[0].split(",")[1]

        if status_code != "0":
            return status_code
        else:
            return res.split("\n")[1]

    def check_left(self):
        url = "http://www.clcjsms.com/msg/QueryBalance"
        params = {
            'account': 'jiapingmi',
            'pswd': 'Tch123456'

        }
        params = urllib.urlencode(params)
        res = urllib.urlopen(url, data=params).read()
        return res


class FMSmsSender(SmsSender):
    def send(self, phone, msg):
        msg=msg+'【乐无限】'
        url = "http://112.74.129.90:9890/cmppweb/sendsms?"
        if isinstance(msg, unicode):
            msg = msg.encode('utf8')
        params = {
            'uid': '507110',
            'pwd': md5('ZFE12345'),
            'mobile': phone,
            'srcphone': '106904587110',
            'msg': msg
        }
        res = urllib.urlopen(url, data=urllib.urlencode(params)).read()
        if res.find(",") != -1:
            return res.split(",")[1]
        return res


class YunXinSender(SmsSender):
    def send(self, phone, msg):
        xml = send_sms(phone, msg)
        import xml.etree.cElementTree as et
        new_xml = unicode(xml, encoding='GB2312').encode('utf-8')
        tree = et.fromstring(new_xml)
        return tree.text


class LianTongSender(SmsSender):
    def send(self, phone, msg):
        account = 'jpmxx'
        pwd = md5('ab8888').upper()
        send_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        val = u'''
<Group Login_Name="%s" Login_Pwd="%s" OpKind="0" InterFaceID="" SerType="01">
    <E_Time>%s</E_Time>
    <Item>
        <Task>
            <Recive_Phone_Number>%s</Recive_Phone_Number>
            <Content><![CDATA[%s]]></Content>
            <Search_ID>1001</Search_ID>
        </Task>
    </Item>
</Group>
''' % (account, pwd, send_time, phone, msg)
        if isinstance(val, unicode):
            val = val.encode('utf8')
        val = val.decode("utf8").encode(encoding="gbk")
        url = "http://qdif.vcomcn.cn/Opration.aspx"
        res = urllib.urlopen(url, data=val).read()
        return res


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

