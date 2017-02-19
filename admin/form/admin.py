# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import validators, PasswordField

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class ModifyPasswordForm(FlaskForm):
    old_password = PasswordField(u'老密码', [
        validators.Required(message=u'老密码不能为空')]
    )
    new_password = PasswordField(u'新密码', [
        validators.Required(message=u'新密码不能为空')])
    repeat_password = PasswordField(u'重复密码', [
        validators.Required(message=u'重复密码不能为空')])

