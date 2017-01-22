# -*- coding:utf-8 -*-
from flask import current_app
from flask_mail import Mail, Message, Attachment
from .logger import logger


mail = Mail()


def send_mail(to_user_list=[], title=None, html=None, cc=None, sender=None, attachments=None):
    """
    发送邮件
    """
    if isinstance(to_user_list, basestring):
        to_user_list = [to_user_list]
    if cc and isinstance(cc, basestring):
        cc = [cc]
    if attachments and isinstance(attachments, Attachment):
        attachments = [attachments]
    try:
        msg = Message(
            title,
            sender=sender or current_app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=to_user_list,
            cc=cc,
            attachments=attachments
        )
        msg.html = html
        mail.send(msg)
        return True
    except Exception as ex:
        import traceback

        print traceback.format_exc()
        logger.warn(u'Send mail fail - %s' % str(ex))
        return False

