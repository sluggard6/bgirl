# -*- coding:utf-8 -*-
import time
from luhu_biz.lib.http_utils import doPost
from sharper.flaskapp.helper import get_client_ip

platform_api_url = 'http://platformapi.hi-wifi.cn/v1/srv'
app_id = 'python'


def send_sms(phone, msg):
    url = platform_api_url + '/sms/mt'
    params = dict(app_id=app_id,
                  timestamp=str(int(time.time())),
                  sign_method='md5',
                  phone=phone,
                  msg=msg,
                  biz_type=1,
                  biz_code=1,
                  client_ip=get_client_ip())
    return doPost(url, params)
