# -*- coding:utf-8 -*-
from datetime import datetime
import json
from flask import current_app, g
from sqlalchemy import and_, or_
from sharper.flaskapp.orm.display_enum import DisplayEnum
from sharper.lib.error import AppError
from sharper.util.app_util import get_package_name
import time
from sharper.util.file import get_file_fix
from bg_biz.orm.sysconfig import SysConfig

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class ConfigService(object):
    class Host(DisplayEnum):
        API = "api"
        MOBILE = "mobile"
        CARD = "card"
        PORTAL = "portal"
        REGISTER = "register"
        STATIC = "static"
        STATIC_HTTPS = "static_https"
        STATIC_CDN = 'static_cdn'
        ADMIN = 'admin'
        PAUTH = 'pauth'
        __display_cn__ = {
            API: u"api",
            MOBILE: u"移动版",
            CARD: u"充值卡",
            PORTAL: u"PORTAL页",
            REGISTER: u"注册应用",
            STATIC: u"静态资源",
            STATIC_HTTPS: u"静态资源https",
            STATIC_CDN: u"静态资源CDN",
            ADMIN: u"后台",
            PAUTH: u"认证服务器"
        }

    @classmethod
    def get_month_fee(cls, month, area_id=None):
        for month_config in cls.get_month_fee_config(area_id):
            if month == month_config.get('month'):
                return month_config.get('amount')
        raise AppError(u"")

    @classmethod
    def get_month_fee_config(cls, area_id=None):
        yingkou_area_ids = SysConfig.get_json("yingkou_area_ids")
        # 营口富士康的单价单独配置，这个等protal迁移时重构
        config_name = "month_fee_price"
        if area_id:
            if area_id in yingkou_area_ids:
                config_name = "month_fee_price_yingkou"
            else:
                area_config = SysConfig.get_json("area_config")
                area_id_str = str(area_id)
                if area_id_str in area_config and area_config.get(area_id_str) == "foxconn":
                    config_name = "month_fee_price_foxconn"
        else:
            # foxconn的单独配置
            if area_util.is_foxconn():
                config_name = "month_fee_price_foxconn"
        return SysConfig.get_json(config_name)

    @classmethod
    def get_host(cls, host):
        host_config = SysConfig.get_json("hosts")
        return host_config.get(host)

    @classmethod
    def __update_info_key__(cls, apk_info, is_preview=False):
        if apk_info['is_foxconn']:
            key = "foxconn_update_info"
        else:
            key = "hiwifi_update_info"
        if is_preview:
            key = "%s_preview" % key
        package_name = apk_info['package_name']
        if package_name.find("com.jz") != -1:
            key = "%s_old" % key
        return key

    @classmethod
    def update_app_info(cls, apk_info, content, is_preview=False):
        key = cls.__update_info_key__(apk_info, is_preview=is_preview)
        config = SysConfig.get(key)
        update_info = json.loads(config.value)

        update_info['code'] = apk_info['version_code']
        update_info['name'] = apk_info['version_name']
        update_info['time'] = int(round(time.time() * 1000))
        update_info['content'] = content
        update_info['size'] = apk_info['size']
        config.value = json.dumps(update_info)
        config.update()
        return True

    @classmethod
    def __get_info_key__(cls, is_foxconn=False, user=None, is_preview=False, is_old=False):
        '''
        针对客户端访问
        '''
        if not is_foxconn:
            is_foxconn = area_util.is_foxconn()
        if is_foxconn:
            key = "foxconn_update_info"
        else:
            key = "hiwifi_update_info"
        if is_preview:
            key = "%s_preview" % key
        elif user:
            # 灰度发布配置
            preview_config = SysConfig.get_json("grey_dist")
            if preview_config.get('active', False):
                if user.area_id and user.area_id in preview_config.get('area_ids'):
                    key = "%s_preview" % key

        # 根据包名判断是否老的包，老的包使用老的版本继续维护
        if not is_old:
            package_name = get_package_name()
            if package_name.find("com.jz") != -1:
                is_old = True
        if is_old:
            key = "%s_old" % key
        return key

    @classmethod
    def get_app_update_info(cls, is_foxconn=False, user=None, is_preview=False, is_old=False):
        key = cls.__get_info_key__(is_foxconn=is_foxconn, user=user, is_preview=is_preview, is_old=is_old)
        return SysConfig.get_json(key)

    @classmethod
    def get_wifi_score(cls, day):
        for score_config in cls.get_wifi_score_config():
            if day == score_config.get('day'):
                return score_config.get('score')
        return None

    @classmethod
    def get_wifi_score_config(cls):
        # foxconn的单独配置
        if area_util.is_foxconn():
            config_name = "wifi_score_foxconn"
        else:
            config_name = "wifi_score"
        return SysConfig.get_json(config_name)

    @classmethod
    def get_close_wifi_fee(cls, amount):
        config = sorted(filter(lambda x: int(x["amount"]) >= amount, cls.get_wifi_fee_config()), lambda x: x["amount"],
                        reverse=True)
        return config[0]["amount"] if config else None

    @classmethod
    def get_wifi_fee(cls, day, type=None,area_id=0, user=None, pay_by=False, pay_for=False, discount_info=None, with_discount=True):
        for fee_config in cls.get_wifi_fee_config(type, area_id=area_id, user=user, pay_by=pay_by, pay_for=pay_for, discount_info=discount_info, with_discount=with_discount):
            if day == fee_config.get('day'):
                return fee_config.get('amount')
        raise AppError(u"")

    @classmethod
    def get_wifi_day(cls, amount, type=None,area_id=0, user=None, pay_by=False, pay_for=False, discount_info=None,with_discount=True):
        for fee_config in cls.get_wifi_fee_config(type, area_id=area_id, user=user, pay_by=pay_by, pay_for=pay_for, discount_info=discount_info, with_discount=with_discount):
            if amount == fee_config.get('amount'):
                return fee_config.get('day')
        # raise AppError(u"")
        return 0

    @classmethod
    def get_wifi_fee_config(cls, type=None, area_id=0, user=None, pay_by=False, pay_for=False, discount_info=None,with_discount=True):
        if type == "apple":
            config = SysConfig.get_json("wifi_fee_apple")
        else:
            #特殊区域充值价格5元30天如营口区域id54
            special_wifi_fee_config = SysConfig.get_json("special_wifi_fee_config")
            special_wifi_fee_config = special_wifi_fee_config if special_wifi_fee_config else {}
            is_special = False
            if special_wifi_fee_config.has_key(str(area_id)):
                is_special = True
            #铜梁
            if area_id == 188:
                config_name = "wifi_fee_tl"
                config =  SysConfig.get_json(config_name)
            elif is_special:
                config = special_wifi_fee_config[str(area_id)]
            else:
                if type == "portal":
                    config_name = "wifi_fee_portal"
                elif type == "card":
                    config_name = "wifi_fee_card"
                else:
                    if area_util.is_foxconn():
                        config_name = "wifi_fee_foxconn"
                    else:
                        config_name = "wifi_fee"
                config =  SysConfig.get_json(config_name)
        if with_discount:
            discount_rule = DiscountRule.query.filter_by(category=DiscountRule.Category.WIFI).\
                filter(and_(or_(DiscountRule.start_time<datetime.now(),DiscountRule.start_time==None),or_(DiscountRule.end_time>datetime.now(),DiscountRule.start_time==None)))\
                .filter_by(display_type=DiscountRule.DisplayType.ALL).order_by(DiscountRule.rank).first()
            for w in config:
                if discount_rule:
                    if w["day"]==int(discount_rule.product):
                        if discount_rule.type == DiscountRule.Type.PERCENT:
                            w["amount"] = w["amount"]*(float(discount_rule.discount)/100)
                        elif discount_rule.type == DiscountRule.Type.DEL:
                            w["amount"] = w["amount"]-float(discount_rule.discount)
                        w["msg"] = discount_rule.name
                        w["discount_info"] = discount_rule.key

                if not w.has_key("discount_info") and user:
                    discount_user_rule = UserDiscountInfo.query.filter_by(user_id=user.id).filter_by(product=str(w['day'])).filter_by(category=UserDiscountInfo.Category.WIFI).\
                        filter(and_(or_(UserDiscountInfo.start_time<datetime.now(),UserDiscountInfo.start_time==None),or_(UserDiscountInfo.end_time>datetime.now(),UserDiscountInfo.start_time==None)))\
                        .filter_by(status=UserDiscountInfo.Status.NEW).order_by(UserDiscountInfo.create_time).first()
                    if discount_user_rule:
                        if discount_user_rule.type == UserDiscountInfo.Type.PERCENT:
                            w["amount"] = w["amount"]*(float(discount_user_rule.discount)/100)
                        elif discount_user_rule.type == UserDiscountInfo.Type.DEL:
                            w["amount"] = w["amount"]-float(discount_user_rule.discount)
                        w["msg"] = discount_user_rule.name
                        w["discount_info"] = discount_user_rule.key
                        w["discount_id"] = discount_user_rule.id


        return config

    @classmethod
    def get_image_url(cls, image):
        return "%s/image/%s" % (cls.get_host(cls.Host.STATIC), image) if image else None

    @classmethod
    def get_apk_url(cls, apk_path):
        return "%s/apk/%s" % (cls.get_host(cls.Host.STATIC), apk_path) if apk_path else None

    @classmethod
    def get_apk_url_https(cls, apk_path):
        return "%s/apk/%s" % (cls.get_host(cls.Host.STATIC_CDN), apk_path) if apk_path else None

    @classmethod
    def get_avatar_url(cls, avatar):
        return "%s/avatar/%s" % (cls.get_host(cls.Host.STATIC), avatar) if avatar else None


    @classmethod
    def load_photo_http_all(cls, uri):
        def get_media_handler_ext_fix_path(file_path, media_type, handler):
            ext = current_app.config['UPLOAD_HANDLER'][media_type]['handlers'][handler].get('ext')
            return get_file_fix(file_path, ext) if ext else file_path

        http_ref = "%s/photo/" % cls.get_host(cls.Host.STATIC_CDN)
        sdd = http_ref + get_media_handler_ext_fix_path(uri, 'photo', 'standard')
        thumb = http_ref + get_media_handler_ext_fix_path(uri, 'photo', 'thumb')
        dic = dict(
            big=http_ref + uri,
            standard=sdd,
            small=sdd,
            thumb=thumb,
            thumb_small=thumb
        )
        return dic['big'], dic['standard'], dic['small'], dic['thumb'], dic['thumb_small']

    @classmethod
    def get_area_by_id(cls, area_id):
        area_config = SysConfig.get_json("area_config")
        from sharper.util import area_util

        area = area_util.Area.NORMAL
        if str(area_id) in area_config:
            area = area_config.get(str(area_id))
        return area

