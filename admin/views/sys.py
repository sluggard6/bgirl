# -*- coding:utf-8 -*-
import json
import os
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app, url_for, redirect, flash, g
from bg_biz.job.tools import refresh_update_info_rq
from bg_biz.orm.sysconfig import SysConfig
from bg_biz.service.config_service import ConfigService
from sharper.util import apk_util
from form import obj2form, form2obj
from form.sys_config import SysConfigForm
from lib.upload import upload_local

__author__ = [
    '"liubo" <liubo@51domi.com>'
]
SysView = Blueprint('sys', __name__)

PAGE_SIZE = 20


@SysView.route('/configs', methods=['GET'])
def show_sys_config():
    return render_template("sys/configs.html", configs=SysConfig.query.all())


@SysView.route('/lottery', methods=['GET'])
def lottery():
    return render_template("lottery.html")


@SysView.route('/config/edit', methods=['GET'])
@SysView.route('/config/edit/<string:key>', methods=['GET'])
def show_config(key=None):
    form = SysConfigForm()
    if key:
        config = SysConfig.get(key)
        if config:
            obj2form(config, form)
            """if form.name.data == "forum_dirty_words":
                new_value = json.loads(form.value.data)
                print form.value.data
                new_value = [x for x in new_value if x!="日" and x!="干"]
                print new_value
                form.value.data = json.dumps(new_value)"""
    return render_template("sys/edit_config.html", form=form)


@SysView.route('/config/edit', methods=['POST'])
@SysView.route('/config/edit/<string:key>', methods=['POST'])
def update_config(key=None):
    form = SysConfigForm(request.form)
    config = None
    if key:
        config = SysConfig.get(key)

    if not config:
        config = SysConfig()
        form2obj(form, config)
        config.insert()
    else:
        form2obj(form, config)
        config.update()
    return render_template("success.html")


@SysView.route('/config/refresh_config_cache', methods=['POST'])
def refresh_config_cache():
    SysConfig.refresh_kvdb()
    return jsonify(success=True)


@SysView.route('/restart', methods=['GET'])
def restart():
    import commands

    r = commands.getstatusoutput('touch /var/tmp/uwsgi/reload.uwsgi')
    r = u'重启成功' if int(r[0]) == 0 else u'重启失败'
    return render_template('sys/restart.html', msg=r)


@SysView.route("/upload_hiwifi_apk", methods=['POST'])
def upload_hiwifi_apk():
    f = request.files['file_uploader']

    # 保存临时文件
    temp_file = "%s.apk" % uuid.uuid4().hex
    apk_path = "%s%s" % (current_app.config['UPLOAD_HANDLER']['apk']['upload_folder'], temp_file)
    f.save(apk_path)
    apk_info = apk_util.get_local_apk_info(apk_path)
    is_foxconn = False
    if apk_info['version_name'].find('foxconn') != -1:
        is_foxconn = True
    if apk_info.get("package_name", "").find("com.jz") != -1:
        is_old = True
    else:
        is_old = False
    apk_info['is_foxconn'] = is_foxconn
    apk_info['path'] = apk_path
    apk_info['file'] = temp_file
    info = "%s版本  code：%s  版本号:%s  包名：%s" % ('富士康' if is_foxconn else u'普通',
                                             apk_info['version_code'], apk_info['version_name'],
                                             apk_info['package_name'])
    is_preview = request.args.get("preview", False)
    if is_preview:
        is_preview = True
    update_info = ConfigService.get_app_update_info(is_foxconn=is_foxconn, is_preview=is_preview, is_old=is_old)

    online_info = "%s版本  code：%s  版本号:%s " % ('富士康' if is_foxconn else u'普通',
                                              update_info['code'],
                                              update_info['name'])

    return jsonify(url=apk_path, info=info, apk_info=json.dumps(apk_info), online_info=online_info,
                   uri='', fileType="apk", original=f.filename, success=True,
                   state="SUCCESS")


@SysView.route("/upload_preview_apk", methods=['GET'])
def upload_preview_apk():
    g.preview = True
    return render_template("sys/upload_apk.html")


@SysView.route("/upload_apk", methods=['GET'])
def upload_apk():
    g.preview = False
    return render_template("sys/upload_apk.html")


@SysView.route("/upload_apk", methods=['POST'])
def do_upload_preview_apk():
    apk_info = json.loads(request.form.get('apk_info'))

    if apk_info['is_foxconn']:
        is_foxconn = True
    else:
        is_foxconn = False

    if apk_info.get("package_name", "").find("com.jz") != -1:
        is_old = True
    else:
        is_old = False
    update_info = ConfigService.get_app_update_info(is_foxconn=is_foxconn, is_preview=False, is_old=is_old)
    version = update_info.get('name')
    file_path = update_info.get('path')
    file_name = file_path[file_path.rfind("/") + 1:]

    # 备份老的文件
    apk_path = "%s%s.apk" % (current_app.config['UPLOAD_HANDLER']['apk']['upload_folder'], file_name[:-4])
    back_file = "%shiwifi_back/%s%s.apk" % (
        current_app.config['UPLOAD_HANDLER']['apk']['upload_folder'], file_name[:-3], version)
    os.system('cp  %s %s' % (apk_path, back_file))

    # 修改更新信息
    content = request.form.get('content', None).replace("\r\n", "\n")

    ConfigService.update_app_info(apk_info, content, is_preview=False)

    # 覆盖新文件
    os.system('mv %s %s' % (apk_info['path'], apk_path))

    return render_template("success.html")


@SysView.route("/upload_preview_apk", methods=['POST'])
def do_upload_apk():
    apk_info = json.loads(request.form.get('apk_info'))
    if apk_info['is_foxconn']:
        is_foxconn = True
    else:
        is_foxconn = False
    update_info = ConfigService.get_app_update_info(is_foxconn=is_foxconn, is_preview=True)
    version = update_info.get('name')
    file_path = update_info.get('path')
    file_name = file_path[file_path.rfind("/") + 1:]

    # 备份老的文件
    apk_path = "%s%s.apk" % (current_app.config['UPLOAD_HANDLER']['apk']['upload_folder'], file_name[:-4])
    back_file = "%shiwifi_preview_back/%s%s.apk" % (
        current_app.config['UPLOAD_HANDLER']['apk']['upload_folder'], file_name[:-3], version)
    os.system('cp  %s %s' % (apk_path, back_file))

    # 修改更新信息
    content = request.form.get('content', None).replace("\r\n", "\n")

    ConfigService.update_app_info(apk_info, content, is_preview=True)

    # 覆盖新文件
    os.system('mv %s %s' % (apk_info['path'], apk_path))

    return render_template("success.html")


@SysView.route('/user_sign', methods=['GET', "POST"])
def user_sign():
    if request.method == "GET":
        config = SysConfig.query.filter_by(name="user_sign").first()
        config = json.loads(config.value)
        add_date = config["add_date"].split(";") if config["add_date"] else []
        sign_score = config["sign_score"].split(";") if config["sign_score"] else []
        return render_template("user_sign.html", add_date=add_date, sign_score=sign_score)
    else:
        config = SysConfig.query.filter_by(name="user_sign").first()
        config.value = request.form.get("value", "")
        config.update()
        return "OK"

@SysView.route('/ad_refresh', methods=['GET', "POST"])
def ad_refresh():
    if request.method == "GET":
        config = SysConfig.query.filter_by(name="app").first()

        config = json.loads(config.value)
        refresh_time = config['ad_refresh_time'] if config['ad_refresh_time'] else ''


        return render_template("ad_refresh.html", refresh_time=refresh_time)
    else:
        config = SysConfig.query.filter_by(name="app").first()
        confign = json.loads(config.value)
        confign['ad_refresh_time'] = request.form.get("refresh_time", "300")
        config.value=json.dumps(confign)
        print config
        config.update()
        return "OK"

