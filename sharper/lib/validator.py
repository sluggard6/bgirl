# -*- coding: utf-8 -*-
"""
    lib/validator.py
    ~~~~~~~~~~~~~~

    数据格式验证

    :author: linnchord@gmail.com
    :date:2011-07-28

"""
import re

from .error import ParaValidateFailError
from ..util.helper import get_dict_val


def type_validate(obj, _type, condition=None):
    """
    obj:需要验证的对象
    _type:验证类型
    condition:验证附加条件 dict|list {'max':20,'min':10}
    """
    _type = _type.strip()

    if _type == 'mobile':
        return is_mobile(obj)
    elif _type == 'en-num':
        return re.compile(r'^[0-9a-zA-Z]+$').match(obj)
    elif _type == 'normalid':
        return re.compile(r'^[0-9a-zA-Z-_.]+$').match(obj)
    elif _type == 'number':
        return re.compile(r'^[0-9]+$').match(obj)
    elif _type == 'length':  # confition = {'max':100,'min':10 || 'eq':20}
        if condition:
            obj = obj.strip()
            length = len(obj)
            keys = condition.keys()
            if 'eq' in keys:
                return length == condition['eq']
            if 'max' in keys and 'min' in keys:
                return condition['min'] <= length <= condition['max']
            if 'max' in keys:
                return length <= condition['max']
            if 'min' in keys:
                return length >= condition['min']
        return False
    elif _type == 'email':
        return is_email(obj)
    elif _type == 'reg':
        if condition:
            return check_regx(obj, condition['reg'])
        return False
    elif _type == 'in':
        return obj in condition
    elif _type == 'int':
        return isinstance(obj, int)
    elif _type == 'numeric':
        return is_numeric(obj)
    elif _type == 'datetime':
        return is_datetime(obj)
    elif _type == 'date':
        return is_date(obj)
    elif _type == 'dict':
        return isinstance(obj, dict)
    elif _type == 'list':
        return isinstance(obj, list)
    elif _type == 'password':
        return validate_password(obj)
    else:
        return False


def paras_dict_validate(dic, rules):
    """
    dict:{'para1':'value', 'para2':value, ...}
    rules:[['para1','required, en-num, length', {'max':20,'min':10}],['para2','in',(1,0)], ...]
    note:如果有'required'规则则此必须在字符串序列第一位，否则无效。

    +   2013-06-27
        深层次指定字典值验证
        dict: {'user':{'body':{'height':180}}}
        ['user.body.height','required, int']
    """

    for r in rules:
        r_types = r[1].split(',')
        r_condition = {}
        msg = ''
        if len(r) > 2:
            r_condition = r[2]
        if len(r) > 3:
            msg = r[3]

        target = get_dict_val(r[0], dic)

        if is_blank(target):
            if r_types[0] == 'exist':
                if target is None:
                    raise ParaValidateFailError(
                        msg or (u'[%s]参数不存在,为必需参数,' % r[0]))
            if r_types[0] == 'required':
                raise ParaValidateFailError(
                    msg or (u'请求参数异常，未提交参数[%s]' % r[0]))
        else:
            for ty in r_types:
                ty = ty.strip()
                if ty != 'required' and ty != 'exist':
                    if not type_validate(target, ty, r_condition):
                        if not msg:
                            if ty == 'length':
                                if r_condition.get('min'):
                                    msg += u'至少%s字符，' % r_condition['min']
                                if r_condition.get('max'):
                                    msg += u'最多%s字符，' % r_condition['max']
                                if r_condition.get('eq'):
                                    msg += u'不是系统指定值，'
                            elif ty == 'datetime':
                                msg += u'日期格式不正确，'
                            elif ty == 'in':
                                msg += u'参数值不在系统指定范围内，'
                            elif ty == 'numeric':
                                msg += u'参数必须为数字，'
                            elif ty == 'mobile':
                                msg += u'参数必须为规范手机号码格式，'
                            elif ty == 'number':
                                msg += u'参数必须为数字串，'
                            elif ty == 'email':
                                msg += u'参数必须为email标准格式，'
                            elif ty == 'int':
                                msg += u'参数必须为整数，'
                            elif ty == 'password':
                                msg += u'密码需要6~16字符，且包含数字、字母、半角符号中至少两种字符，'
                            msg = u'参数[%s]异常，%s请确认。' % (r[0], msg)

                        raise ParaValidateFailError(msg)
    return True


def check_regx(_str, regx):
    """检查正则表达式匹配"""
    return re.compile(regx).match(_str)


def is_email(_str):
    return check_regx(_str.lower(), r'^([a-z\d\._-]+)@([\da-z\._-]+)\.([a-z]{2,6})$')

def is_mobile(_str):
    return check_regx(_str, r'^((\+86)|(86))?1[0-9]{10}$') or (str(_str) in SysConfig.get_config('test_phones').replace('"', '').replace("[", '').replace("]", "").replace(' ', '').replace('\r\n','').split(','))


def is_mobile_or_email(_str):
    return check_regx(_str, r'(^((\+86)|(86))?1[0-9]{10}$)|(^([a-z\d\._-]+)@([\da-z\._-]+)\.([a-z]{2,6})$)')


def is_datetime(_str):
    return check_regx(_str, r'^(19|20)[0-9]{2}\-(0|1)?[0-9]\-[0-3]?[0-9] [0-2]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9]$')


def is_date(_str):
    return check_regx(_str, r'^(19|20)[0-9]{2}\-(0|1)?[0-9]\-[0-3]?[0-9]$')


def is_blank(obj):
    return True if not obj and obj != 0 and obj != 0.0 else False

def is_numeric(num):
    return isinstance(num, (int, long, float, complex))


def validate_password(password):
    """
    验证密码 必须大于6字符 且包含至少2个字符集
    """
    from string import ascii_lowercase, ascii_uppercase, digits, punctuation
    flags = [bool(set(password) & set(s))
             for s in [ascii_lowercase, ascii_uppercase, digits, punctuation]]
    return flags.count(True) > 1 and 17 > len(password) > 5
