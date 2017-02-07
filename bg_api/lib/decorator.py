# -*- coding: utf-8 -*-
"""装饰器"""
from functools import wraps

from flask import g
from sharper.flaskapp.helper import json_error, json_ok

def switch_ret(f):

    @wraps(f)
    def do(*args, **kwargs):
        do_switch_ret()
        return f(*args, **kwargs)
    return do

def do_switch_ret():
    g.ret_error_func = json_error
    g.ret_success_func = json_ok
