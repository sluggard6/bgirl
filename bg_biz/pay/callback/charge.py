# -*- coding:utf-8 -*-

from bg_biz.pay.callback import Executor
from bg_biz.orm.pay.charge import Charge
from bg_biz.orm.user import User
from bg_biz.service.user_service import UserService

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class ChargeExecutor(Executor):
    def execute_internal(self, obj_id, trans=None):
        charge = Charge.get(obj_id)
        if not charge:
            return False
        user = User.get(charge.user_id)

        if charge.status != Charge.Status.NEW:
            return False

        charge.status = Charge.Status.FINISHED
        charge.update()

        if user:
            UserService.delay_wifi(user, charge.day, admin_log_info="VIP充值", category=1, obj_id=charge.id)

        return True
