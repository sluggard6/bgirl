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
	DOMAIN = '127.0.0.1'
	HTTP_DOMAIN = 'https://' + DOMAIN
	STATIC_HTTP_REF = ''
	HIWIFI_HTTP_DOMAIN = 'https://hi-wifi.cn'
	SQLALCHEMY_DATABASE_URI = 'mysql://root:admin1234@127.0.0.1:3306/bgirl'
	SQLALCHEMY_BINDS = {
		'data': 'mysql://root:admin1234@127.0.0.1:3306/bgirl'
	}
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	# redis-server
	REDIS_HOST = '127.0.0.1'
	REDIS_PASSWORD = ''
	REDIS_PORT = 6379
	REDIS_DB = 0  # rq redis配置
	# session config
	SESSION_COOKIE_NAME = 'la_seid'
	SECRET_KEY = '\x19\xb4\xaaA\xec\xd43z]\xce\x1cW\xbe\x980\xceJ\xb7\xaf\x14OR\xb2\xca'
	PERMANENT_SESSION_LIFETIME = 1800

	SESSION_COOKIE_DOMAIN = DOMAIN
	REDIS_URL = 'redis://127.0.0.1:6379/0'
	REDIS_JOB_HOST = '127.0.0.1'
	REDIS_JOB_PORT = 6379
	REDIS_JOB_PASSWORD = ''
	REDIS_KVDB = {'common': 0, 'session': 0}
	# sms repeat limit
	USER_BIND_PHONE_VCODE_EXPIRE = 3600

	# mail config
	MAIL_SERVER = 'smtp.exmail.qq.com'
	# MAIL_USERNAME = 'webmaster@hi-wifi.cn'
	# MAIL_PASSWORD = 'luhu#2014!'
	MAIL_USERNAME = 'caoyonghui@hi-wifi.cn'
	MAIL_PASSWORD = 'Cao2014'
	MAIL_DEFAULT_SENDER = '乐无限 <caoyonghui@hi-wifi.cn>'
	MAX_CONTENT_LENGTH = 500 * 1024 * 1024
	# 系统测试账号
	SYS_TEST_ACCOUNT = [10000000900, 10000001000]

	APP_LOG_FILE = '/Users/john/git/meimei/luhu_admin.log'
	LUHU_LIB_DIR = '/usr/hiwifi/lib'
	CLIENT_AGENT_MARK = 'com.domi.giftpi'

	ASSETS_DEBUG = False

	SUPPORT_HTTPS = True

	AMOUNT_SCORE_EXCHANGE_RATIO = 2

	UPLOAD_HANDLER = {
		'apk': {
			'upload_folder': '/var/www/upload/apk/',
			'allowed_ext': ['.apk'],
		},
		'image': {
			'upload_folder': '/var/www/upload/image/',
			'allowed_ext': ['.jpeg', '.jpg', '.png', '.bmp', '.gif'],
		},
		'file': {
			'upload_folder': '/var/www/upload/file/',
			'allowed_ext': ['.txt'],
		},
		'photo': {
			'upload_folder': '/var/www/upload/photo/',
			'allowed_ext': ['.jpg', '.jpeg', '.png'],
			'handlers': {
				'origin': {
					'method': 'zoom',  # zoom按比例缩放
					'long': 1280,  # 最大边1280
				},
				'standard': {
					'method': 'zoom',
					'short': 500,  # 最小边500
					'ext': 'standard'
				},
				'thumb': {
					'method': 'square',  # 正方形剪切
					'side': 160,  # 边长160
					'ext': 'thumb'
				}
			}
		},
		'avatar': {
			'upload_folder': '/var/www/upload/avatar/',
			'allowed_ext': ['.jpg', '.jpeg', '.png'],
			'handlers': {
				'origin': {
					'method': 'square',
					'side': 200
				}
			}
		},
		'qrcode': {
			'upload_folder': '/var/www/upload/qrcode/',
			'allowed_ext': ['.jpg', '.jpeg', '.png'],
			'handlers': {
				'origin': {
					'method': 'square',
					'side': 200
				}
			}
		},

	}

	DOWNLOAD_HOST = "http://static.hi-wifi.cn"
	MONTH_FEE_SCORE = 5000
	DAILY_CONTINUE_SCORE = 30
	DAILY_SCORE = 10
	SCORE_SCALE = 250
	API_HOST = 'https://api.hi-wifi.cn'
	MOBILE_HOST = 'https://m.hi-wifi.cn'

	ACCOUNT_CHECKING_TITLE = u"自动对账"

	YEEPAY_FTP_FILE_PATH = "/var/www/upload/file/yeepay_ftp/"


class Release(Production):
	LOG_DEBUG = True
	# DEBUG = True
	DOMAIN = 'test.admin.server.hi-wifi.cn/'

	HTTP_DOMAIN = 'http://' + DOMAIN
	STATIC_HTTP_REF = ''

	SQLALCHEMY_DATABASE_URI = 'mysql://luhu:lu@hu#2014@test-db-01/luhu'
	SQLALCHEMY_BINDS = {
		'data': 'mysql://luhu:lu@hu#2014@test-db-01/luhu',
		'slave': 'mysql://luhu:lu@hu#2014@test-db-01/luhu',
		'card': 'mysql://luhu:lu@hu#2014@test-db-01/payment',
		'apas': 'mysql://luhu:lu@hu#2014@test-db-01/apas',
		'project': 'mysql://luhu:lu@hu#2014@test-db-01/area',
		'market': 'mysql://luhu:lu@hu#2014@test-db-01/market',
		'foxconn': 'mysql://hiwifi:H*SjJ)qS3bF@10.135.80.40/luhu',
		'auth': 'mysql://auth:authtest@20151023@test-db-01/auth',
		'sms': 'mysql://sms:smstest@20160504@test-db-01/sms',
		'game': 'mysql://game:nkBpBOtDmvegJhqD@db-data:3306/game',
		'KTLOG': 'mysql://browser:s@de5&dE@180.150.177.130:10031/KTLOG',
		'video': 'mysql://video:videotest@201612@test-db-01/video',
		'guian': 'mysql://root:uK92Awqh1ULVAHcz@210.83.232.55:3306/luhu'
	}
	USER_MAILBIND_URL = HTTP_DOMAIN + '/auth/email/%(vcode)s'
	SESSION_COOKIE_DOMAIN = None
	REDIS_URL = 'redis://123.206.15.218:6379/0'
	REDIS_HOST = '123.206.15.218'
	REDIS_JOB_HOST = '123.206.15.218'
	REDIS_PORT = 6379
	REDIS_PASSWORD = 'crs-oj7t4z7i:hiwifi@2016'
	# assets设置
	ASSETS_DEBUG = True

	APP_LOG_FILE = '/var/log/hiwifi/luhu_admin/luhu_admin_release.log'

	LUHU_LIB_DIR = '/usr/hiwifi/lib/release'

	SUPPORT_HTTPS = False

	AUTH_API = "http://as.hi-wifi.cn"
	PERMISSION_LIMIT = "no"

	API_HOST = 'http://test.api.hi-wifi.cn'
	DOWNLOAD_HOST = "http://test.static.hi-wifi.cn"
	MOBILE_HOST = 'http://test.m.hi-wifi.cn'


class Development(Release):
	DOMAIN = '180.168.36.206:8286'
	HTTP_DOMAIN = 'http://' + DOMAIN

	APP_LOG_FILE = '/var/log/hiwifi/luhu_admin_dev.log'

	# 关联站点
	GIFTPI_HTTP = 'http://180.168.36.206:8280'
