# -*- coding:utf-8 -*-
"""
    lib/signals.py
    ~~~~~~~~~~~~~~

    系统信号机制 代替event

    自定义信号 信号定义变量名和信号字符串一致
    my_signals = kidsdna_signals.signal('my_signals')

    订阅信号
    my_signals.connect(FUNCTION)


    信号订阅函数 在业务对象内定义
    def FUNCTION(obj, **kwds):
        print obj, dict(**kwds)

    发送信号 在业务对象内定义
    class Foo(object):
        def set_attr(self, val):
            self.attr = val
            my_signals.send((self, para1='sdf', para2=123))   #此处参数定义请保证和FUNCTION一致

"""
from blinker import Namespace

kidsdna_signals = Namespace()


#自定义信号 ------------------------------------------------------------------------------

#camp用户权限发生变化
admin_rup_changed = kidsdna_signals.signal('admin_rup_changed')

def init_signals_silvermoon():

    #用户权限发生变化 ------------------------------------
    from models.admin import AdminUser
    admin_rup_changed.connect(AdminUser.clear_all_user_permissions_cache)
