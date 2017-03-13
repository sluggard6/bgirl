# -*- coding:utf-8 -*-

from flask_login import LoginManager


login_manager = LoginManager()

@login_manager.user_loader
def load_user(userid):
    from bg_biz.orm.user import User
    return User.get(userid)



def init_login(app):

    login_manager.init_app(app)