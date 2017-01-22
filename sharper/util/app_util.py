# -*- coding:utf-8 -*-
import re
from flask import request
from luhu_sharper.util.area_util import is_foxconn

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


def get_app_name(source=""):
    if is_foxconn(source):
        return u"智联云网"
    else:
        return u"Hi-WiFi"


def get_score_name(source=""):
    if is_foxconn(source):
        return u"康豆"
    else:
        return u"Hi点"


def get_balance_name(source=""):
    if is_foxconn(source):
        return u"康币"
    else:
        return u"Hi币"


def get_package_name():
    return ua_parse().get('package_name', '')


def must_update(g, ua):
    return False
    # print "client_version:%s\nua:%s" % (g.client_version,ua)
    if int(g.client_version) < 30:
        return get_area(ua) == Area.DAFENG
    # return True
    return False


def ua_parse():
    ret = dict()
    ua = request.headers.get("User-Agent", "unknown")

    if ua.find("com.jz.videocenter") != -1 or ua.find("hi.wifi") != -1 or ua.find("hiwifi") !=-1 or ua.find("Hi-WiFi") != -1:
        if ua.find('IOS') != -1:
            ua = re.findall(r"Mobile\/.*?\s(.*)",ua)
            ua = ua[0] if ua else request.headers.get("User-Agent", "unknown")
            package_name = ua[:ua.find("/")]
            client_version = ua[package_name.__len__() + 1:ua.find(' ')]
            infos = ua[ua.find("(") + 1:].split("; ")
            ret['package_name'] = package_name
            ret['client_version'] = client_version
            ret['model'] = infos[0]
            ret['os_version'] = infos[3]
            ret['device_id'] = infos[4]
            if infos.__len__() > 5:
                ret['manufacturer'] = infos[5]
            if infos.__len__() > 10:
                ret['context_id'] = infos[10]
            ret['os'] = 'iOS'

        else:
            package_name = ua[:ua.find("/")]
            client_version = ua[package_name.__len__() + 1:ua.find(' ')]
            infos = ua[ua.find("(") + 1:].split("; ")
            ret['package_name'] = package_name
            ret['client_version'] = client_version
            ret['model'] = infos[0]
            ret['os_version'] = infos[3]
            ret['device_id'] = infos[4]
            if infos.__len__() > 5:
                ret['manufacturer'] = infos[5]
            if infos.__len__() > 10:
                ret['context_id'] = infos[10]
            ret['os'] = 'Android'
    return ret
