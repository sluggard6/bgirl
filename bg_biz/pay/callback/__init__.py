# -*- coding:utf-8 -*-
import traceback
from sharper.flaskapp.logger import logger
from sharper.flaskapp.mail import send_mail
from sharper.flaskapp.orm.base import db
from bg_biz.orm.pay.transaction import Transaction

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class Executor(object):
    def __init__(self):
        pass

    def execute(self, trans):
        self.trans = trans
        #flush_method = db.session.flush
        #commit_method = db.session.commit
        db.engine.execute("set autocommit=0")
        db.session.begin(subtransactions=True)
        try:
            if trans.status == Transaction.Status.FINISHED:
                return
            logger.error("====================begin deal transaction: %s===============\n" % trans.id)

            #db.session.commit = flush_method
            if trans.object_type == Transaction.ObjectType.CHARGE:
                ret = self.execute_internal(trans.object_id,trans=trans)
            else:
                ret = self.execute_internal(trans.object_id)
            print ret
            if not ret:
                to_user_list = ['chenfazhun@hi-wifi.cn']
                title = u"支付处理异常-%s" % trans.id
                try:
                    send_mail(to_user_list, title, u"")
                except Exception as e:
                    logger(e)

            trans.status = Transaction.Status.FINISHED
            logger.error("====================end deal transaction: %s===============\n" % trans.id)
            db.session.merge(trans)
            #db.session.commit = commit_method
            db.session.commit()
        except Exception as e:
            #db.session.commit = commit_method
            logger.error(e)
            logger.error(traceback.format_exc())
            db.session.rollback()
            #db.session.transaction.close()
            db.engine.execute("set autocommit=1")
            db.session.begin(subtransactions=True)
            trans.status = Transaction.Status.ERROR
            if trans.memo:
                trans.memo += "\n %s \n" % e.message
            else:
                trans.memo = "\n %s \n" % e.message
            db.session.merge(trans)
            db.session.commit()
            raise e
        finally:
            db.engine.execute("set autocommit=1")

    def execute_internal(self, obj_id,trans=None):
        __doc__ = '''执行具体的逻辑'''
        pass
