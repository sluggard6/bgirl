# -*- coding:utf-8 -*-
"""
自定义wtf表单元素
"""
from flask import current_app, request, session
from flask.views import View
from wtforms import Field, ValidationError
from wtforms.widgets import HTMLString, html_params

__author__ = [
    '"linnchord" <linnchord@gmail.com>'
]

DEFAULT_RECAPTCHA_URL = '/recaptcha'


class RecaptchaWidget(object):
    """
    验证码呈现
    """
    def __call__(self, field, error=None, **kwargs):
        RECAPTCHA_HTML = u'''<input type="text" placeholder="%(debug)s" %(html_params)s/> <img class="captcha" title="点击换一个新的验证码" src="%(code_img_url)s" onclick="refreshCaptcha()" /> <a href="javascript:refreshCaptcha()"  class="recaptcha_ctrl">看不清</a>'''

        return HTMLString(RECAPTCHA_HTML % dict(
            html_params=html_params(name=field.name, id=field.name, **kwargs),
            code_img_url=current_app.config.get('RECAPTCHA_IMG_URL', DEFAULT_RECAPTCHA_URL),
            debug='DEBUG' if current_app.config.get('RECAPTCHA_DEBUG') or current_app.testing else ''
        ))


class RecaptchaValidate(object):
    """验证码验证方式"""
    def __init__(self, message=u'图片验证码错误，请再尝试。'):
        self.message = message

    def __call__(self, form, field):
        challenge = request.form.get('recaptcha_code')

        if not self._validate_recaptcha(challenge):
            raise ValidationError(self.message)

    def _validate_recaptcha(self, challenge):
        if current_app.testing or current_app.config.get('RECAPTCHA_DEBUG'):
            return True

        if challenge.lower() == session.get('recaptcha_code').lower():
            session.pop('recaptcha_code')
            return True

        return False


class RecaptchaField(Field):
    """
    验证码字段
    """
    widget = RecaptchaWidget()

    recaptcha_error = None

    def __init__(self, label='', validators=None, **kwargs):
        validators = validators or [RecaptchaValidate()]
        super(RecaptchaField, self).__init__(label, validators, **kwargs)


class RecaptchaView(View):
    """
    图片验证码视图
    """
    def dispatch_request(self):
        try:
            import cStringIO as StringIO
        except ImportError:
            import StringIO

        mstream = StringIO.StringIO()

        from sharper.util import vcode
        img, code = vcode.create_validate_code()
        session['recaptcha_code'] = code
        img.save(mstream, "GIF")

        return current_app.response_class(mstream.getvalue(), mimetype='image/gif')


def init_recaptcha(app):
    """
    初始化验证码图片服务
    """
    app.add_url_rule(app.config.get('RECAPTCHA_IMG_URL', DEFAULT_RECAPTCHA_URL),
                     view_func=RecaptchaView.as_view('recaptcha'))