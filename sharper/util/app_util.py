# -*- coding:utf-8 -*-
import re
from flask import request

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


def get_app_name(source=""):
    return u"昧昧"

def get_package_name():
    return ua_parse().get('package_name', '')



def ua_parse():
    ret = dict()
    ua = request.headers.get("User-Agent", "unknown")

    if ua.find("bgirl") != -1:
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