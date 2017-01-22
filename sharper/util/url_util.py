# -*- coding:utf-8 -*-

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


def add_param(url, key, value):
    if url.find("?") != -1:
        return "%s&%s=%s" % (url, key, value)
    else:
        return "%s?%s=%s" % (url, key, value)
