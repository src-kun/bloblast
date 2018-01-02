#! usr/bin/python 
#coding=utf-8 
import os
from copy import deepcopy

import urllib
from datetime import datetime
from moudle.lurkscan.repeater import Repeate
from moudle.lurkscan.redis import ScanRedis
from lib.connection.http import Request
from lib.connection.http import analysis_response
from lib.utils.common import md5
from moudle.lurkscan.settings import XSS

if XSS:
	from moudle.lurkscan.plugins.xss.template import *

XSS_TARGET = 'XSS_'

class XssEntity():
	
	def __init__(self, request, payload = ''):
		self.request = request
		self.url = request['url']
		self.headers = request['headers']
		self.params = request['params']
		self.method = request['method']
		self.content = ''
		self.payload = payload
	
class Xss():
	
 	def __init__(self): 
		self._payloads = None
	
	def _load_payloads(self):
		raise Exception('load paylaods error !')
	
	#初始化攻击请求
	def _initialization_request(self, request):
		result = []
		#有参数
		for key in request['params']:
			for payload in self._payloads:
				req_tmp = deepcopy(request)
				req_tmp['params'][key] += payload
				result.append(XssEntity(req_tmp, payload))
		
		#生成urlpayload
		#TODO 识别url链接中的变量、伪静态链接等
		for payload in self._payloads:
			req_tmp = deepcopy(request)
			req_tmp['url'] += payload
			result.append(XssEntity(req_tmp, payload))
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
		return XSS_TARGET + md5(url + param)
	
	#设置超时
	def get_timeout(self):
		return 5
	
	def start(self, headers):
		self._payloads = self._load_payloads()
		for header in headers:
			key = Xss.get_key(header.values()[0]['request']['url'], header.values()[0]['request']['params'])
			#防止一个url的name相同而value不同二次注入检测的发生
			if self.result_handle.exists(key):
				continue
			xssetyary = self._initialization_request(header.values()[0]['request'])
			for xssety in xssetyary:
				response = Repeate(url = header.values()[0]['request']['url'], 
									params = xssety.params, 
									method = xssety.method, 
									headers = xssety.headers, 
									timeout = self.get_timeout()).replay()
				if response:
					xssety.content = response.read()
					if self._check(xssety):
						result = deepcopy(header.values()[0])
						poc = header.values()[0]['request']['url'] + Request.urlencode(xssety.params)
						print '*'*80
						print 'url : %s xss inject'%poc
						print xssety.params 
						result['request'] = xssety.request
						#保存返回数据，漏洞复现依据
						result['response']['content'] = xssety.content
						result['response']['code'] = response.code
						result['response']['headers'] = analysis_response(str(response.headers))['headers']
						result['response']['raw'] = str(response.headers)
						result['vuln'] = self.__class__.__name__
						self.result_handle.set(key, result)
						break
				else:
					pass
			