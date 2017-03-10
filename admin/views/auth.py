# -*- coding:utf-8 -*-
from flask import Blueprint, current_app, session, request, redirect, render_template, g, jsonify
from form import LoginForm

from bg_biz.orm.admin import AdminUser
from sharper.flaskapp.helper import clear_cookie
from sharper.util import string

__author__ = [
    '"liubo" <liubo@51domi.com>'
]

AuthView = Blueprint('auth', __name__)

AUTO_LOGIN_COOKIE_NAME = "auto_login_gm"


def get_auto_login_token(cuser):
    return str(cuser.id) + '_' + string.md5(str(cuser.id) + cuser.password)


def login_session(cuser):
    session['user_id'] = cuser.id
    session['user_name'] = cuser.user_name

    g.is_login = True


def write_auto_login(cuser, response):
    response.set_cookie(AUTO_LOGIN_COOKIE_NAME, value=get_auto_login_token(cuser), max_age=3600 * 24 * 7)
    return response


@AuthView.route('/logout', methods=['GET'])
def logout():
    """
    logout page
    """
    return_url = session.get('return_url',None)
    session.clear()
    session['return_url'] = return_url
    return clear_cookie(redirect('/'), AUTO_LOGIN_COOKIE_NAME)

@AuthView.route('/can_logout',methods=['POST','GET'])
def can_logout():
    admin_uname = None
    if request.method == 'POST':
        admin_uname = request.form.get('uname', None)
    if request.method == 'GET':
        admin_uname = request.args.get('uname', None)
    return jsonify(success=False)


def login_ok(cusr, is_auto_login=True, return_url=None):
    """
    登录成功-设定用户登录状态及跳转
    """
    login_session(cusr)

    rurl = session.pop('return_url', None)
    #if return_url:
    #    rurl = return_url+'?sid='+request.cookies.get(current_app.session_cookie_name)
    if rurl:
        response = current_app.make_response(redirect(rurl))
    else:
        response = current_app.make_response(redirect('/home'))

    if is_auto_login:
        response = write_auto_login(cusr, response)
    return response


@AuthView.route("/", methods=['GET', 'POST'])
def index():
    print request.method
    if request.method == 'GET':
        if 'user_id' in session:
            #if return_url:
            #    return redirect(return_url)
            return redirect('/home')
        else:
            token = request.cookies.get(AUTO_LOGIN_COOKIE_NAME)
            if token:
                user_id, hs = token.split('_')
                u = AdminUser.get(int(user_id))
                if u and token == get_auto_login_token(u):
                    login_session(u)
                    #if return_url:
                    #    return redirect(return_url)
                    return redirect('/home')
                else:
                    return redirect('/logout')

    form = LoginForm()
    #if return_url:
    #    form.return_url.data = return_url
    if request.method == 'POST':
        if form.validate_on_submit():
            print 'submit :'
            #return login_ok(form.user, form.remembered, form.return_url.data)
            return login_ok(form.user, form.remembered, None)

    return render_template("index.html", form=form)

