# -*- coding:utf-8 -*-
"""
    app/form.py
    ~~~~~~~~~~~~~~

    wtf form helper
"""
from flask import jsonify
from wtforms import SelectMultipleField, widgets


def orm2form(obj, form, include=(), out=()):
    """
    填充sql对象到表单 支持指定包含的字段和排除的字段 ('field_name', ...)

    obj/form 依赖 domi.orm.base/wtf_form

    @param obj: orm对象
    @param form: 指定表单
    @param include: 包含字段
    @param out: 排除字段
    @return:
    """
    if not include:
        include = obj.all_data_field
    if out:
        include = set(include) - set(out)
    for attr in include:
        if hasattr(obj, attr) and hasattr(form, attr):
            filed = getattr(form, attr)
            filed.data = getattr(obj, attr)


def form2orm(form, obj, include=(), out=()):
    """
    从指定表单获取字段值填充到sql对象 支持指定包含的字段和排除的字段 ('field_name', ...)
    obj/form 依赖 domi.orm.base/wtf_form

    @param obj: orm对象
    @param form: 指定表单
    @param include: 包含字段
    @param out: 排除字段
    @return:
    """
    if not include:
        include = obj.all_data_field
    if out:
        include = set(include) - set(out)
    for attr in include:
        if hasattr(obj, attr) and hasattr(form, attr):
            setattr(obj, attr, getattr(form, attr).data)


def get_form_errors(form, spliter=' '):
    if form.errors:
        ary = []
        for field_errors in form.errors.values():
            ary.append(spliter.join(field_errors))
        return spliter.join(ary)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()