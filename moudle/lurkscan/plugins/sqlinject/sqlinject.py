#! usr/bin/python 
#coding=utf-8 

import os

import urllib
from copy import deepcopy
from datetime import datetime

from moudle.lurkscan.pluginmanager import Check
from moudle.lurkscan.repeater import Repeate
from moudle.lurkscan.redis import ScanRedis
from moudle.lurkscan.plugins.sqlinject.template import *
from lib.connection.http import Request
from lib.connection.http import analysis_response
from lib.utils.common import md5

request_redis = {'ip':'192.168.5.131', 'port':6379}
result_handle = ScanRedis(request_redis['ip'], request_redis['port'], db = 15)

SQLINJECT_TARGET = 'SQL_INJECT_'

class InjectEntity():
	
	def __init__(self, url, params, headers, start_time = None, timeout = 5):
		self.url = url
		self.params = params
		self.headers = headers
		self.content = ''
		if not start_time:
			start_time = datetime.now()
		self.start_time = start_time
		self.timeout = timeout
		self.exp_req = {
							'urls':[],
							'params': {
							},
							'headers': {
							}
						}
	#计算时间差
	def time_diff(self, time = None):
		if not time:
			time = datetime.now()
		return (time - self.start_time).seconds
			
class SqlInject():
	
	def __init__(self):
		self._payloads = None
	
	def _load_payloads(self):
		raise Exception('load paylaods error !')
	
	#初始化攻击请求
	def _initialization_request(self, inject):
		result = []
		self._payloads = self._load_payloads()
		#有参数
		for key in inject.params:
			if not inject.exp_req['params'].has_key(key):
				inject.exp_req['params'][key] = []
			for payload in self._payloads:
				tmp = deepcopy(inject.params)
				tmp[key] += payload
				inject.exp_req['params'][key].append(tmp)

		return inject
	
	#检测是否为注入
	def _check(self, inject):
		raise Exception('_check_reponse undefined !')
	
	#md5(url + 所有参数的name组成的字符串)
	@staticmethod
	def get_key(url, params):
		param = ''
		for key in params:
			param += key
		return SQLINJECT_TARGET + md5(url + param)
	
	#设置超时
	def get_timeout(self):
		return 5
	
	def start(self):
		headers = self.redis_handle.iteritems()
		for header in headers:
			head_tmp = deepcopy(header.values()[0])
			key = SqlInject.get_key(header.values()[0]['request']['url'], head_tmp['request']['params'])
			#防止一个url的name相同而value不同二次注入检测的发生
			if result_handle.exists(key):
				continue
			inject = InjectEntity(header.values()[0]['request']['url'], header.values()[0]['request']['params'], header.values()[0]['request']['headers'])
			exp_inject = self._initialization_request(inject)
			for name in exp_inject.exp_req['params']:
				for param in exp_inject.exp_req['params'][name]:
					head_tmp['request']['params'] = param
					inject.start_time = datetime.now()
					response = Repeate(url = head_tmp['request']['url'], 
										params = head_tmp['request']['params'], 
										method = head_tmp['request']['method'], 
										headers = head_tmp['request']['headers'], 
										timeout = self.get_timeout()).replay()
					if response:
						inject.content = response.read()
						if self._check(inject):
							vuln_url = header.values()[0]['request']['url'] + Request.urlencode(head_tmp['request']['params'])
							print '*'*80
							print 'url : %s sql inject'%vuln_url
							print head_tmp['request']['params']
							#保存返回数据，漏洞复现依据
							head_tmp['response']['content'] = inject.content
							head_tmp['response']['code'] = response.code
							head_tmp['response']['headers'] = analysis_response(str(response.headers))['headers']
							head_tmp['response']['raw'] = str(response.headers)
							head_tmp['vuln'] = self.__class__.__name__
							result_handle.set(key, head_tmp)
							break
					else:
						pass
			
			for url in exp_inject.exp_req['urls']:
				response = Repeate(url = url, 
									params = head_tmp['request']['params'], 
									method = head_tmp['request']['method'], 
									headers = head_tmp['request']['headers']).replay()






























