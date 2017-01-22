# -*- coding:utf-8 -*-
"""系统功能视图"""
from flask.blueprints import Blueprint

DefaultView = Blueprint('default', __name__)


def error_handler(e):
	"""
	debug关闭后统一错误处理
	"""
	if isinstance(e, AuthFailedError):
		return json_error(e, 401)
	elif isinstance(e, AppError):
		return helper.render_json_warn(e, request)
	else:
		return helper.render_json_error(e, request)


@DefaultView.route('/', methods=['GET'])
def default():
	return g.ret_success_func(flask='flask ' + flask.__version__)


