# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

from bg_biz.orm.sysconfig import SysConfig
from bg_biz.orm.user import User, UserVcode, ExchangeWifiRecord, UserHit
from bg_biz.service.tool_service import ToolService
from sharper.flaskapp.orm.base import transaction, db
from sharper.lib.error import AppError
from sharper.lib.validator import is_mobile
from sharper.util.string import random_number
from sharper.util.app_util import get_app_name
from bg_biz.orm.app_log import SmsLog
from bg_biz.orm.admin import AdminLog, AdminAction

__author__ = [
    "sluggrd"
]


@transaction
def send_user_vcode(phone, category, app=UserVcode.App.ANDROID, mac=None):
    vcode = random_number(4)

    sms_config = SysConfig.get_json("reg_sms_config")

    limit_times = sms_config.get('limit_times', 10)
    # 如果指定时间内发送过同类型的验证码，并且未使用过，则发送相同验证码
    keep_time = datetime.now() - timedelta(minutes=sms_config.get('keep_minutes', 30))
    delay_time = datetime.now() - timedelta(minutes=1)
    vcode_today = UserVcode.query.filter_by(phone=phone).filter(
        "date(create_time)='%s'" % datetime.now().strftime("%Y-%m-%d")).all()
    vcode_today = sum([x.times for x in vcode_today])
    if vcode_today > 9:
        raise AppError(u"今日获取短信过多，已关闭验证码发送")
    vcode_latest_log = UserVcode.query.with_lockmode("update").filter_by(phone=phone).filter_by(
        category=category).filter_by(app=app).filter(
        UserVcode.modify_time > delay_time.strftime("%Y-%m-%d %H:%M:%S")).first()
    if vcode_latest_log:
        raise AppError(u"获取短信过于频繁，请稍后再试")
    vcode_log = UserVcode.query.filter_by(phone=phone).filter_by(category=category).filter_by(app=app).filter_by(
        status=UserVcode.Status.INIT).filter(
        UserVcode.create_time > keep_time.strftime("%Y-%m-%d %H:%M:%S")).first()
    if vcode_log:
        if vcode_log.times > limit_times:
            raise AppError(u"获取次数过多，请稍后再试")
        vcode = vcode_log.vcode
        vcode_log.times = vcode_log.times + 1
        vcode_log.update()
    else:
        vcode_log = UserVcode()
        vcode_log.phone = phone
        vcode_log.category = category
        vcode_log.vcode = vcode
        vcode_log.mac = mac
        vcode_log.app = app
        vcode_log.insert()
    content = ''
    if not is_mobile(phone):
        raise AppError(u"请输入正确的手机号码")
    if category == UserVcode.Category.REGISTER:
        content = u"您在%s的验证码是：%s 。 请不要把验证码泄露给其他人。如非本人操作，可不用理会！" % (get_app_name(), vcode)
    elif category == UserVcode.Category.FORGET_PASS:
        content = u"您的验证码为：%s " % vcode
    # elif category == UserVcode.Category.CHANGE_PHONE_OLD:
    #         content = u"您的验证码为：%s " % vcode
    #     elif category == UserVcode.Category.CHANGE_PHONE_NEW:
    #         content = u"您的验证码为：%s " % vcode
    else:
        content = u"您的验证码为：%s " % vcode
    need_switch = True
    #     if category in [UserVcode.Category.CHANGE_PHONE_OLD, UserVcode.Category.CHANGE_PHONE_NEW]:
    #         need_switch = False

    print vcode_log
    ToolService.send_sms(phone, content, need_switch=need_switch, app=app, scene=SmsLog.Scene.VCODE)
    return vcode


class UserService:
    
    @classmethod
    def add_hit(cls, user_hit):
        sql = 'insert into user_hit (user_id,pic_id,status) values (%s,%s,%s) ON DUPLICATE KEY UPDATE status=%s' % (user_hit.user_id,user_hit.pic_id,user_hit.status,user_hit.status)
        print sql
        return db.engine.execute(sql)
        
        
    @classmethod
    @transaction
    def register(cls, phone, password):
        if User.query.filter_by(phone=phone).first():
            return AppError(msg=u'该手机号码已经被注册。')
        u = User.register(phone, password)
        return u

    @classmethod
    @transaction
    def delay_wifi(cls, user, day=None, seconds=None, admin_log_info="", category=None, obj_id=None):
        now = datetime.now()
        vipend = user.vipend
        if user:
            if vipend > now:
                if day:
                    net_end = vipend + timedelta(days=int(day))
                else:
                    net_end = vipend + timedelta(seconds=int(seconds))
            else:
                if day:
                    net_end = now + timedelta(days=int(day))
                else:
                    net_end = now + timedelta(seconds=int(seconds))
            user.vipend = net_end
            record = ExchangeWifiRecord()
            record.before_net_end = vipend
            record.category = category
            record.obj_id = obj_id

            if day:
                record.days = day
            elif seconds:
                record.seconds = seconds
            record.user_id = user.id
            record.after_net_end = net_end
            record.insert()
            user.update()
            if not admin_log_info:
                admin_log_info = '空'
            if not day:
                log = AdminLog.write(AdminAction.DelayNetEnd, user.id, ip="", key1=user.id,
                                     key2=admin_log_info, key3=seconds)
            else:
                log = AdminLog.write(AdminAction.DelayNetEnd, user.id, ip="", key1=user.id,
                                     key2=admin_log_info, key3=day)
        return True
    
    @classmethod
    def build_user_hit(cls, hits):
        dic = dict()
        for hit in hits:
            dic[str(hit.pic_id)] = hit.status
        return dic


def validate_vcode(phone, code, category):
    """
    验证码验证
    """
    record = UserVcode.query.filter_by(phone=phone).filter_by(vcode=code).filter_by(category=category).first()
    print record
    limit_time = datetime.now() - timedelta(minutes=60)
    if record:
        print limit_time > record.create_time
        print limit_time
    if record and record.status == UserVcode.Status.INIT and record.create_time > limit_time:
        print "---------------------------"
        record.status = UserVcode.Status.VERIFIED
        record.update()
        return True
    return False


