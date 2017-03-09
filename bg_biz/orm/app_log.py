# -*- coding:utf-8 -*-
from datetime import datetime
from luhu_sharper.flaskapp.orm.base import BaseModel, db
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum
from luhu_biz.job.tools import write_app_log, write_app_log_async
from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME, TIMESTAMP

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class AppLog(BaseModel):
    __bind_key__ = 'data'
    __tablename__ = 'app_log'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    device_id = db.Column(db.String(100), nullable=True)
    key1 = db.Column(db.String(50), nullable=True)
    key2 = db.Column(db.String(50), nullable=True)
    key3 = db.Column(db.String(50), nullable=True)
    data = db.Column(db.String(500), nullable=True)
    ip = db.Column(db.String(15), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)


    @classmethod
    def write(cls, action, user_id=None, device_id=None, key1=None, key2=None, key3=None, data=None, ip=None):
        if not ip:
            try:
                from flask import request

                ip = request.headers.get('X-Forwarded-For', None) or request.remote_addr
            except Exception:
                pass
        data_json = {"action": action, "user_id": user_id, "device_id": device_id, "key1": key1, "key2": key2,
                     "key3": key3,
                     "data": data, "ip": ip, "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        write_app_log_async(data_json)


class AppLogNew(BaseModel):
    __bind_key__ = 'data'
    __tablename__ = 'app_log_new'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    device_id = db.Column(db.String(100), nullable=True)
    key1 = db.Column(db.String(50), nullable=True)
    key2 = db.Column(db.String(50), nullable=True)
    key3 = db.Column(db.String(50), nullable=True)
    data = db.Column(db.String(500), nullable=True)
    ip = db.Column(db.String(15), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)


class AppAction:
    # 登录 {'action':'Login', 'key1':'email/phone/tqq/weibo/auto_login', 'key2':'web/client'}
    Login = "Login"

    # 网站注册
    WebReg = "WebReg"

    # 客户端激活操作
    ClientActive = "ClientActive"

    # 客户端注册
    ClientReg = "ClientReg"

    # webview统计
    WebViewTrack = "WebViewTrack"

    # 流量交换app统计
    AppTrack = "AppTrack"

    # web用户访问统计
    WebTrack = "WebTrack"

    # 用户绑定
    ClientReport = "ClientReport"

    # 脚本操作
    Script = "script"
    # 发送短信
    SMS = "sms"

    # LOGIN_MAC
    LOGIN_MAC = "login_mac"

    # area_id_change
    AREA_ID = "area_id"

    LOGIN_WIFI = "login_wifi"

    # webview统计
    JUMP_APP = "open_app"

    ERROR = "error"

    CHANNEL_CHANGE = "channel"


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