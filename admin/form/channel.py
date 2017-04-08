# -*- coding:utf-8 -*-
"""登录认证类表单"""
from sharper.lib import validator
from sharper.util import helper, string
from flask import flash

from flask_wtf import FlaskForm, validators
from wtforms import TextField, PasswordField, BooleanField, ValidationError
from wtforms.validators import *
from wtforms import TextField, PasswordField, BooleanField, validators, ValidationError, HiddenField,SelectField
from bg_biz.orm.admin import AdminUser
from bg_biz.orm.pic import Supplier


def special_chars(form, field):
    if field.data:
        if string.check_special_sign(field.data.strip()):
            raise ValidationError(u'只允许中英文、数字和下划线，不能输入特殊字符！')


class GroupForm(FlaskForm):
    id = HiddenField(u'id')
    name = TextField(u'名称', [
        optional(),
        Length(min=2, max=16, message=u'名称必须为2～16字符。')
    ]
                     )
    description = TextField(u'描述', [
        optional()]
                            )
    thumb = HiddenField(u"封面")
    thumb2 = HiddenField(u"封面2")
    thumb3 = HiddenField(u"封面3")
    shoot_time = TextField(u"拍摄时间")
    group_no = TextField(u"编号")
    images = HiddenField(u"images")
    status = BooleanField(u'状态')
    choices = list()
    suppliers = Supplier.query.filter_by(status=1).all()
    for t in suppliers:
        choices.append((t.id, t.name))
    supplier_id = SelectField(u'供应商', [DataRequired(message=u'请选择供应商')], choices=choices, coerce=int)


class ChannelForm(FlaskForm):

    id = HiddenField(u'id')
    name = TextField(u'名称', [
        optional(),
        Length(min=2, max=16, message=u'名称必须为2～16字符。')
    ]
                     )
    thumb = HiddenField(u"封面")
    description = TextField(u'描述', [
        Length(min=0, max=50, message=u'描述不能超过50字符。')]
                            )
    status = BooleanField(u'状态')


class SupplierForm(FlaskForm):

    id = HiddenField(u'id')
    name = TextField(u'名称', [
        optional(),
        Length(min=2, max=16, message=u'名称必须为2～16字符。')
    ]
                     )
    description = TextField(u'描述', [
        Length(min=0, max=50, message=u'描述不能超过50字符。')]
                            )
    status = BooleanField(u'状态')