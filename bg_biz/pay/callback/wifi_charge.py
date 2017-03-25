# -*- coding:utf-8 -*-
import calendar
from datetime import datetime, timedelta, date
from sharper.lib.error import AppError, WrongOperationError
from bg_biz.pay.callback import Executor
from bg_biz.orm.pay.wifi_charge import WifiCharge, WifiChargeRecord
from bg_biz.orm.user import  User
from bg_biz.service.tool_service import ToolService
from bg_biz.orm.app_log import SmsLog

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class WifiChargeExecutor(Executor):
    def execute_internal(self, obj_id):
        wifi_charge = WifiCharge.get(obj_id)
        if wifi_charge.status != WifiCharge.Status.NEW:
            raise WrongOperationError(u"wifi充值记录 %s 状态为： %s" % (wifi_charge.id, wifi_charge.status_cn))
        is_new = False
        # 如果帐号不存在，则创建帐号
        wifi_account = UserWifiAccount.get_by_account(wifi_charge.account)
        if not wifi_account:
            wifi_account = UserWifiAccount.gen_by_account(wifi_charge.account)
            wifi_account.net_start = datetime.now()
            is_new = True

        if wifi_charge.category == WifiCharge.Category.MONTH:
            days = wifi_charge.month * 30
        else:
            days = wifi_charge.day
        net_start, net_end = cal_net_end(wifi_account.net_end, days)
        wifi_account.net_end = net_end
        if wifi_account.user_id:
            user = User.get(wifi_account.user_id)
            user.net_end = wifi_account.net_end
        wifi_account.save()
        # 充值成功，发送短信
        if is_new:
            msg = "您的上网帐号：%s 密码：%s 现已开通，上网有效期至：%s " % (
                wifi_account.account, wifi_account.get_password(), wifi_account.net_end.strftime("%Y-%m-%d"))
        else:
            msg = "您的上网帐号：%s  密码：%s 续费成功，当前上网有效期至：%s " % (
                wifi_account.account, wifi_account.get_password(), wifi_account.net_end.strftime("%Y-%m-%d"))
        wifi_charge.status = WifiCharge.Status.FINISHED
        wifi_charge.update()

        ToolService.send_sms(wifi_charge.account, msg, app=SmsLog.App.API, scene=SmsLog.Scene.CHARGE)

        charge_record = WifiChargeRecord()
        charge_record.net_end = net_end
        charge_record.net_start = net_start
        charge_record.wifi_account_id = wifi_account.id
        charge_record.amount = wifi_charge.amount
        charge_record.insert()
        if datetime.now() > datetime(2015, 04, 22, 00, 00, 00) and datetime.now() < datetime(2015, 04, 30, 23, 59, 59):
            send_config = {400: 40, 900: 150, 2500: 600, 5000: 2100}
            vip_send_config = {400: 40, 900: 180, 2500: 800, 5000: 2400}
            charge_search = WifiCharge.query.filter_by(user_id=wifi_charge.user_id).filter_by(
                status=WifiCharge.Status.FINISHED).first()
            if charge_search:
                s_config = vip_send_config
            else:
                s_config = send_config
            if s_config.has_key(int(wifi_charge.amount)):
                user = User.get(wifi_charge.user_id)
                from luhu_biz.service.user_service import UserService

                UserService.add_score(user, s_config[int(wifi_charge.amount)], wifi_charge.id,
                                      UserScoreLog.Category.SYSTEM_ADD_SCORE,
                                      data=s_config[int(wifi_charge.amount)], desc="充值奖励")


def cal_net_end(net_end, days):
    start_day = now = datetime.now()
    if not net_end or net_end <= now:
        pass
    else:
        start_day = net_end

    end_day = start_day + timedelta(days=days)
    return start_day, datetime(end_day.year, end_day.month, end_day.day,
                               hour=23,
                               minute=59, second=59)




    # start_day, end_day = monthrange(now.year, now.month)
    # user.net_end = datetime(now.year, now.month, end_day, hour=23, minute=59, second=59)
    # user.net_start = datetime(now.year, now.month, start_day, hour=0, minute=0, second=0)
