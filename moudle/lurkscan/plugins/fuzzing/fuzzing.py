#! usr/bin/python 
#coding=utf-8 

from moudle.lurkscan.pluginmanager import Check

from copy import deepcopy

import urllib
from datetime import datetime
from moudle.lurkscan.repeater import Repeate
from moudle.lurkscan.redis import ScanRedis
from lib.connection.http import Request
from lib.connection.http import analysis_response
from lib.utils.common import md5
from moudle.lurkscan.plugins.fuzzing.template import *

request_redis = {'ip':'192.168.5.131', 'port':6379}
result_handle = ScanRedis(request_redis['ip'], request_redis['port'], db = 15)

FUZZING_TARGET = 'FUZZING_'

class TestEntity():
	
	def __init__(self, title, payload, errors, describe = ''):
		self.payload = payload
		self.errors = errors
		self.title = title
		self.describe = describe

class FuzzingEntity():
	
	def __init__(self, request, tety):
		self.request = request
		self.url = request['url']
		self.headers = request['headers']
		self.params = request['params']
		self.method = request['method']
		self.content = ''
		self.tety = tety
	
class Fuzzing():
	
 	def __init__(self):
		#攻击实体 TestEntity
		self._tetys = None
	
	def _load_payloads(self):
		raise Exception('load paylaods error !')
	
	#初始化攻击请求
	def _initialization_request(self, request):
		result = []
		#有参数
		for key in request['params']:
			for tety in self._tetys:
				req_tmp = deepcopy(request)
				req_tmp['params'][key] += tety.payload
				result.append(FuzzingEntity(req_tmp, tety))
		
		#生成urlpayload
		#TODO 识别url链接中的变量、伪静态链接等
		for tety in self._tetys:
			req_tmp = deepcopy(request)
			req_tmp['url'] += tety.payload
			result.append(FuzzingEntity(req_tmp, tety))
		return result
	
	#检测是否为注入
	def _check(self, inject):
		raise Exception('_check_reponse undefined !')
	
	#md5(url + 所有参数的name组成的字符串)
	@staticmethod
	def get_key(url, params):
		param = ''
		for key in params:
			param += key
		return FUZZING_TARGET + md5(url + param)
	
	#设置超时
	def get_timeout(self):
		return 5
	
	def start(self):
		headers = self.redis_handle.iteritems()
		self._tetys = self._load_payloads()
		for header in headers:
			key = Fuzzing.get_key(header.values()[0]['request']['url'], header.values()[0]['request']['params'])
			#防止一个url的name相同而value不同二次注入检测的发生
			if result_handle.exists(key):
				continue
			fzetys = self._initialization_request(header.values()[0]['request'])
			for fzety in fzetys:
				response = Repeate(url = fzety.url, 
									params = fzety.params, 
									method = fzety.method, 
									headers = fzety.headers, 
									timeout = self.get_timeout()).replay()
				if response:
					fzety.content = response.read()
					if self._check(fzety):
						result = deepcopy(header.values()[0])
						poc = header.values()[0]['request']['url'] + Request.urlencode(fzety.params)
						print '*'*80
						print 'fuzzing : %s %s '%(fzety.tety.title ,poc)
						print 'describe: %s'%(fzety.tety.describe)
						print fzety.params
						result['request'] = fzety.request
						#保存返回数据，漏洞复现依据
						result['response']['content'] = fzety.content
						result['response']['code'] = response.code
						result['response']['headers'] = analysis_response(str(response.headers))['headers']
						result['response']['raw'] = str(response.headers)
						result['vuln'] = self.__class__.__name__
						result_handle.set(key, result)
						break
				else:
					pass
			