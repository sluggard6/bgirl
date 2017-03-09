# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

from bg_biz.orm.sysconfig import SysConfig
from bg_biz.orm.user import User, UserVcode
from bg_biz.service.tool_service import ToolService
from sharper.flaskapp.orm.base import transaction
from sharper.lib.error import AppError
from sharper.lib.validator import is_mobile
from sharper.util.string import random_number
from sharper.util.app_util import get_app_name
from bg_biz.orm.app_log import SmsLog

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
    vcode_today = UserVcode.query.filter_by(phone=phone).filter("date(create_time)='%s'"%datetime.now().strftime("%Y-%m-%d")).all()
    vcode_today = sum([x.times for x in vcode_today])
    if vcode_today>9:
        raise AppError(u"今日获取短信过多，已关闭验证码发送")
    vcode_latest_log = UserVcode.query.with_lockmode("update").filter_by(phone=phone).filter_by(category=category).filter_by(app=app).filter(
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
        content = u"验证码：%s 欢迎您注册%s" % (vcode, get_app_name())
    elif category == UserVcode.Category.FORGET_PASS:
        content = u"您的验证码为：%s " % vcode
#     elif category == UserVcode.Category.CHANGE_PHONE_OLD:
#         content = u"您的验证码为：%s " % vcode
#     elif category == UserVcode.Category.CHANGE_PHONE_NEW:
#         content = u"您的验证码为：%s " % vcode
    else:
        content = u"您的验证码为：%s " % vcode
    need_switch = True
#     if category in [UserVcode.Category.CHANGE_PHONE_OLD, UserVcode.Category.CHANGE_PHONE_NEW]:
#         need_switch = False

    ToolService.send_sms(phone, content, need_switch=need_switch, app=app, scene=SmsLog.Scene.VCODE)
    if category == UserVcode.Category.REGISTER \
            and sms_config.get('green_channel', False) \
            and vcode_log.times >= sms_config.get('retry_times', 2):
        return vcode
    return None

class UserService:
    @classmethod
    @transaction
    def register(cls, phone, password):
        if User.query.filter_by(phone=phone).first():
            return AppError(msg=u'该手机号码已经被注册。')
        u = User.register(phone, password)
        return u

def validate_vcode(phone, code, category):
    """
    验证码验证
    """
    record = UserVcode.query.filter_by(phone=phone).filter_by(vcode=code).filter_by(category=category).first()
    limit_time = datetime.now() - timedelta(minutes=60)
    if record and record.status == UserVcode.Status.INIT and record.create_time > limit_time:
        record.status = UserVcode.Status.VERIFIED
        record.update()
        return True
    return False