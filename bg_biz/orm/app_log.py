# -*- coding:utf-8 -*-
from datetime import datetime
from sharper.flaskapp.orm.base import BaseModel, db
from sharper.flaskapp.orm.display_enum import DisplayEnum

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP


__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class SmsLog(BaseModel):
    __tablename__ = 'sms_log'
    __table_args__ = {}

    id = Column(u'id', INTEGER(), nullable=False, primary_key=True, autoincrement=True)
    phone = Column(u'phone', VARCHAR(length=16), nullable=False)
    gateway = Column(u'gateway', VARCHAR(length=32), nullable=False)
    content = Column(u'content', VARCHAR(length=256), nullable=False)
    length = Column(u'length', INTEGER(), nullable=False)
    status = Column(u'status', VARCHAR(length=32), nullable=True, default=1)
    create_time = Column(u'create_time', DATETIME(), nullable=False, default=datetime.now)
    modify_time = Column(u'modify_time', TIMESTAMP(), nullable=True, default=datetime.now)
    ip = Column(u'ip', VARCHAR(length=32), nullable=True)
    app = Column(u'app', VARCHAR(length=32), nullable=True)
    scene = Column(u'scene', VARCHAR(length=32), nullable=True)

    class App(DisplayEnum):
        PORTAL = "portal"
        API = "api"
        AUTH = "auth"
        ADMIN = "admin"
        __display_cn__ = {
            PORTAL: u"portal",
            API: u"api",
            AUTH: u"auth",
            ADMIN: u"后台"
        }

    class Scene(DisplayEnum):
        REGISTER = "reg"
        FORGOT_PWD = "forgot_pwd"
        VCODE = "vcode" #验证码，针对不区分注册还是忘记密码的地方
        CHANGE_PHONE = "change_phone"
        WARN = "warn"
        OPERATION = "operation"
        TIPS = "tips"
        OTHER = "other"
        CHARGE = "charge"
        __display_cn__ = {
            REGISTER: u"注册",
            FORGOT_PWD: u"忘记密码",
            CHANGE_PHONE: u"修改手机号码",
            WARN: u"报警",
            TIPS: u"提醒",
            OPERATION: u"运营",
            CHARGE: u"充值",
            OTHER: u"其他"
        }