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
    return hit(id,UserHit.Status.GOOD, 1)
    
@PicView.route('/<int:id>/ungood', methods=['POST', 'GET'])
@login_required
def ungood(id):
    return hit(id,UserHit.Status.GOOD, 0)
        
@PicView.route('/<int:id>/bad', methods=['POST', 'GET'])
@login_required
def bad(id):
    return hit(id,UserHit.Status.BAD, 1)

@PicView.route('/<int:id>/unbad', methods=['POST', 'GET'])
@login_required
def unbad(id):
    return hit(id,UserHit.Status.BAD, 0)
        
def hit(id, status, action):
    print id, status, action
    user = current_user
    pic = Pic.get_by_kvdb(id)
#     user_hit = 
    if pic:
        user_hit = UserHit.query.filter_by(user_id=user.id).filter_by(pic_id=pic.id).first()
        print user_hit
        if not user_hit:
            user_hit = UserHit()
            user_hit.user_id = user.id
            user_hit.pic_id = pic.id
            user_hit.status = UserHit.Status.INIT
        if action == 1:
            if status == UserHit.Status.GOOD:
                if user_hit.status == UserHit.Status.GOOD:
                    return g.ret_error_func(err=u"已经赞过了")
                elif user_hit.status == UserHit.Status.BAD:
                    pic.good += 1
                    pic.bad -= 1
                elif user_hit.status == UserHit.Status.INIT:
                    pic.good += 1
                else:
                    return g.ret_success_func()
            elif status == UserHit.Status.BAD:
                if user_hit.status == UserHit.Status.BAD:
                    return g.ret_error_func(err=u"已经踩过了")
                elif user_hit.status == UserHit.Status.GOOD:
                    pic.good -= 1
                    pic.bad += 1
                elif user_hit.status == UserHit.Status.INIT:
                    pic.bad += 1
                else:
                    return g.ret_success_func()
            else:
                raise AppError(u'不支持的状态')
            user_hit.status = status
        elif action == 0:
            if status == UserHit.Status.GOOD and user_hit.status == UserHit.Status.GOOD:
                pic.good -= 1
            elif status == UserHit.Status.BAD and user_hit.status == UserHit.Status.BAD:
                pic.bad -= 1
            else:
                return g.ret_success_func()
            user_hit.status = UserHit.Status.INIT
        else:
            raise AppError(u'不支持的状态')
        pic.update()
        
        UserService.add_hit(user_hit)
        return g.ret_success_func()
    return g.ret_error_func()