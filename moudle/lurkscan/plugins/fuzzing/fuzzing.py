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

FUZZING_TARGET = 'FUZZING_'

class TestEntity():
	
	def __init__(self, key, payload, title = '', errors = '', describe = ''):
		self.key = key
		self.payload = payload
		self.errors = errors
		#漏洞名称
		self.title = title
		#漏洞描述
		self.describe = describe

class FuzzingEntity():
	
	def __init__(self, request, tety):
		self.request = request
		self.url = request['url']
		self.headers = request['headers']
		self.params = request['params']
		self.method = request['method']
		self.content = ''
		self.code = -1
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
		#生成urlpayload
		for tety in self._tetys:
			req_tmp = deepcopy(request)
			if req_tmp['url'][-1] == '/':
				req_tmp['url'] = req_tmp['url'][:-1] + tety.payload
			else:
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
	
	def start(self, headers):
		self._tetys = self._load_payloads()
		for header in headers:
			key = Fuzzing.get_key(header.values()[0]['request']['url'], header.values()[0]['request']['params'])
			fzetys = self._initialization_request(header.values()[0]['request'])
			for fzety in fzetys:
				response = Repeate(url = fzety.url, 
									params = fzety.params, 
									method = fzety.method, 
									headers = fzety.headers, 
									timeout = self.get_timeout()).replay()
				if response:
					fzety.content = response.read()
					fzety.code = response.code
					if self._check(fzety):
						result = deepcopy(header.values()[0])
						poc = fzety.url
						print '*'*80
						print 'fuzzing : %s %s '%(fzety.tety.title ,poc)
						print 'method : %s params: %s '%(fzety.method, Request.urlencode(fzety.params))
						print 'describe: %s'%(fzety.tety.describe)
						print fzety.params
						result['request'] = fzety.request
						#保存返回数据，漏洞复现依据
						result['response']['content'] = fzety.content
						result['response']['code'] = response.code
						result['response']['headers'] = analysis_response(str(response.headers))['headers']
						result['response']['raw'] = str(response.headers)
						result['vuln'] = self.__class__.__name__
						self.result_handle.set(key, result)
				else:
					pass
			