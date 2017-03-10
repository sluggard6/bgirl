# -*- coding:utf-8 -*-
import json
from bg_biz.orm.admin import AdminUser

__author__ = [
    '"liubo" <liubo@51domi.com>'
]
from flask_wtf import Form

from wtforms.validators import Required, Length
from wtforms import TextField, PasswordField, BooleanField, SelectField
from wtforms import TextField, validators, HiddenField, TextAreaField, SelectField, BooleanField, DateField,FileField,SelectMultipleField
from wtforms import widgets

class JsonField(TextField):
    widget = widgets.Select()

    def __init__(self, *args,**kwargs):
        new_kw = kwargs.copy()
        if new_kw.has_key("json_list"):
            del new_kw['json_list']
        super(JsonField, self).__init__(*args,**new_kw)
        self.json_list = kwargs.get("json_list",{})

def form2obj(form, obj, excludes=[],rep_quote=False):
    fields = form.__dict__.get("_fields")
    for field in fields:
        if hasattr(obj, field) and field not in excludes:
            form_field = getattr(form, field, None)
            if form_field or form_field == 0:
                d = form_field.data.replace('\"',"'") if rep_quote and isinstance(form_field.data,unicode) else form_field.data
                setattr(obj, field, d)


def obj2form(obj, form, excludes=[]):
    fields = form.__dict__.get("_fields")
    for field in fields:
        if hasattr(obj, field) and field not in excludes:
            obj_field = getattr(obj, field, None)
            form_field = getattr(form, field, None)
            if (obj_field or obj_field == 0) and form_field:
                #
                # if isinstance(form_field, SelectField):
                # choices = getattr(form_field, 'choices', [])
                # for i in range(0, choices.__len__()):
                # choice = choices[i]
                #         if obj_field == choice[0]:
                #             choice = (choice[0], choice[1], True)
                #             choices[i] = choice
                #     setattr(form_field, 'choices', choices)
                # else:
                if isinstance(form_field,JsonField):
                    setattr(form_field, 'json_list_data', json.loads(obj_field))
                setattr(form_field, 'data', obj_field)


def obj2obj(obj, obj1, excludes=[]):
    fields = obj.__dict__
    for field in fields:
        if hasattr(obj, field) and field not in excludes:
            obj_field = getattr(obj, field, None)
            form_field = getattr(obj1, field, None)
            if (obj_field or obj_field == 0) and not form_field:
                #
                # if isinstance(form_field, SelectField):
                # choices = getattr(form_field, 'choices', [])
                # for i in range(0, choices.__len__()):
                # choice = choices[i]
                #         if obj_field == choice[0]:
                #             choice = (choice[0], choice[1], True)
                #             choices[i] = choice
                #     setattr(form_field, 'choices', choices)
                # else:
                if field:
                    setattr(obj1, field, obj_field)


class LoginForm(Form):
    user_name = TextField('用户名', [
        Required(message=u'请填写账号名'), ]
    )
    password = PasswordField('密 码', [
        Required(message=u'请填写密码'),
        Length(min=6, max=16, message=u'请认真填写密码')]
    )
    remembered = BooleanField(u'保持登录1周')
    return_url = HiddenField(u'保存跳转链接')
    # recaptcha_code = RecaptchaField(u'验证码')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False
        user = AdminUser.get_by_name(self.user_name.data)
        if not user:
            self.user_name.errors = [u'该用户不存在']
            return False
        if not user.status:
            self.user_name.errors = [u'该用户已被禁用！']
            return False
        if not user.check_password(self.password.data):
            self.password.errors = [u'密码错误，请确认。']
            return False

        self.user = user
        return True
