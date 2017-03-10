# -*- coding: utf-8 -*-
import json
import types
import urllib
import urllib2

ACCOUNT_URL = 'http://platformapi.hi-wifi.cn/v1/srv/account/'
APP_KEY = 'nGMBtt56WXpdMCFZ'


def md5(s):
	import hashlib
	if type(s) is not types.StringType:
		s = str(s)
	m = hashlib.md5()
	m.update(s)
	return m.hexdigest()


def doParams(params):
	"""
	客户端接口签名算法 把参数(包括系统参数和业务参数)除sign和空值外, 按照key的首字母顺序排序, 用key1+value1+key2+value2+...的方式拼接在一起,
	再在最后加上app_key,然后转UTF-8编码进行MD5后, 得到字符串再转小写。 即: md5(utf-8:k1+v1+k2+v2+...+kn+vn + app_key).toLowerCase()
	服务端接口签名算法 算法同上, 唯一不同的是将app_key替换成app_secret
	:param params:
	:return:重载后的params
	"""
	params = sorted(params.iteritems(), key=lambda k: k[0], reverse=False)
	s = ''
	p_list = []
	for p_key, p_value in params:
		if p_value is not None and p_value is not '':
			if type(p_value) is unicode:
				p_value = p_value.encode('utf-8')
			p_list.append([p_key, p_value])
			s += p_key + str(p_value)
	sign = md5((s + APP_KEY)).lower()
	print sign
	params = dict(p_list)
	params.update(dict(sign=sign))
	return params


def doPost(url, params):
	params = doParams(params)
	params = urllib.urlencode(params)
	# print params
	req = urllib2.Request(url=url, data=params)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	return res


def get(url):
	try:
		request = urllib2.urlopen(url)
		res = request.read()
		request.close()
		return res
	except:
		return None


def get_json(url):
	res = get(url)
	try:
		return json.loads(res)
	except:
		return None
