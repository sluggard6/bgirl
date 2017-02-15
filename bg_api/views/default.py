# -*- coding:utf-8 -*-
"""系统功能视图"""
import flask

from flask import Blueprint, g, request, current_app

from sharper.flaskapp.helper import json_error, json_ok, render_json_warn, render_json_error
from sharper.lib.error import AuthFailedError, AppError

DefaultView = Blueprint('default', __name__)


def error_handler(e):
	"""
	debug关闭后统一错误处理
	"""
	if isinstance(e, AuthFailedError):
		return json_error(e, 401)
	elif isinstance(e, AppError):
		return render_json_warn(e, request)
	else:
		return render_json_error(e, request)


@DefaultView.route('/', methods=['GET'])
def default():
	g.ret_success_func = json_ok
	return g.ret_success_func(flask='flask ' + flask.__version__)


@DefaultView.route('/profile', methods=['GET'])
def profile():
	ret = dict()
	ret['host'] = current_app.config.get("HTTP_DOMAIN");
	ret['port'] = current_app.config.get("PORT");
	return g.ret_success_func(profile=ret)
