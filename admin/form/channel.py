# -*- coding:utf-8 -*-
"""登录认证类表单"""
from sharper.lib import validator
from sharper.util import helper, string
from flask import flash

from flask_wtf import FlaskForm, validators
from wtforms import TextField, PasswordField, BooleanField, ValidationError
from wtforms.validators import *
from wtforms import TextField, PasswordField, BooleanField, validators, ValidationError, HiddenField
from bg_biz.orm.admin import AdminUser


def special_chars(form, field):
    if field.data:
        if string.check_special_sign(field.data.strip()):
            raise ValidationError(u'只允许中英文、数字和下划线，不能输入特殊字符！')


class GroupForm(FlaskForm):
    id = HiddenField(u'id')
    name = TextField(u'名称', [
        optional(),
        Length(min=2, max=16, message=u'名称必须为2～16字符。'),
        special_chars
    ]
                     )
    description = TextField(u'描述', [
        optional()]
                            )
    thumb = HiddenField(u"封面")

    images = HiddenField(u"images")
    status = BooleanField(u'状态')


class ChannelForm(FlaskForm):

    id = HiddenField(u'id')
    name = TextField(u'名称', [
        optional(),
        Length(min=2, max=16, message=u'名称必须为2～16字符。'),
        special_chars
    ]
                     )
    thumb = HiddenField(u"封面")
    description = TextField(u'描述', [
        Length(min=0, max=50, message=u'描述不能超过50字符。')]
                            )
    status = BooleanField(u'状态')
