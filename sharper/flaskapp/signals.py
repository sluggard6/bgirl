# -*- coding:utf-8 -*-
"""
    core/lib/signals.py
    ~~~~~~~~~~~~~~

    系统信号机制 代替event

    自定义信号 信号定义变量名和信号字符串一致
    my_signals = mige_signals.signal('my_signals')

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


#所有信号请从mige_signals派生
mige_signals = Namespace()



#自定义信号 ------------------------------------------------------------------------------

#
# #post更新tag变化
# post_tags_changed = mige_signals.signal('post_tags_changed')
# #用户积分等级提升
# user_level_up = mige_signals.signal('user_level_up')
# #用户积分变化
# user_credit_changed = mige_signals.signal('user_credit_changed')
# #camp用户权限发生变化
# camp_rup_changed = mige_signals.signal('camp_rup_changed')
#


def init_signals():pass

    # #post更新tag变化 ------------------------------------
    # from core.models.motive import Motive
    # post_tags_changed.connect(Motive.update_from_post)
    #
    # #用户权限发生变化 ------------------------------------
    # from core.models.camp_sys import CampUser
    # camp_rup_changed.connect(CampUser.clear_all_user_permissions_cache)
