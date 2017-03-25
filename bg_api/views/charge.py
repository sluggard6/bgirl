# -*- coding:utf-8 -*-

from flask import Blueprint,jsonify,request,g
from bg_biz.service.pay_service import PayService
from bg_biz.orm.pay.transaction import Transaction

__author__ = [
    'John Chan'
]

ChargeView = Blueprint('charge', __name__)

@ChargeView.route('/do', methods=['GET'])
def do_pay():
    pay_type = request.args.get('pay_type')
    title = u'支付宝充值'
    detail = u'昧昧充值'
    amount = 1
    charge_id = 1
    callback = ''
    object_type = Transaction.ObjectType.CHARGE
    user_id = 1
    if pay_type == Transaction.PayType.ALIPAY_APP:
        url = PayService.create_pay_url(pay_type,amount,title,detail,charge_id,callback,object_type,user_id)
        print url
        return g.ret_success_func(url=url)

    if pay_type == "weixin_pay":
        #channel+pay_type
        url, trans = PayService.create_pay_url_new(pay_type, amount, title, detail,charge_id, callback,
                                               object_type, user_id=user_id)
        return g.ret_success_func(wxdata=url)
    return jsonify(success=False)