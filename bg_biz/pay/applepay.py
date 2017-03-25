# -*- coding:utf-8 -*-
import json
import urllib2
import datetime,time
from bg_biz.orm.sysconfig import SysConfig
#from bg_biz.orm.user import UserScoreLogLock
from bg_biz.pay.callback.charge import ChargeExecutor
from bg_biz.orm.pay.transaction import Transaction
import os

__author__ = [
    '"John Chan" <chenfazhun@163.com>'
]




url = 'https://buy.itunes.apple.com/verifyReceipt'
test_url = "https://sandbox.itunes.apple.com/verifyReceipt"


class ApplePay(object):

    def __init__(self):
        pass

    @classmethod
    def check_pay_result(self, trans, receipt_data, out_serial_no):
        #print '----------applepay-biz-receipt_data----------',receipt_data
        params = json.dumps({'receipt-data': receipt_data})
        conn = urllib2.Request(url=url, data=params)
        res_data = urllib2.urlopen(conn)
        res = res_data.read()
        json_res = json.loads(res)
        #print '-----------applepay-biz-json_res---------------------',json_res
        status = json_res.get('status')
        #print '----------applepay-biz-status-----------',status
        if int(status) == 21007:
            print '---------applepay-biz-sandbox-------------------'
            conn = urllib2.Request(url=test_url, data=params)
            res_data = urllib2.urlopen(conn)
            res = res_data.read()
            json_res = json.loads(res)

        receipt = json_res.get('receipt')
        print '---------applepay-biz-receipt-------------------',receipt
        in_app = receipt.get('in_app')
        print '---------applepay-biz-in_app-------------------',in_app
        in_app_array = sorted(in_app, key=lambda x: x['original_purchase_date_ms'], reverse=True)
        for app in in_app_array:
            original_purchase_date_ms = app.get('original_purchase_date_ms')
            print 'original_purchase_date_ms=', original_purchase_date_ms
            if (time.time()-int(original_purchase_date_ms)/1000)/86400 > 7:
                return False
            product_id = app.get('product_id')
            transaction_id = app.get('transaction_id')
            #print '---------applepay-biz-transaction_id------------------',transaction_id,'--------applepay-biz-product_id-------------',product_id
            if product_id == out_serial_no:
                config = SysConfig.get_json("apple_pay_list")
                amount = config.get(out_serial_no)

                print '=applepay-biz=', amount, '-applepay-biz-', trans.amount

                if trans.amount == amount:
                    print 'trans.end=',transaction_id
                    import hashlib
                    m = hashlib.md5()
                    m.update(transaction_id)
                    score_log_lock = UserScoreLogLock()
                    score_log_lock.sign = m.hexdigest()
                    #print 'applepay-biz ------------- trans.end=', score_log_lock.sign
                    try:
                        score_log_lock.insert()
                    except Exception as e:
                        print 'e==', e
                        continue
                    trans.out_serial_no = transaction_id
                    ChargeExecutor().execute(trans)
                    print '----applepay-biz-----charge-------success-----------4'
                    return True
        return False
    @classmethod
    def admin_check_pay_result(self, trans):
        receipt_data =''
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        path = '/var/www/upload/apple'+os.sep+str(year)+os.sep+str(month)
        pj = file(path+os.sep+str(trans.id), 'rb')
        for line in pj:
            print line
            receipt_data += line
        params = json.dumps({'receipt-data': receipt_data})
        conn = urllib2.Request(url=url, data=params)
        res_data = urllib2.urlopen(conn)
        res = res_data.read()
        json_res = json.loads(res)
        #print '-----------applepay-biz-json_res---------------------',json_res
        status = json_res.get('status')
        #print '----------applepay-biz-status-----------',status
        if int(status) == 21007:
            print '---------applepay-biz-sandbox-------------------'
            conn = urllib2.Request(url=test_url, data=params)
            res_data = urllib2.urlopen(conn)
            res = res_data.read()
            json_res = json.loads(res)

        receipt = json_res.get('receipt')
        print '---------applepay-biz-receipt-------------------',receipt
        in_app = receipt.get('in_app')
        print '---------applepay-biz-in_app-------------------',in_app
        in_app_array = sorted(in_app, key=lambda x: x['original_purchase_date_ms'], reverse=True)
        for app in in_app_array:
            original_purchase_date_ms = app.get('original_purchase_date_ms')
            print 'original_purchase_date_ms=', original_purchase_date_ms
            if (time.time()-int(original_purchase_date_ms)/1000)/86400 > 7:
                return False
            product_id = app.get('product_id')
            transaction_id = app.get('transaction_id')
            transaction = Transaction.query.filter_by(out_serial_no=transaction_id).filter_by(status='finished').first()
            if transaction:
                continue
            #print '---------applepay-biz-transaction_id------------------',transaction_id,'--------applepay-biz-product_id-------------',product_id
            config = SysConfig.get_json("apple_pay_list")
            amount = config.get(product_id)
            if amount == trans.amount:
                print 'trans.end=',transaction_id
                import hashlib
                m = hashlib.md5()
                m.update(transaction_id)
                score_log_lock = UserScoreLogLock()
                score_log_lock.sign = m.hexdigest()
                #print 'applepay-biz ------------- trans.end=', score_log_lock.sign
                try:
                    score_log_lock.insert()
                except Exception as e:
                    print 'e==', e
                    trans.out_serial_no = transaction_id
                    ChargeExecutor().execute(trans)
                trans.out_serial_no = transaction_id
                ChargeExecutor().execute(trans)
                print '----applepay-biz-----charge-------success-----------4'
                return True
        return False