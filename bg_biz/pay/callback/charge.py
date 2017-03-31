# -*- coding:utf-8 -*-
import json
from flask import g
#from bg_biz.job.notification import send_notification_rq
#from bg_biz.orm.activity import ActivityAction
#from bg_biz.orm.discount import UserDiscountInfo
#from bg_biz.orm.message import Message, PopMessageButtonType
#from bg_biz.orm.rule_config import RuleConfig
from bg_biz.pay.callback import Executor
from bg_biz.orm.pay.charge import Charge,ChargeRecords
from bg_biz.orm.user import User
from bg_biz.service.user_service import UserService
from bg_biz.orm.pay.account_detail import AccountDetail
#from bg_biz.orm.add_task import AddTask
from bg_biz.orm.pay.transaction import Transaction
from datetime import datetime
#from bg_biz.orm.user import UserActionLog
from bg_biz.service.config_service import ConfigService
#from bg_biz.service.user_action_service import MonitorUserAction
from sharper.flaskapp import kvdb
#from sharper.util.app_util import get_balance_name
from bg_biz.orm.app_log import SmsLog
from sharper.flaskapp.orm.base import db


__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class ChargeExecutor(Executor):
    def execute_internal(self, obj_id,trans=None):
        charge = Charge.get(obj_id)
        if not charge:
            return False
        print 'ChargeExecutor--charge--',charge
        user = User.get(charge.user_id)

        if charge.status != Charge.Status.NEW:
            return False

        charge.status = Charge.Status.FINISHED
        charge.update()

        if user:
            UserService.delay_wifi(user, 365)

        return True


class NewChargeExecutor(Executor):
    def execute_internal(self, obj_id):
        charge = ChargeRecords.get(obj_id)
        if not charge:
            return False
        user = User.get(charge.user_id)

        if charge.status != ChargeRecords.Status.NEW:
            return False

        from bg_biz.orm.lottery import LotteryAct
        from bg_biz.service.user_service import UserService
        from bg_biz.service.client_service import BalanceService
        if charge.category!=Charge.Category.SYSTEM:
            lottery = LotteryAct.get_by_key("zhuanpan")
            UserService.add_lottery_chance(user,1,lottery=lottery)
        # 如果有充值任务，则在这里处理
        from bg_biz.task.add_task import AddTaskChain

        AddTaskChain.charge_process(user, charge)
        from bg_biz.task.add_task import WebViewExecutor
        if charge.charge_type == ChargeRecords.ChargeType.SCORE:
            b_type = "score"
            totalListPrice = charge.charge_num/2
            totalSalesPrice = charge.amount
            UserService.new_balance(user,charge.id,totalListPrice,totalSalesPrice,charge.charge_num,type=b_type)
        elif charge.charge_type == ChargeRecords.ChargeType.BALANCE:
            b_type = "balance"
            totalListPrice = charge.charge_num
            totalSalesPrice = charge.amount
            UserService.new_balance(user,charge.id,totalListPrice,totalSalesPrice,charge.charge_num,type=b_type)
        else:
            UserService.delay_wifi(user, charge.charge_num)
        charge.status = ChargeRecords.Status.FINISHED
        charge.update()
        return True
