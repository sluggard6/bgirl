# -*- coding:utf-8 -*-
import json
from flask import request, session, g
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum
from luhu_biz.orm.sysconfig import SysConfig

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]
FOXCONN_AREA_ID = 3


class Area(DisplayEnum):
    FOXCONN = "foxconn"
    NORMAL = "normal"
    DAFENG = "dafeng"

    __display_cn__ = {
        FOXCONN: u"富士康",
        NORMAL: u"通用",
        DAFENG: u"达丰",
    }


_foxconn_package_ = "foxconn.hi.wifi"


def get_area(ua):
    # 富士康单独处理，对于富士康生产的手机，ua中会包含“foxconn”，不用包名判断会出错
    if ua.find(_foxconn_package_) != -1:
        return Area.FOXCONN
    for area in [Area.DAFENG, Area.NORMAL]:
        if ua.find(area) != -1:
            return area
    return Area.NORMAL


def is_foxconn(source=""):
    '''
    是否富士康版本
    '''
    if source == "portal":
        area_configs = SysConfig.get_json("area_id_config")
        area_id = int(g.area_id or 0)
        if area_id in area_configs["foxconn"]:
            return True
        else:
            return False
    else:
        foxconn_flag = False
        ua = request.headers.get("User-Agent", "unknown").lower()
        if ua.find(_foxconn_package_) != -1:
            foxconn_flag = True
        elif request.args.get('area', '') == "foxconn":
            foxconn_flag = True
        elif request.args.get('areaid', 0) == 3 and request.args.get('uitype', '') == 'foxconn':
            foxconn_flag = True
        elif request.form.get('postdata', None):
            try:
                data = json.loads(request.form.get('postdata'))
                if data.get('areaid', 0) == 3 and data.get('uitype', '') == 'foxconn':
                    foxconn_flag = True
            except Exception:
                pass
        if foxconn_flag:
            session['is_foxconn'] = True
            return True
        return session.get('is_foxconn', False)


def is_demo():
    '''
    是否demo版本
    '''
    ua = request.headers.get("User-Agent", "unknown").lower()
    if ua.find("demo") != -1:
        return True
    return False


def clear_foxconn_mark():
    session.pop('is_foxconn', '')