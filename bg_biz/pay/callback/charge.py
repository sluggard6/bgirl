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

        user_balance = AccountDetail.get_balance(user.id)

        if charge.ask_for:
            charge.ask_for_status = Charge.AskStatus.PAYED
        if charge.discount_id:
            discount = UserDiscountInfo.get(charge.discount_id)
            if discount:
                discount.status = UserDiscountInfo.Status.USED
                discount.update()
        charge.status = Charge.Status.FINISHED
        charge.update()
        from bg_biz.service.user_service import UserService
        need_balance = True
        if (charge.memo and charge.memo.startswith("201508charge2")) and datetime.now() > datetime(2015, 8, 10, 00, 00, 00) and datetime.now() < datetime(2015, 8, 31, 23, 59, 59):
            if charge.memo=="201508charge2aug":
                new_check_aug = UserService.add_activity_action(charge.user_id,"new","201508charge2",limit_count=1,key2="aug",check=True)
                if new_check_aug:
                     UserService.add_activity_action(charge.user_id,"new","201508charge2",limit_count=1,key2="aug")
            else:
                new_check_sep = UserService.add_activity_action(charge.user_id,"new","201508charge2",limit_count=1,key2="sep",check=True)
                new_check_sep_delay = UserService.add_activity_action(charge.user_id,"new","201508charge2",limit_count=1,key2="sep_delay",check=True)
                if new_check_sep:
                    UserService.add_activity_action(charge.user_id,"new","201508charge2",limit_count=1,key2="sep")
                if new_check_sep_delay:
                    UserService.add_activity_action(charge.user_id,"new","201508charge2",limit_count=1,key2="sep_delay",key3=charge.amount)
                    need_balance = False
        if need_balance and charge.source not in (charge.Source.WIFI,charge.Source.PORTAL_WIFI):
            account_detail = AccountDetail()
            account_detail.user_id = user.id
            account_detail.ref_id = charge.id
            account_detail.amount = charge.amount
            account_detail.balance_before = user_balance
            account_detail.balance_after = user_balance + charge.amount
            account_detail.category = AccountDetail.Category.CHARGE

            source =str("callback_charge_")+str(account_detail.category)+str(account_detail.user_id)+str(account_detail.ref_id)+str(account_detail.amount)
            import hashlib
            m=hashlib.md5()
            m.update(source)
            score_log_lock = UserScoreLogLock()
            score_log_lock.sign = m.hexdigest()
            try:
                score_log_lock.insert()
            except Exception, e:
                print '=====duplicate_key=====user_id:',user.id,e
                return False
            account_detail.insert()

            order_id = account_detail.category+user.id+charge.id
            UserService.connect_platform_api(user,order_id,charge.amount,1,'charge balance')

            user.refresh_balance()
        user = User.get(charge.user_id)
        from bg_biz.orm.lottery import LotteryAct

        if charge.category!=Charge.Category.SYSTEM and 0:
            if charge.amount>=1000:
            #愚人节活动 充值大于10元 第七步入口
                #from bg_biz.service.user_action_service import MonitorUserAction
                MonitorUserAction.finish_step(MonitorUserAction.Category.RECHARGE_STEP, user)
            lottery = LotteryAct.get_by_key("zhuanpan")
            if lottery:
                UserService.add_lottery_chance(user,1,lottery=lottery)
        # 如果有充值任务，则在这里处理
        from bg_biz.task.add_task import AddTaskChain

        AddTaskChain.charge_process(user, charge)

        from bg_biz.task.add_task import WebViewExecutor
        rmb_amount = float(charge.amount)/100
        if (charge.source == charge.Source.WIFI or charge.source == charge.Source.PORTAL_WIFI) and need_balance:
            user = User.get(charge.user_id)
            day = UserService.charge_exchange_wifi(charge,user,trans=trans)
            add_task = AddTask.get(140)
            executor = WebViewExecutor(user.id, add_task)
            executor.execute()
            if charge.amount>=500 and datetime.now() > datetime(2015, 8, 10, 00, 00, 00) and datetime.now() < datetime(2015, 9, 27, 23, 59, 59):
                num  = charge.amount/500
                from bg_biz.service.tool_service import ToolService
                UserService.add_activity_action(user.id,"new","201509mooncake",key2=num,no_limit=True)
                #ToolService.add_pop(PopMessageButtonType.WEB,"成功抽取月饼","成功获取5月饼快去抽取福袋吧",phones=[charge.user.phone],url=pay_url_all)
                send_notification_rq("成功获取%s月饼快去抽取福袋吧"%num,[charge.user_id],action_type=Message.ActionType.WEBVIEW,uri="/activity/by_rule_key/201509mooncake")
            if user.area_id in [35,36,37,38] and charge.amount>=2500:
                add_task = AddTask.get(173)
                executor = WebViewExecutor(user.id, add_task)
                executor.execute()
            if 0:
                activity_key = "201601hicharge4"
                content = UserService.add_activity_action_new(charge.user_id,activity_key,get_content=True)
                evil_blood = int(content.get("evil_blood"))
                justice_blood = int(content.get("justice_blood"))
                if evil_blood>=0 and justice_blood>=0:
                    content["evil_blood"] = str(evil_blood-charge.amount)
                    content["edit_time"] = str(datetime.now())
                act_rule = RuleConfig.get_by_category_key(RuleConfig.Category.ACTIVITY, activity_key)
                act_rule.content = json.dumps(content)
                act_rule.update()
            if datetime.now() > datetime(2014, 12, 25, 00, 00, 00) and datetime.now() < datetime(2015, 01, 01, 23, 59, 59) and charge.amount>=2500:
                if UserActionLog.query.filter_by(key1="all").filter_by(key2="2014_christmas_charge") \
                    .filter_by(category=UserActionLog.Category.ADD_WIFI).filter_by(user_id=user.id).count() < 1:
                    UserService.delay_wifi(user, int(charge.amount/625))
                    UserService.add_user_action(user.id, UserActionLog.Category.ADD_WIFI, "all", "2014_christmas_charge",int(charge.amount/625),"圣诞活动延长上网时间")
                    from bg_biz.service.tool_service import ToolService
                    ToolService.add_msg("成功获得活动赠送上网时间%s天"%int(charge.amount/625),user.id,title="充值赠送上网时间")
                    ToolService.add_msg("成功获得活动赠送上网时间%s天"%int(charge.amount/625),user.id,title="充值赠送上网时间",type=Message.Type.SYSTEM)
            if charge.source == charge.Source.PORTAL_WIFI:
                selected_amount = charge.amount / 100
                paid_amount = charge.amount / 100
                if self.trans.origin_object_id:
                    original_charge = Charge.get(self.trans.origin_object_id)
                    if original_charge:
                        selected_amount = original_charge.amount / 100
                from bg_biz.service.tool_service import ToolService

                ios_c = self.trans.pay_type
                channel_num = ios_c.find('ios_')
                if channel_num >= 0:
                    ios_c = ios_c[4:]

                if ios_c == Transaction.PayType.YEEPAY_CARD:
                    msg = "恭喜您成功充值。你选择充值%s元，实际充值卡内金额%s元，成功兑换%s天上网时间，请留意是否到账，若未到账，请联系我们客服，客服电话4008217110" % (
                    selected_amount, paid_amount, day)
                    ToolService.send_sms(user.phone, msg, app=SmsLog.App.API, scene=SmsLog.Scene.CHARGE)
            if charge.pay_by:
                pay_by_user = User.get(charge.pay_by)
                notice_str = "%s已为您充值%s元购买天数：%s天，%s请享受美好的上网时光，并要记得答谢您的代充人噢！"%(pay_by_user.phone,day,rmb_amount,charge.memo or "")
                pay_for_str = "代付成功！您本次花费%s元，为%s账号成功购买%s天上网时间"%(rmb_amount,user.phone,day)
                send_notification_rq(pay_for_str,[pay_by_user.id])
                send_notification_rq(pay_for_str,[pay_by_user.id],type=Message.Type.SYSTEM)
                from bg_biz.service.tool_service import ToolService
                #ToolService.add_pop(PopMessageButtonType.CANCEL,"充值信息",notice_str,phones=[user.phone])
                send_notification_rq(notice_str,[user.id],type=Message.Type.NOTE)
                send_notification_rq(notice_str,[user.id],type=Message.Type.SYSTEM)
            elif charge.ask_for:
                ask_for_user = User.get(charge.ask_for)
                notice_str = "%s已为您充值%s元购买天数：%s天，%s请享受美好的上网时光，并要记得答谢您的代充人噢！"%(ask_for_user.phone,rmb_amount,day,charge.memo or "")
                pay_for_str = "代付成功！您本次花费%s元，为%s账号成功购买%s天上网时间"%(rmb_amount,user.phone,day)
                send_notification_rq(pay_for_str,[ask_for_user.id])
                send_notification_rq(pay_for_str,[ask_for_user.id],type=Message.Type.SYSTEM)
                from bg_biz.service.tool_service import ToolService
                #ToolService.add_pop(PopMessageButtonType.CANCEL,"充值信息",notice_str,phones=[user.phone])
                send_notification_rq(notice_str,[user.id],type=Message.Type.NOTE)
                send_notification_rq(notice_str,[user.id],type=Message.Type.SYSTEM)
            else:
                from bg_biz.service.tool_service import ToolService
                notice_str = "充值成功！您本次花费%s元，成功购买%s天上网时间。"%(rmb_amount,day)
                ToolService.add_msg(notice_str,user.id,title="充值成功",type=Message.Type.SYSTEM)


            if datetime.now() > datetime(2015, 07, 14, 00, 00, 00) and datetime.now() < datetime(2015, 07, 31, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                amount = charge.amount / 100
                if self.trans.pay_type == Transaction.PayType.YEEPAY_CARD:
                    key2 = "card"+str(amount)
                else:
                    amount = charge.amount / 50 if charge.discount_info else charge.amount / 100
                    day = ConfigService.get_wifi_day(amount)
                    key2 = "normal"+str(day)
                check_action = UserService.add_activity_action(charge.user_id,"new","201507_charge",limit_count=1,key2=key2,check=True)
                if check_action:
                    UserService.add_activity_action(charge.user_id,"new","201507_charge",limit_count=1,key2=key2)

            if datetime.now() > datetime(2015, 07, 14, 00, 00, 00) and datetime.now() < datetime(2015, 9, 30, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                amount = charge.amount / 100
                if self.trans.pay_type == Transaction.PayType.YEEPAY_CARD:
                    key2 = "card"+str(amount)
                else:
                    amount = charge.amount / 50 if charge.discount_info else charge.amount / 100
                    day = ConfigService.get_wifi_day(amount)
                    key2 = "normal"+str(day)
                UserService.add_activity_action(charge.user_id,"new","201509charge3",no_limit=True,key2=key2)

            if datetime.now() > datetime(2015, 07, 14, 00, 00, 00) and datetime.now() < datetime(2015, 10, 31, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                amount = charge.amount / 100
                day = ConfigService.get_wifi_day(amount,area_id=user.area_id)
                if day==30:
                    if UserService.add_activity_action(charge.user_id,"new","201510hicharge",limit_count=1,key2="12",check=True):
                        from sharper.flaskapp.kvdb import kvdb
                        r = kvdb.common
                        r.incr("201510hicharge_count")
                    UserService.add_activity_action(charge.user_id,"new","201510hicharge",limit_count=1,key2="11")
                    UserService.add_activity_action(charge.user_id,"new","201510hicharge",limit_count=1,key2="12")

            if datetime.now() < datetime(2015, 11, 30, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                #amount = charge.amount / 50 if charge.discount_info else charge.amount / 100
                #day = ConfigService.get_wifi_day(amount,area_id=user.area_id)
                if day>=30:
                    check_get,action = UserService.add_activity_action_new(charge.user_id,"201511hicharge2",limit_count=1,check=True)
                    if check_get:
                        from sharper.flaskapp.kvdb import kvdb
                        r = kvdb.common
                        r.incr("201511hicharge2_count")
                    UserService.add_activity_action_new(charge.user_id,"201511hicharge2",status=ActivityAction.Status.NEW,limit_count=1)
                    #UserService.delay_wifi(charge.user,day=7,admin_log_info="小乐答谢")

            if datetime.now() < datetime(2016, 9, 23, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                #amount = charge.amount / 50 if charge.discount_info else charge.amount / 100
                #day = ConfigService.get_wifi_day(amount,area_id=user.area_id)
                if day>=30:
                    check_get,action = UserService.add_activity_action_new(charge.user_id,"201609hicharge",limit_count=1,check=True)
                    if check_get:
                        from sharper.flaskapp.kvdb import kvdb
                        r = kvdb.common
                        r.incr("201611hicharge2_count")
                    UserService.add_activity_action_new(charge.user_id,"201609hicharge",status=ActivityAction.Status.NEW,limit_count=1)
                    #UserService.delay_wifi(charge.user,day=7,admin_log_info="小乐答谢")

            if datetime.now() < datetime(2016, 12, 18, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                #amount = charge.amount / 50 if charge.discount_info else charge.amount / 100
                #day = ConfigService.get_wifi_day(amount,area_id=user.area_id)
                if day>=30:
                    sql = '''SELECT sum(transaction.amount) FROM transaction WHERE status = 'finished' AND user_id = '%s';''' % (charge.user_id)
                    print sql
                    amount = db.engine.scalar(sql)
                    if amount>=5000:
                        check_get,action = UserService.add_activity_action_new(charge.user_id,"201612hicharge",limit_count=1,check=True)
                        if check_get:
                            from sharper.flaskapp.kvdb import kvdb
                            r = kvdb.common
                            r.incr("201612hicharge2_count")
                        UserService.add_activity_action_new(charge.user_id,"201612hicharge",status=ActivityAction.Status.NEW,limit_count=1)
                        title = '回馈消息'
                        category = '消息'
                        notify = '恭喜' + user.phone + '您可以去首页广告页面領取7天上网时间了,并有800积分赠送哦！'
                        ToolService.add_msg(notify, charge.user_id, display_area=Message.DisplayArea.EITHER, title=title,
                                            type=Message.Type.SYSTEM)
                        #UserService.delay_wifi(charge.user,day=7,admin_log_info="小乐答谢")


            if datetime.now() < datetime(2015, 11, 30, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                #amount = charge.amount / 50 if charge.discount_info else charge.amount / 100
                #day = ConfigService.get_wifi_day(amount,area_id=user.area_id)
                if day==30:
                    charge_check = Charge.query.filter_by(user_id=charge.user_id).filter(Charge.category!=Charge.Category.SYSTEM).filter_by(status=Charge.Status.FINISHED).count()
                    if charge_check<2:
                        UserService.add_activity_action_new(charge.user_id,"201511firstcharge",limit_count=1,status=ActivityAction.Status.GET)
                        UserService.delay_wifi(charge.user,day=30,admin_log_info="首次充值赠送")

            if datetime.now() < datetime(2015, 12, 31, 23, 59, 59) and not charge.ask_for and not charge.pay_by:
                if day==30 or day==7:
                    UserService.add_activity_action_new(charge.user_id,"201512endcharge",key1=str(day),status=ActivityAction.Status.NEW,limit_count=1)


            if datetime.now() > datetime(2015, 04, 22, 00, 00, 00) and datetime.now() < datetime(2015, 04, 30, 23, 59, 59):
#合并代码,一下是release部分
#                 send_notification_rq("成功帮用户%s充值%s天上网时间"%(user.phone,day),[charge.pay_by])
#                 send_notification_rq("%s用户成功帮您充值%s天上网时间"%(pay_by_user.phone,day),[user.id])
#             if datetime.now() > datetime(2015, 04, 22, 00, 00, 00) and datetime.now() < datetime(2015, 04, 30, 23, 59, 59):
#                 print "send_start 1111111111111111111111111111111111111"
                send_config = {400:40,900:150,2500:600,5000:2100}
                vip_send_config = {400:40,900:180,2500:800,5000:2400}
                charge_search = Charge.query.filter_by(user_id=charge.user_id).filter_by(status=Charge.Status.FINISHED).filter_by(category=Charge.Category.USER).first()
                if charge_search:
                    s_config = vip_send_config
                else:
                    s_config = send_config
                if s_config.has_key(int(charge.amount)):
                    user = User.get(charge.user_id)
                    UserService.add_score(user, s_config[int(charge.amount)], charge.id, UserScoreLog.Category.SYSTEM_ADD_SCORE,
                                              data=s_config[int(charge.amount)], desc="充值奖励")
        else:
            if charge.category!=Charge.Category.SYSTEM:
                if charge.user_id!=self.trans.user_id:
                    pay_by_user = User.get(self.trans.user_id)
                    notice_str = "%s已为您充值30元购买：%s%s，%s请享受美好的上网时光，并要记得答谢您的代充人噢！"%(pay_by_user.phone,charge.amount,get_balance_name(),charge.memo or "")
                    pay_for_str = "代付成功！您本次花费%s元，为%s账号成功购买%s%s"%(rmb_amount,user.phone,charge.amount,get_balance_name())
                    send_notification_rq(pay_for_str,[pay_by_user.id],type=Message.Type.SYSTEM)
                    send_notification_rq(notice_str,[user.id],type=Message.Type.SYSTEM)
                else:
                    from bg_biz.service.tool_service import ToolService
                    notice_str = "充值成功！您本次花费%s元，成功购买%s%s。"%(rmb_amount,charge.amount,get_balance_name())
                    ToolService.add_msg(notice_str,user.id,title="充值成功",type=Message.Type.SYSTEM)


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
