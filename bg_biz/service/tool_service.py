# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import json
from sharper.flaskapp.kvdb import kvdb
from sharper.flaskapp.orm.base import db
from bg_biz.orm.sysconfig import SysConfig
from bg_biz.orm.user import UserVcode, User
import random
from sharper.util.uploader import gen_random_path
from bg_biz.orm.app_log import SmsLog
from sharper.util.sms import send, SmsSender

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]



class ToolService(object):
    @classmethod
    def __key_sms_channel__(cls, phone):
        return "hi:t:sms:cnl:%s" % phone

    @classmethod
    def send_sms(cls, phone, msg, need_switch=True, app=None, scene=None):
        ret = send(phone, msg, SmsSender.MEILIAN)
        sms_log = SmsLog()
        sms_log.scene = scene
        sms_log.content = msg
        sms_log.phone = phone
        sms_log.status = ret
        sms_log.gateway = SmsSender.MEILIAN
        sms_log.length = msg.__len__()
        sms_log.insert()


    @classmethod
    def do_send_sms(cls, phone, msg, need_switch=True, app=None, scene=None, sender=None):
        '''
        自动添加小尾巴..【乐无限】
        need_switch, 如果不需要更换短信发送方则设置为False
        '''
        if phone.find("hi") != -1:
            phone = phone[2:]
        if not sender:
            sender = cls.__sender_list__[0]
        key = cls.__key_sms_channel__(phone)
        if kvdb.common.exists(key) and need_switch:
            last_channel = kvdb.common.get(key)
            sender = cls.sender_switch(last_channel)
        #if sender == SmsSender.ChuangLan:
        #    sender = cls.sender_switch(sender)
        if sender == SmsSender.ShuMi:
            msg = "%s 【乐无限】" % msg
        try:
            ret = send(phone, msg, sender)
        except Exception as e:
            AppLog.write(AppAction.ERROR, key1=phone, data=e, key2=sender)
            sender = cls.sender_switch(sender)
            ret = send(phone, msg, sender)
        kvdb.common.setex(key, sender, 5 * 60)

        if app:
            sms_log = SmsLog()
            sms_log.app = app
            sms_log.scene = scene
            sms_log.content = msg
            sms_log.phone = phone
            sms_log.status = ret
            sms_log.gateway = sender
            sms_log.length = msg.__len__()
            sms_log.insert()
        else:
            AppLog.write(AppAction.SMS, key1=phone, data=msg, key2=ret, key3=sender)

    #__sender_list__ = [SmsSender.ChuangLan, SmsSender.FanMeng, SmsSender.ChangTian]

    __sender_list__ = SysConfig.get_json("sms_list")
    #__sender_list__ = [SmsSender.FanMeng, SmsSender.ChangTian]
    #__sender_list__ = [SmsSender.ChuangLan, SmsSender.ChangTian]

    @classmethod
    def sender_switch(cls, last_sender):
        s_list = cls.__sender_list__
        random.shuffle(s_list)
        for i in range(0, cls.__sender_list__.__len__()):
            if last_sender == s_list[i]:
                return s_list[(i + 1) % s_list.__len__()]
            #if last_sender == "chuanglan":
            #    return cls.__sender_list__[0]
        if last_sender in cls.__sender_list__:
            return last_sender
        else:
            return cls.__sender_list__[0]

    @classmethod
    def send_sms_batch(cls, phones, msg, app=None, scene=None):
        '''
        自动添加小尾巴..【乐无限】
        need_switch, 如果不需要更换短信发送方则设置为False
        '''

        for phone in phones:
            if phone:
                cls.do_send_sms(phone, msg, app=app, scene=scene)

    @classmethod
    def send_sms_batch_ct(cls, phones, msg, app=None, scene=None):
        '''
        自动添加小尾巴..【乐无限】
        针对畅天游
        '''

        # 每次最多只能发300个手机号码
        PHONE_LIMIT = 300
        phones_array = []
        if isinstance(phones, set):
            phones = list(phones)
        while phones.__len__() > PHONE_LIMIT:
            phones_array.append(phones[0:PHONE_LIMIT])
            phones = phones[PHONE_LIMIT:]
        if phones:
            phones_array.append(phones)
        sender = SmsSender.ChangTian
        for batch_phones in phones_array:
            ret = send_batch(batch_phones, msg, sender)
            if app:
                for phone in batch_phones:
                    sms_log = SmsLog()
                    sms_log.app = app
                    sms_log.scene = scene
                    sms_log.content = msg
                    sms_log.phone = phone
                    sms_log.status = ret
                    sms_log.length = msg.__len__()
                    sms_log.gateway = sender
                    db.session.add(sms_log)
                db.session.commit()
            else:
                data = {"phones": ",".join(batch_phones), "msg": msg}
                AppLog.write(AppAction.SMS, data=json.dumps(data), key2=ret, key3=sender)

    dfa = None

    @classmethod
    def __init_dfa__(cls):
        words = SysConfig.get_json("forum_dirty_words")
        cls.dfa = Dfa(words)

    @classmethod
    def filter(cls, content):
        if not cls.dfa:
            cls.__init_dfa__()
        return cls.dfa.filter(content)


    @classmethod
    def add_pop(cls, category, title, desc, range=None, phones=None, task_id=None,
                url=None, confirm_text="确定", need_cancel=False, cancel_text="取消", promotion_id=None, obj_id=None,message_type=None
                ,keep_time=None,times=None,mobile_system=None,client_version=None,display=None,action_type=None):
        phone_strs = ",".join(phones)
        message = PopMessageBuilder.build(category, title, desc,
                                          range, phone_strs,
                                          task_id=task_id,
                                          url=url, confirm_text=confirm_text, need_cancel=need_cancel,keep_time=keep_time,
                                            times=times,
                                          cancel_text=cancel_text,message_type=message_type,action_type=action_type)
        user_ids = [User.get_by_phone(phone) for phone in phones]
        user_ids = [user.id for user in user_ids if user]
        schedule = Schedule()
        schedule.data = json.dumps(
            {
                'user_ids': user_ids,
                'category': category,
                'title': title,
                'desc': desc,
                'phones': phone_strs,
                'promotion_id': promotion_id,
                'url': url,
                'confirm_text': confirm_text,
                'need_cancel': need_cancel,
                'cancel_text': cancel_text,
                'mobile_system': mobile_system,
                'client_version': client_version,
                'display': display,
                'keep_time': keep_time,
                'times': times,
                'message_type': message_type,
                'action_type': action_type
            }
        )
        schedule.send_time = datetime.now()
        schedule.category = Schedule.Category.POP_MESSAGE
        schedule.obj_id = obj_id
        schedule.insert()


    __key_area_ip__ = "h:a:i"

    @classmethod
    def build_area_ids(cls, area_ip_rows):
        for row in area_ip_rows:
            area_id, ip = row[0], row[1]
            kvdb.common.hset(cls.__key_area_ip__, ip, area_id)

    @classmethod
    def get_area_id(cls, ip):
        area_id = kvdb.common.hget(cls.__key_area_ip__, ip)
        if area_id:
            return area_id
        return 0


    @classmethod
    def d_qrcode(cls, link, height=20,width=20):
        import qrcode
        uri, abs_uri = gen_random_path("qrcode", link)
        img = qrcode.make(link)
        img.save(abs_uri)
        return uri