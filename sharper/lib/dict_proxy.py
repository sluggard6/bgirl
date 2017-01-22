# -*- coding:utf-8 -*-
"""字典代理对象"""


class DictProxyObject(dict):
    """Container object for datasets: dictionary-like object that
       exposes its keys as attributes."""
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


dictp = DictProxyObject
