# -*- coding:utf-8 -*-

from flask import Blueprint,jsonify,request,g
from bg_biz.service.pay_service import PayService
from bg_biz.orm.pay.transaction import Transaction
from bg_biz.orm.pay.charge import Charge
from flask_login import login_required
from flask_login.utils import current_user

__author__ = [
    'John Chan'
]

ChargeView = Blueprint('charge', __name__)

@ChargeView.route('/do', methods=['GET'])
@login_required
def do_pay():
    pay_type = request.args.get('pay_type')
    title = u'充值VIP'
    detail = u'昧昧充值'
    amount = 1
    callback = ''
    charge = Charge()
    charge.user_id = current_user.id
    charge.phone = current_user.phone
    charge.amount = amount
    charge.status = 1
    charge.paid = amount
    charge.category = Charge.Category.WIFI
    charge.source = Charge.Source.WIFI
    charge.day = 365
    charge.insert()

    object_type = Transaction.ObjectType.CHARGE
    if pay_type == Transaction.PayType.ALIPAY_APP:
        url,trans = PayService.create_pay_url_new(pay_type,amount,title,detail,charge.id,callback,object_type,charge.user_id)
        print url
        return g.ret_success_func(url=url)

    if pay_type == "weixin_pay":
        #channel+pay_type
        url, trans = PayService.create_pay_url_new(pay_type, amount, title, detail,charge_id, callback,
                                               object_type, user_id=user_id)
        return g.ret_success_func(wxdata=url)
    return jsonify(success=False)