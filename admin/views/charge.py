# -*- coding:utf-8 -*-
from datetime import datetime
import urllib2
from flask import Blueprint, request, g, render_template, url_for, redirect, jsonify
from sqlalchemy import func
from bg_biz.orm.pay.charge import Charge
from bg_biz.orm.pay.transaction import Transaction
from bg_biz.orm.user import User
from bg_biz.pay.alipay import Alipay
from bg_biz.service.pay_service import PayService
from bg_biz.service.user_service import UserService
from form.charge import GiveHiCoinForm
from form.score import GiveScoreForm
from lib.decorator import pagination
from views.helper import get_phones

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]

ChargeView = Blueprint('charge', __name__)


@ChargeView.route("", methods=['GET'])
@pagination
def charge_list():
    g.status = request.args.get('status', Charge.Status.FINISHED)
    base_query = Charge.query.filter_by(status=g.status)

    charges = base_query.order_by(Charge.id.desc()).offset(
        g.real_page * g.page_size).limit(g.page_size).all()
    g.total_count = base_query.count()
    return render_template("charge/list.html", charges=charges)


@ChargeView.route("", methods=['GET'])
@pagination
def charge_statis():
    g.status = request.args.get('status', Charge.Status.FINISHED)
    base_query = Charge.query.filter_by(status=g.status)

    charges = base_query.order_by(Charge.id.desc()).offset(
        g.real_page * g.page_size).limit(g.page_size).all()
    g.total_count = base_query.count()
    return render_template("charge/list.html", charges=charges)


@ChargeView.route('/give/list', methods=['GET'])
@pagination
def give_coin_list():
    base_query = Charge.query.filter_by(category=Charge.Category.SYSTEM)
    score_logs = base_query.order_by(Charge.id.desc()).offset(
        g.real_page * g.page_size).limit(g.page_size).all()
    g.total_count = base_query.count()
    return render_template("charge/give_list.html", score_logs=score_logs)


@ChargeView.route('/give', methods=['GET'])
def give_coin():
    form = GiveHiCoinForm()
    return render_template("charge/give.html", form=form)


@ChargeView.route('/give', methods=['POST'])
def do_give():
    return redirect(url_for("charge.give_coin_list"))

    form = GiveHiCoinForm(request.form)
    coin = form.coin.data
    desc = form.descr.data
    if form.validate():
        phones = get_phones(form.phones.data)
        phone_set = set(phones)
        for phone in phone_set:
            user = User.get_by_phone(phone)
            if user:
                trans, charge = UserService.gen_charge_record(user, coin, category=Charge.Category.SYSTEM)
                UserService.charge_success(trans.id, 0, datetime.now(), '', memo=desc)
    else:
        return give_coin()
    return redirect(url_for("charge.give_coin_list"))


@ChargeView.route('/search', methods=['GET'])
@pagination
def search():
    g.charge_date = charge_date = request.args.get('charge_date', None)
    g.trans_id = trans_id = request.args.get('trans_id', None)
    print trans_id
    g.card_num = card_num = request.args.get('card_num', None)
    g.phone = phone = request.args.get('phone', None)
    if not phone and not charge_date and not trans_id and not card_num:
        transactions = []
        g.total_count = 0
    else:
        base_query = Transaction.query.join(Charge, Charge.id == Transaction.object_id).join(User,
                                                                                             User.id == Transaction.user_id). \
            filter(Transaction.object_type == Transaction.ObjectType.CHARGE)
        if charge_date:
            base_query = base_query.filter(func.date(Transaction.create_time) == charge_date)
        if phone:
            base_query = base_query.filter(User.phone == phone)
        if trans_id:
            base_query = base_query.filter(Transaction.id == int(trans_id))
        if card_num:
            base_query = base_query.filter(Transaction.memo.contains(card_num))
        transactions = base_query.order_by(Transaction.create_time.desc()).offset(
            g.real_page * g.page_size).limit(g.page_size).all()
        g.total_count = base_query.count()
    print transactions
    return render_template("charge/search.html", transactions=transactions)


@ChargeView.route('/alipay_check/<int:trans_id>', methods=['GET'])
@pagination
def alipay_check(trans_id):
    trans = Transaction.get(trans_id)
    if trans:
        info = Alipay().single_trade_check(trans)
    else:
        info = {}
    print info
    return render_template("charge/alipay_check_info.html", info=info)


@ChargeView.route('/callback/<int:trans_id>', methods=['GET', 'POST'])
@pagination
def pay_callback(trans_id):
    # trans_id = 1100733184
    trans = Transaction.get(trans_id)
    if trans:
        channel = trans.pay_type
        channel_num = channel.find('ios_')
        if channel_num >= 0:
            channel = channel[4:]
        if channel in [Transaction.PayType.ALIPAY_DIRECT, Transaction.PayType.ALIPAY_WAP,Transaction.PayType.ALIPAY_APP]:
            info = Alipay().single_trade_check(trans)
        elif channel in [Transaction.PayType.YEEPAY_CARD, Transaction.PayType.YEEPAY_DEPOSIT]:
            from luhu_biz.pay.yeepay import MerchantAPI
            api = MerchantAPI()
            info = {}
            # url = api.create_pay_single_check_url(trans_id=trans_id)
            # date_str = datetime(trans.create_time.year, trans.create_time.year.month, trans.create_time.year.day).strftime("%Y-%m-%d")
            date_str = datetime(datetime.now().year, datetime.now().month, 15).strftime("%Y-%m-%d")
            url = api.create_clear_data_url(date_str, date_str)
            lines = urllib2.urlopen(url).read()
            for line in lines.split("\n"):
                # print line.find("YB01000001694"), line
                if line.find("YB01000001694") == 0:
                    infos = line.split(",")
                    trans_s_id = int(infos[4])
                    if str(trans_s_id) == str(trans_id):
                        print trans_id
                        info = {"id": trans_id}
        elif channel in [Transaction.PayType.APPLE_PAY]:
            from luhu_biz.pay.applepay import ApplePay
            info = ApplePay.admin_check_pay_result(trans)
        elif channel in [Transaction.PayType.WEIXIN_PAY]:
            from luhu_biz.pay.weixinpay import WXpay
            info = WXpay.queryOrderTest(trans)
        elif channel in [Transaction.PayType.WEIXIN_PAY_FOXCONN]:
            from luhu_biz.pay.weixinpay import WXpay
            info = WXpay.queryOrderTest(trans,'foxconn')
        else:
            info = {}

    else:
        info = {}
    if info:
        print 'admin charge--info --',info
        PayService.get_callback(trans).execute(trans)
    return jsonify(success=True)


@ChargeView.route('/check_vip', methods=['GET', 'POST'])
def check_vip():
    phone = request.args.get('phone', None)
    import datetime
    charge_date = datetime.date.today() - datetime.timedelta(days=60)
    print charge_date
    if phone:
        from luhu_sharper.flaskapp.orm.base import db
        user_sql = '''SELECT id from user where date(last_login_time) >= '%s' AND phone = '%s';''' % (
            charge_date, phone)
        print user_sql
        user_row = db.engine.execute(user_sql)
        for row in user_row:
            sql = '''SELECT sum(transaction.amount) FROM transaction WHERE status = 'finished' AND user_id = '%s';''' % (
                row[0])
            print sql
            amount = db.engine.scalar(sql)
            print amount
            if amount >= 10000:
                return jsonify(success=True)
    return jsonify(success=False)
