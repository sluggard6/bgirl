# -*- coding:utf-8 -*-
from bg_biz.orm.pic import Pic
from flask import Blueprint, request, g, session
from bg_biz.service.pic_service import pic_build
from flask_login.utils import login_required, current_user
from bg_biz.service.user_service import UserService
from bg_biz.orm.user import UserHit

__author__ = [
    'sluggrd'
]

PicView = Blueprint('pic', __name__)


@PicView.route('/list', methods=['POST', 'GET'])
def list():
    data = request.args or request.form
    print request.cookies.__str__()
    _ids = data.get('ids')
    pics = Pic.query.filter(Pic.id.in_(_ids.split(','))).all()
    ret = []
    for pic in pics:
        ret.append(pic_build(pic))
    return g.ret_success_func(pics=ret)

@PicView.route('/<int:id>', methods=['POST', 'GET'])
def one(id):
    pic = Pic.get_by_kvdb(id)
    return g.ret_success_func(pic=pic_build(pic))

@PicView.route('/<int:id>/good', methods=['POST', 'GET'])
@login_required
def good(id):
    user = current_user
    pic = Pic.get_by_kvdb(id)
    if pic:
        user_hit = UserHit.query.filter_by(user_id=user.id).filter_by(pic_id=pic.id).first()
        if not user_hit:
            user_hit = UserHit()
            user_hit.user_id = user.id
            user_hit.pic_id = pic.id
            user_hit.status = UserHit.Status.INIT
        if user_hit.status == UserHit.Status.GOOD:
            return g.ret_error_func(err=u"已经赞过了")
        elif user_hit.status == UserHit.Status.INIT:
            user_hit.status = UserHit.Status.GOOD
            pic.good += 1
            pic.update()
            UserService.add_hit(user_hit)
            return g.ret_success_func()
        else:
            return g.ret_error_func(err=(u"未知的status状态:%s" % user_hit.status))
    return g.ret_error_func(err=(u"找不到图片:%s" % id))
 