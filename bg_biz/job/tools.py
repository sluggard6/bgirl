# -*- coding:utf-8 -*-
from datetime import datetime
import json
import os
from xml.dom import minidom
from flask import current_app
from sharper.flaskapp.logger import logger
from sharper.lib.axmlparser import axmlprinter
import time
from sharper.util.sms import SmsSender
from bg_biz.job import rqueue
from bg_biz.orm.sysconfig import SysConfig
from sharper.flaskapp.orm.base import db
import re
from pyquery import PyQuery as pq
import urllib2
from random import randint
import random
from sharper.util.string import md5


__author__ = [
    '"liubo" <liubo@51domi.com>'
]


def batch_sms(phones, msg, channel=SmsSender.MEILIAN, app=None, scene=None, **kw):
    '''
    运营类短信需要指定渠道为畅天游
    '''
    rqueue.enqueue(send_sms_batch, phones, msg, channel, app=app, scene=scene, timeout=6000, **kw)


def send_sms_rq(phone, msg, need_switch=True, app=None, scene=None):
    from bg_biz.service.tool_service import ToolService

    rqueue.enqueue(ToolService.do_send_sms, phone, msg, need_switch=need_switch, app=app, scene=scene)


def send_sms_batch(phones, msg, channel, app=None, scene=None):
    from bg_biz.service.tool_service import ToolService

    if channel == SmsSender.ChangTian:
        func = ToolService.send_sms_batch_ct
    else:
        func = ToolService.send_sms_batch
    func(phones, msg, app=app, scene=scene)


def get_apk_info_rq(apk):
    rqueue.enqueue(get_apk_info, apk)


def get_apk_info(apk):
    if not apk:
        return None
    save_dir = current_app.config['UPLOAD_HANDLER']["apk"]['upload_folder']
    apk_path = "%s%s" % (save_dir, apk.link)

    apk_info = get_local_apk_info(apk_path)

    # 填充apk信息
    apk.size = apk_info.get('size', None)
    apk.package_name = apk_info.get('package_name', None)
    apk.version_code = apk_info.get('version_code', None)
    apk.version_name = apk_info.get('version_name', None)

    apk.update()


def get_local_apk_info(apk_path):
    to_dir = "/tmp/%s" % apk_path[apk_path.rfind("/") + 1:-4]
    print 'cfz-----1------',to_dir
    from bg_biz.orm.app_log import AppAction, AppLog
    # 解压app
    # AppLog.write(AppAction.AppTrack, key1="back_delete1", key2=to_dir,
    # key3=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    os.system('unzip %s -d %s >> /dev/null' % (apk_path, to_dir))
    print 'cfz-----2------',to_dir
    # 读取app manifest信息
    ap = axmlprinter.AXMLPrinter(open('%s/AndroidManifest.xml' % to_dir, 'rb').read())
    print 'cfz-----3------',ap
    buff = minidom.parseString(ap.getBuff())
    print 'cfz-----4------',buff
    ele = buff.getElementsByTagName("manifest")[0]
    print 'cfz-----5------',ele
    dic = {}
    for k, v in ele.attributes.items():
        print 'cfz-----kv------',k,v
        dic[k] = v
    ret = dict()
    # 填充apk信息
    ret['size'] = os.path.getsize(apk_path)
    ret['package_name'] = dic.get('package', None)
    ret['version_code'] = dic.get('android:versionCode', None)
    ret['version_name'] = dic.get('android:versionName', None)
    print 'cfz-----6------',ret
    # AppLog.write(AppAction.AppTrack, key1="back_delete2", key2=to_dir,
    # key3=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return ret


def write_app_log(data):
    rqueue.enqueue(write_app_log_async, data)

def write_webview_log(data):
    rqueue.enqueue(write_webview_log_async, data)

def write_third_action_log(data):
    rqueue.enqueue(write_third_action_log_async, data)


def write_app_log_async(data):
    from bg_biz.orm.app_log import AppLogNew

    log = AppLogNew()
    log.action = data.get('action')
    log.user_id = data.get('user_id')
    log.device_id = data.get('device_id')
    log.key1 = data.get('key1')
    log.key2 = data.get('key2')
    log.key3 = data.get('key3')
    log.data = data.get('data')
    log.ip = data.get('ip')
    if 'create_time' in data:
        log.create_time = data.get('create_time')
    log.insert()


def write_webview_log_async(data):
    from bg_biz.orm.webview_log import WebViewLog

    log = WebViewLog()
    log.action = data.get('action')
    log.user_id = data.get('user_id')
    log.uv_id = data.get('uv_id')
    log.blueprint = data.get('blueprint')
    log.fuc = data.get('fuc')
    log.key1 = data.get('key1')
    log.key2 = data.get('key2')
    log.key3 = data.get('key3')
    log.data = data.get('data')
    log.ip = data.get('ip')
    if 'create_time' in data:
        log.create_time = data.get('create_time')
    log.insert()


def write_third_action_log_async(data):
    from bg_biz.orm.third.third import ThirdActionLog

    log = ThirdActionLog()
    log.app_id = data.get('app_id')
    log.user_id = data.get('user_id')
    log.category = data.get('category')
    log.key1 = data.get('key1')
    log.key2 = data.get('key2')
    log.key3 = data.get('key3')
    log.ip = data.get('ip')
    if 'create_time' in data:
        log.create_time = data.get('create_time')
    log.insert()


def refresh_update_info_rq(apk_path, content, config_name='hiwifi_update_info'):
    rqueue.enqueue(refresh_update_info, apk_path, content, config_name)


def refresh_update_info(apk_path, content, config_name):
    apk_info = get_local_apk_info(apk_path)

    config = SysConfig.get(config_name)
    update_info = json.loads(config.value)

    update_info['code'] = apk_info['version_code']
    update_info['name'] = apk_info['version_name']
    update_info['time'] = int(round(time.time() * 1000))
    update_info['content'] = content
    update_info['size'] = apk_info['size']
    config.value = json.dumps(update_info)
    config.update()


def add_contents(key, book):
    rqueue.enqueue(add_read_contents, key, book)


def add_read_contents(key, book):
    file = open(key).read()
    contents = re.findall(r"#+?\d+#.*?(\d+)(.*?)\n([^#]+?)#", file)

    for c in contents:
        new_content = BookContent()
        new_content.book_id = book.id
        new_content.order_index = c[0]
        new_content.title = c[1].split(" ")[1] if len(c[1].split(" ")) > 1 else c[0]
        new_content.content = c[2]
        db.session.add(new_content)
    db.session.commit()


def make_dirs(abs_dirs):
    if not os.path.isdir(abs_dirs):
        try:
            os.makedirs(abs_dirs)
        except OSError as e:
            logger.warn(str(e))


def collect_mop():
    rqueue.enqueue(collect_mop_forum)


def collect_mop_forum():
    from bg_biz.orm.forum.forum import ForumThread
    from bg_biz.service.forum_service import ForumService
    from bg_biz.orm.user import User

    d1 = pq(url="http://3g.mop.com/mop/api/rss2.xml?id=1&qq-pf-to=pcqq.c2c",
            opener=lambda url, **kw: urllib2.urlopen(url).read())
    d2 = pq(url="http://3g.mop.com/mop/api/rss2.xml?id=2&qq-pf-to=pcqq.c2c",
            opener=lambda url, **kw: urllib2.urlopen(url).read())

    def test(index, dom, t):
        if index != 0:
            print str(pq(dom))[7:]
            inner = pq(url=str(pq(dom))[7:].replace("&amp;", "&"), opener=lambda url, **kw: urllib2.urlopen(url).read())
            title = inner(".sTit").text()
            print title
            imgs = inner(".conWidth img")
            img_clone = imgs.clone()
            timeout = False
            for i in range(len(img_clone)):
                url = pq(img_clone[i]).attr("src")
                try:
                    img = urllib2.urlopen(url, timeout=30).read()
                except Exception, e:
                    print e
                    timeout = True
                    break
                    # continue
                img_name = url.split("/")[-1]
                save_dir = current_app.config['UPLOAD_HANDLER']["image"]['upload_folder']
                random_dir = md5(str(time.time()) + str(randint(10000000, 99999999)), 8)
                random_filename = md5(str(time.time()) + str(randint(10000000, 99999999)), 16) + img_name
                abs_dir = os.path.join(save_dir, random_dir)
                make_dirs(abs_dir)
                uri = os.path.join(random_dir, random_filename)
                abs_uri = os.path.join(save_dir, uri)
                open(abs_uri, "wb").write(img)
                if imgs.eq(i).parents("a"):
                    imgs.eq(i).parents("a").attr("href", "%s/image/%s" % (current_app.config['DOWNLOAD_HOST'], uri))
                imgs.eq(i).attr("src", "%s/image/%s" % (current_app.config['DOWNLOAD_HOST'], uri))
            if not timeout:
                # user = SysConfig.get_config("forum_sys_user")
                # user = User.get_by_phone(user)
                forums = json.loads(SysConfig.get_config("forum_type_id"))
                authors = json.loads(SysConfig.get_config("forum_test_users"))
                user = random.choice(authors)
                user = User.get_by_phone(user)
                content = inner(".conWidth").html() if inner(".conWidth").html() else ""
                forum_id = forums["mop"] if t == "d2" else forums["gossip"]
                thread = ForumThread.query.filter_by(title=title).filter(ForumThread.user_id.in_(authors)).filter_by(
                    forum_id=forum_id).first()
                if not thread:
                    ForumService.add_thread(forum_id, user.id, title, content,
                                            type=ForumThread.Type.HTML)

    d1("link").each(
        lambda i, d: test(i, d, "d1")
    )
    d2("link").each(
        lambda i, d: test(i, d, "d2")
    )
