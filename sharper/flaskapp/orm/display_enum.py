# -*- coding:utf-8 -*-
import re

__author__ = [
    '"liubo" <liubo@51domi.com>'
]


class DisplayEnum(object):
    """
    需要提供一个__display_cn__ 的dict，
    __display_cn__ = {
        DISCOUNT: u'折现',
        WITHDRAW: u'提现',
        DEAL_FAIL: u'交易失败退款',
        REJECT: u'拒收退款',
    }
    """
    _all_enum_cache = None

    @classmethod
    def get_display_cn(cls, status):
        values = getattr(cls, '__display_cn__')
        return values.get(status, "") if values else ""

    @classmethod
    def AllEnum(cls):
        """
        获取所有枚举值
        该值变量必须以大写字母开始
        """
        if not cls._all_enum_cache:
            cls._all_enum_cache = map(
                lambda x: cls.__dict__[x],
                filter(
                    lambda x: re.compile(r'^[A-Z][0-9a-zA-Z_]*$').match(x),
                    cls.__dict__
                )
            )
        return cls._all_enum_cache

    @classmethod
    def allEnumCnDict(cls):
        dic = {}
        for x in cls.AllEnum():
            dic[x] = cls.get_display_cn(x)
        return dic

    @classmethod
    def items(cls):
        return cls.__display_cn__.items()

