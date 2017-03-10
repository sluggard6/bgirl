# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, validators, TextAreaField

__author__ = [
    '"liubo" <liubo@51domi.com>'
]


class SysConfigForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    name = TextField(u'key', [
        validators.Required(message=u'key不能未空')]
    )
    value = TextAreaField(u'value', [
        validators.Required(message=u'value不能为空')]
    )
    descr = TextField(u'描述', [
        validators.Required(message=u'描述不能为空')]
    )
