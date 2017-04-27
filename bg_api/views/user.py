# -*- coding:utf-8 -*-
import traceback

from bg_biz.orm.user import User, UserVcode, UserHit
from flask_login import login_required
from flask_login import login_user
from bg_biz.service.user_service import UserService, validate_vcode
from sharper.flaskapp.orm.base import transaction
from sharper.lib.validator import paras_dict_validate, is_mobile
from sharper.util.transfer import dict2vars

from flask import Blueprint, request, g, session
from flask.json import jsonify
from flask_login.utils import current_user

__author__ = [
    'sluggard'
]

UserView = Blueprint('user', __name__)


@UserView.route('/login', methods=['POST', 'GET'])
def login():
    data = request.args or request.form

    phone, passwd = dict2vars(data, ('uname', 'pwd'))

    try:
        if not User.get_by_phone(phone):
            return g.ret_error_func(u'该手机号码未注册')
        user = User.login(phone, passwd)
    except Exception as e:
        traceback.print_exc()
        myuser = User()
        myuser.clear_unique_kvdb("phone", phone)
        return g.ret_error_func(u"手机号码或者密码错误，请确认")
    login_user(user)
    session['user_hits'] = set(UserHit.query.filter_by(user_id=user.id).all())
    return g.ret_success_func(msg=session.sid)

@UserView.route('/logined', methods=['POST', 'GET'])
@login_required
def logined():
    data = request.args or request.form
    user = current_user
    print user
    return g.ret_success_func();

@UserView.route('/register', methods=['GET', 'POST'])
@transaction
def register():
    if request.method == "GET":
        data = request.args
    elif request.method == "POST":
        data = request.form
    version = int(data.get("version", 1))
    paras_dict_validate(
        data, [
            ('pwd', 'required, length', {'min': 5, 'max': 20}, u'密码至少5-20位字符，支持大小写，数字，下划线'),
            ('uname', 'required, mobile', None, u'该手机号码无效！')
        ]
    )
    phone, password = dict2vars(data, ('uname', 'pwd'))
#     verified = int(data.get('verified', 0))
    # 如果手机号码是直接读取的，则不用验证
#     if not verified:
    vcode = data.get('key', None)
    if not vcode:
        return g.ret_error_func(u'请输入验证码')
    if not validate_vcode(phone, vcode, UserVcode.Category.REGISTER):
        return g.ret_error_func(u'验证码无效，请确认')
    if User.get_by_phone(phone):
        return g.ret_error_func(u'该手机号码已经被注册！')

    user = UserService.register(phone, password)
    print user
    login_user(user)
    return g.ret_success_func(seid=session.sid)

@UserView.route('/forgotPass', methods=['GET', 'POST'])
@transaction
def forgotPass():
    """
    修改密码
    """
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args
    paras_dict_validate(
        data, [
            ('key', 'required', None, u'请输入验证码'),
            ('uname', 'required', None, u'请输入手机号码'),
            ('pwd', 'required, length', {'min': 5, 'max': 20}, u'密码至少5-20位字符，支持大小写，数字，下划线'),
        ]
    )

    vcode, phone, new_password = dict2vars(data, ('key', 'uname', 'pwd'))

    if not validate_vcode(phone, vcode, UserVcode.Category.FORGET_PASS):
        return g.ret_error_func(u'验证码无效，请返回上一步')

    user = User.get_by_phone(phone)
    user.set_password(new_password)
    user.update()

    return g.ret_success_func()

@UserView.route('/checkPhone', methods=['GET', 'POST'])
def checkPhone():
    data = request.args or request.form
    phonenum = data.get("phone", None)
    if not phonenum:
        return jsonify(success=False, message=u'未指定验证手机号码')
    if not is_mobile(phonenum):
        return jsonify(success=False, message=u"请输入正确的手机号码")
    user = User.get_by_phone(phonenum)
    if user:
        return jsonify(success=False, message=u"该手机号码已经被注册",msgcode=1)
    return jsonify(success=True, message=u"可以注册的手机号码")


@UserView.route('/hasUser', methods=['GET', 'POST'])
def hasUser():
    data = request.args or request.form
    phonenum = data.get("phone", None)
    if not phonenum:
        return jsonify(success=False, message=u'未指定验证手机号码')
    if not is_mobile(phonenum):
        return jsonify(success=False, message=u"请输入正确的手机号码")
    user = User.get_by_phone(phonenum)
    if not user:
        return jsonify(success=False, message=u"手机号码不存在",msgcode=1)
    return jsonify(success=True, message=u"成功")

@UserView.route('/profile')
@login_required
def profile():
    u = current_user
    ret = dict()
    ret['id'] = u.id
    ret['phone'] = u.phone
    ret['status'] = u.status
    ret['nick'] = u.nick
    ret['balance'] = u.balance
    ret['score'] = u.score
    ret['realname'] = u.realname
    ret['vipend'] = u.vipend_time
    return g.ret_success_func(user=ret)
    
@UserView.route('/user_hit')
@login_required
def user_hit():
    u = current_user
    hits = UserHit.query.filter_by(user_id=u.id).all()
    return g.ret_success_func(hits=UserService.build_user_hit(hits))
    
    
    
    