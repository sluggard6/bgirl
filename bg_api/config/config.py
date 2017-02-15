# -*- coding:utf-8 -*-
"""

    config/config.py
    ~~~~~~~~~~~~~~

    系统配置

    定义开发机本地配置

    * 同目录下创建local.py
    * local.py中

        from config import Development
        class Local(Development):
            DEBUG=True
            ...

"""


class Production:
	SQLALCHEMY_POOL_RECYCLE = 15
	DEBUG = False
	DOMAIN = 'api.hi-wifi.cn'
	HTTP_DOMAIN = 'https://' + DOMAIN
	STATIC_HTTP_REF = ''
	SQLALCHEMY_DATABASE_URI = 'mysql://luhu:29UMp188Jazq07AP@db-web:3306/luhu'
	# 降低SQLALCHEMY的初始连接数
	SQLALCHEMY_POOL_SIZE = 2
	# SQLALCHEMY_MAX_OVERFLOW
	SQLALCHEMY_MAX_OVERFLOW = 3
    
    #
	SQLALCHEMY_BINDS = {
		'data': 'mysql://hiwifi:ftDEOH3at9vGxN7M@db-data:3306/luhu',
	}
    
    #hahaha
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# redis-server
	REDIS_HOST = '10.66.106.110'
	# REDIS_PASSWORD = 'crs-oflkfu3i:iHoVmt8gYTTaxD2k'
	REDIS_PORT = 6379

	# session config
	SESSION_COOKIE_NAME = 'seid'
	SECRET_KEY = '\x19\xb4\xaaA\xec\xd43z]\xce\x1cW\xbe\x980\xceJ\xb7\xaf\x14OR\xb2\xca'
	PERMANENT_SESSION_LIFETIME = 17280

	SESSION_COOKIE_DOMAIN = '.vogor.cn'
	REDIS_JOB_HOST = '10.141.63.241'
	REDIS_JOB_PORT = 6379
	REDIS_JOB_PASSWORD = ''

	REDIS_KVDB = {'common': 0, 'session': 0}
	# sms repeat limit
	USER_BIND_PHONE_VCODE_EXPIRE = 3600

	# mail config
	MAIL_SERVER = 'smtp.exmail.qq.com'
	MAIL_USERNAME = 'noreply@hi-wifi.cn'
	MAIL_PASSWORD = 'no51d@mi!'
	MAIL_DEFAULT_SENDER = '乐无限 <noreply@hi-wifi.cn>'

	# 系统测试账号
	SYS_TEST_ACCOUNT = [10000000900, 10000001000]

	APP_LOG_FILE = '/var/log/bgirl/bg_api.log'
	LIB_DIR = '/usr/bgirl/lib'
	CLIENT_AGENT_MARK = 'com.hiwifi.luhu'

	ASSETS_DEBUG = False

	SUPPORT_HTTPS = True

	UPLOAD_HANDLER = {
		'apk': {
			'upload_folder': '/var/www/upload/apk/',
			'allowed_ext': ['.apk'],
		},
		'image': {
			'upload_folder': '/var/www/upload/image/',
			'allowed_ext': ['.jpeg', '.jpg', '.png', '.bmp'],
		},
		'photo': {
			'upload_folder': '/var/www/upload/photo/',
			'allowed_ext': ['.jpg', '.jpeg', '.png'],
			'handlers': {
				'origin': {
					'method': 'zoom',  # zoom按比例缩放
					'long': 1920,  # 最大边1280
				},
				'standard': {
					'method': 'zoom',
					'long': 1280,  # 最小边500
					'ext': 'standard'
				},
				'thumb': {
					'method': 'square',  # 正方形剪切
					'side': 160,  # 边长160
					'ext': 'thumb'
				}
			}
		},
	}
	MONTH_FEE_SCORE = 5000
	DAILY_CONTINUE_SCORE = 30
	DAILY_SCORE = 10
	DOWNLOAD_HOST = "http://rs.hi-wifi.cn"
	PAYMENT_WARES_ID = u'1'

	AUTH_API = "http://auth.hi-wifi.cn"

	API_HOST = 'https://api.hi-wifi.cn'
	MOBILE_HOST = 'https://m.hi-wifi.cn'

	CHARGE_RESTRICT_API = ['61.174.8.251', '101.69.178.209', '122.226.44.71', '101.69.178.211', '122.226.73.182',
						   '10.4.13.191', '10.4.1.158',
						   '122.226.44.89', '10.4.16.40', '10.4.9.153', '10.4.1.158', '10.4.13.191']

	MONTH_FEE_MONEY = 3000  # 单位为分

	AMOUNT_SCORE_EXCHANGE_RATIO = 2
	GUIAN_FOXCONN = False




class Release(Production):
	# LOG_DEBUG = True
	# DEBUG = True
	DOMAIN = 'test.api.vogor.cn'

	HTTP_DOMAIN = 'http://' + DOMAIN
	STATIC_HTTP_REF = ''

	SQLALCHEMY_DATABASE_URI = 'mysql://admin:admin$bgirl#2016!@10.9.98.127:3306/bgirl?charset=utf8'

	# SQLALCHEMY_POOL_TIMEOUT = 180
	SQLALCHEMY_POOL_RECYCLE = 180

	USER_MAILBIND_URL = HTTP_DOMAIN + '/auth/email/%(vcode)s'
	SESSION_COOKIE_DOMAIN = ".vogor.cn"
	REDIS_HOST = '10.9.98.127'
	REDIS_JOB_HOST = '10.9.98.127'
	REDIS_PORT = '6379'
	# REDIS_PASSWORD = 'crs-oj7t4z7i:hiwifi@2016'
	# assets设置
	ASSETS_DEBUG = True

	APP_LOG_FILE = '/var/log/bgirl/bg_api/bg_api_release.log'

	LIB_DIR = '/usr/bgirl/lib/release'

	SUPPORT_HTTPS = False


	PAYMENT_WARES_ID = u'1'

	DOWNLOAD_HOST = "http://test.rs.vogor.cn"



class Development(Release):
	DOMAIN = '180.153.152.60:8286'
	HTTP_DOMAIN = 'http://' + DOMAIN

	REDIS_JOB_HOST = '10.4.16.219'
	# 关联站点
	GIFTPI_HTTP = 'http://180.153.152.60:8280'
