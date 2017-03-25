# -*- coding:utf-8 -*-
import copy
from functools import wraps
import json

from flask import request, jsonify, g
#from bg_biz.orm.third.third import ThirdActionLog
from sharper.util import encrypt_util

from bg_biz.pay.sign.rsa import RSASigner
#from bg_biz.orm.coop_app import CoopApp
from bg_biz.orm.sysconfig import SysConfig

__author__ = [
    '"liubo" <liubo@51domi.com>'
]


def open_sign_verify(f):
    @wraps(f)
    def do(*args, **kwargs):
        app_id = get_params('app_id')
        g.app_id = app_id

        ret, ret_code = check_sign()
        if not ret:
            return jsonify(success=False, error_code=ret_code['code'], error_msg=ret_code['msg'])

        return f(*args, **kwargs)

    return do


def check_sign():
    app_id = get_params('app_id')

    if not app_id:
        return False, RetInfo.APP_ID_ABSENCE
    encrypted_data = get_params("data")
    if not encrypted_data:
        return False, RetInfo.DATA_ABSENCE
    if app_id!="luhu":
        app_id = int(app_id)
        coop_app = CoopApp.get(app_id)

        if not coop_app:
            return False, RetInfo.APP_ID_NOT_EXIST
        aes_key = coop_app.aes_key
    else:
        aes_key = SysConfig.get_json("luhu_keys")["aes"]


    #encrypted_data =  encrypt_util.aes_base64_encrypt('{"pay_type": "alipay", "title": "3", "app_id": "luhu", "detail": "1", "amount": "0.04", "notify_url": "http://test.api.hi-wifi.cn/pay/notify/alipay", "out_trade_no": "1100037397", "sign": "GL5ID0VreGdmgM5mC8xQLrPZftbam8W+FSJwOyxIFy/2fcArR04DCdXdO9L/wq61SHkBa39uQJQjpc5cI/RJuOgvkVJft0svSLhWQwqDllKfeWrE6ZC5DoWsLYJVb74X+bpl2JSYs+Yf6ofXhdeXeX0Ym9bbNFlxl/NSELMa7Ng=", "return_url": "http://test.m.hi-wifi.cn/pay/1100037397/callback"}',aes_key)
    g.data = json.loads(encrypt_util.base64_aes_decrypt(encrypted_data, aes_key))
    g.app_id = app_id
    signature = g.data.get('sign', None)

    if not signature:
        return False, RetInfo.SIGN_ABSENCE

    rsa = RSASigner(app_id)
    message = sort_params(g.data)
    if rsa.verify(message, signature):
        ThirdActionLog.write(app_id,ThirdActionLog.Category.ACCESS,key1=request.path)
        return True, RetInfo.OK
    else:
        return False, RetInfo.SIGN_ERROR


def check_sign_old():
    app_id = int(get_params('appid'))

    if not app_id:
        return False, RetInfo.APP_ID_ABSENCE

    coop_app = CoopApp.get(app_id)
    if not coop_app:
        return False, RetInfo.APP_ID_NOT_EXIST
    if coop_app.category == CoopApp.Category.SINGLE:
        return True, RetInfo.OK

    signature = get_params('sign')
    params = []
    if request.method == 'GET':
        params = request.args
    elif request.method == 'POST':
        params = request.form

    if not signature:
        return False, RetInfo.SIGN_ABSENCE

    rsa = RSASigner(app_id)
    message = sort_params(params)

    if rsa.verify(message, signature):
        ThirdActionLog.write(app_id,ThirdActionLog.Category.ACCESS,key1=request.path)
        return True, RetInfo.OK
    else:
        return False, RetInfo.SIGN_ERROR


def copy_params(params):
    ret = {}
    for key in params.keys():
        ret[key] = params[key]
    return ret


def sort_params(params):
    new_params = copy_params(params)
    ks = new_params.keys()
    ks.sort()
    rlt = ''
    for k in ks:
        if type(new_params[k]) is unicode:
            new_params[k] = new_params[k].encode('utf8')
        new_params[k] = str(new_params[k])
        if k == "sign" or k == "sign_type":
            continue

        rlt = "%s&%s=%s" % (rlt, k, new_params[k])
    return rlt[1:]


def get_params(name):
    return request.form.get(name, None) or request.args.get(name, None)


class RetInfo(object):
    OK = {"code": 0, "msg": u""}

    SIGN_ERROR = {"code": 101, "msg": u"签名错误"}
    DATA_ABSENCE = {"code": 102, "msg": u"缺少参数data"}
    SIGN_ABSENCE = {"code": 104, "msg": u"缺少签名"}
    APP_ID_ABSENCE = {"code": 105, "msg": u"缺少appid"}
    APP_ID_NOT_EXIST = {"code": 106, "msg": u"appid不存在"}

    UID_ABSENCE = {"code": 121, "msg": u"缺少u_id"}
    UNAUTHORIZED = {"code": 122, "msg": u"用户未授权"}

    BIZ_ERROR = {"code": 130, "msg": u"业务错误"}
    SERVER_ERROR = {"code": 150, "msg": u"服务器错误"}

def add_third_url(app_id):
    def getFunc(f):
        @wraps(f)
        def do(*args, **kwargs):
            ThirdActionLog.write(app_id,ThirdActionLog.Category.ACCESS,key1=request.path)

            return f(*args, **kwargs)
        return do

    return getFunc
