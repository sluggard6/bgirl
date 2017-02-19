# -*- coding:utf-8 -*-
"""登录认证类表单"""
from sharper.lib import validator
from sharper.util import helper, string
from flask import flash

from flask_wtf import FlaskForm, validators
from wtforms import TextField, PasswordField, BooleanField, ValidationError
from wtforms.validators import *
from wtforms import TextField, PasswordField, BooleanField, validators, ValidationError
from bg_biz.orm.admin import AdminUser


def special_chars(form, field):
    if field.data:
        if string.check_special_sign(field.data.strip()):
            raise ValidationError(u'只允许中英文、数字和下划线，不能输入特殊字符！')


class AdminUserForm(FlaskForm):
    user_name = TextField(u'用户名', [
        optional(),
        Length(min=2, max=16, message=u'用户必须为2～16字符。'),
        special_chars
    ]
    )
    password = PasswordField(u'密码', [
        optional(),
        Length(min=6, max=16, message=u'请认真填写密码，6～16字符。')]
    )
    description = TextField(u'用户描述', [
        optional()]
                     )
    status = BooleanField(u'生效')


class AdminRoleForm(FlaskForm):
    name = TextField(u'角色名', [
        optional(),
        Length(min=2, max=16, message=u'角色必须为2～16字符。'),
        special_chars
    ]
    )
    description = TextField(u'描述', [
        Length(min=0, max=50, message=u'描述不能超过50字符。')]
    )
    status = BooleanField(u'生效')


class AdminPermissionForm(FlaskForm):
    id = TextField(u'id', [
        Regexp(r'^[0-9]{3,9}$', message=u'id格式错误')
    ]
    )
    parent_id = TextField(u'parent_id', [
        Regexp(r'^[0-9]{1,9}$', message=u'id格式错误')
    ]
    )
    name = TextField(u'权限名', [
        Length(min=2, max=16, message=u'权限名必须为2～16字符。'),
        special_chars
    ]
    )
    key = TextField(u'key', [
        optional(),
        Regexp(r'^[0-9a-zA-Z_\/]{5,50}$', message=u'key必须为英文数字下划线字符，5～50字符。')
    ]
    )
    path = TextField(u'操作路径', [
        optional()]
    )
    description = TextField(u'描述', [
        optional(),
        Length(min=0, max=50, message=u'描述不能超过50字符。')]
    )
    status = BooleanField(u'生效')


