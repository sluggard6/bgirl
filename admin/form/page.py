# -*- coding:utf-8 -*-
from flask.ext.wtf import Form

from bg_biz.orm.page import PageContent, PageModule
from wtforms import SelectField, StringField, BooleanField, IntegerField, TextAreaField, HiddenField,\
    validators
from wtforms.validators import NumberRange, DataRequired

from flask.ext.wtf import Form

__author__ = 'Frank'

class PageModuleForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    page = SelectField(u'所属页面', [DataRequired(message=u'请选择所属页面')], coerce=str)
    des = StringField(u'简介', [DataRequired(message=u'请输入页面简介')])
    category = SelectField(u'显示类型', [DataRequired(message=u'请选择显示类型')], coerce=str)
    text = StringField(u'标题文本')
    icon = StringField(u'标题ICON')
    style = StringField(u'样式扩展')
    extend = StringField(u'扩展内容')
    status = BooleanField(u'状态')
    rank = IntegerField(u'排序权重',[NumberRange(message=u'请输入数字')],default=0)


class PageContentForm(Form):
    page = StringField(u'所属页面')
    module_id = StringField(u'所属组件',[NumberRange(min=1,message=u'所属页面错误')])
    #desc = StringField(u'简介', [DataRequired(message=u'请输入页面简介')])
    # promotion_id = SelectField(u'关联推广', [DataRequired(message=u'请选择类型')], coerce=int)
    # coop_app_id = SelectField(u'关联app', [DataRequired(message=u'请选择类型')], coerce=int)
    title = StringField(u'标题', [DataRequired(message=u'标题不能为空')])
    #brief = StringField(u'简介', [DataRequired(message=u'简介不能为空')])
    desc = TextAreaField(u'描述')
    url = StringField(u'url', [DataRequired(message=u'')])
    #rank = StringField(u'rank', [DataRequired(message=u'')])
    choices = list()
    image = HiddenField(u"图片")
    resource_id = StringField(u'资源id')
    source_id = StringField(u'内容id')

    style = StringField(u'额外的样式配置')
    category = SelectField(u'类型', [DataRequired(message=u'请选择类型')], choices=choices, coerce=int)
