# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, g, request, flash, redirect, url_for
from bg_biz.orm.admin import AdminLog, AdminUser
from form.admin import ModifyPasswordForm
from sharper.flaskapp.kvdb import kvdb

__author__ = [
    'John Chan'
]

DefaultView = Blueprint('default', __name__)


@DefaultView.route('/home', methods=['GET'])
def home():
    logs = AdminLog.query.filter_by(user_id=g.me.id).order_by(AdminLog.id.desc()).limit(20).all()
    return render_template('home.html', logs=logs)


@DefaultView.route('/favicon.ico', methods=['GET'])
def favicon():
    return redirect(url_for("default.home"))


@DefaultView.route('/modify_password', methods=['GET'])
def modify_password():
    form = ModifyPasswordForm()
    return render_template('admin/modify_password.html', form=form)


@DefaultView.route('/modify_password', methods=['POST'])
def do_modify_password():
    form = ModifyPasswordForm(request.form)
    if form.validate():
        admin_user = g.me
        if not admin_user.check_password(form.old_password.data):
            flash(u"旧密码错误，请确认", "warn")
            return render_template('admin/modify_password.html', form=form)
        if form.new_password.data != form.repeat_password.data:
            flash(u"两次密码输入不一致，请确认", "warn")
            return render_template('admin/modify_password.html', form=form)
        admin_user.gen_password(form.new_password.data)
        admin_user.update()
        flash(u"密码修改成功", "ok")
        return render_template('admin/modify_password.html', form=form)
    else:
        return render_template('admin/modify_password.html', form=form)


@DefaultView.route('/log_ip', methods=['GET', 'POST'])
def log_ip():
    ip = "abcdefg"
    kvdb.common.setex('ip', ip, 10000000)
    return ip


@DefaultView.route('/project-manager/', methods=['GET', 'POST'])
@DefaultView.route('/project-manager', methods=['GET', 'POST'])
def empty_page_for_qq_validate():
    return render_template("/qq_validate.html")


@DefaultView.route('/project-manager/user/qq-login-callback', methods=['GET', 'POST'])
def qq_login_callback():
    return render_template("/qq_callback.html")