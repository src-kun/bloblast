#! usr/bin/python 
#coding=utf-8 

import os
from copy import deepcopy

from moudle.lurkscan.pluginmanager import Check
from moudle.lurkscan.repeater import Repeate
from moudle.lurkscan.redis import ScanRedis
from moudle.lurkscan.plugins.sqlinject.template import *
from lib.connection.http import Request
from lib.utils.common import md5

request_redis = {'ip':'192.168.5.131', 'port':6379}
result_handle = ScanRedis(request_redis['ip'], request_redis['port'], db = 15)

SQLINJECT_TARGET = 'SQL_INJECT'

class InjectEntity():
	
	def __init__(self, url, params, headers):
		self.url = url
		self.params = params
		self.headers = headers
		self.exp_req = {
							'urls':[],
							'params': {
							},
							'headers': {
							}
						}
						
class SqlInject():
	
	def __init__(self):
		self._payloads = None
	
	def _load_payloads(self):
		raise Exception('load paylaods error !')
	
	#初始化攻击请求
	def _initialization_request(self, header, params):
		raise Exception('_initialization_request undefined !')
	
	#检测返回中的错误信息
	def _check_content(self, response):
		raise Exception('_check_reponse undefined !')
	
	def start(self):
		self._payloads = self._load_payloads()
		headers = self.redis_handle.iteritems()
		for header in headers:
			inject = InjectEntity(header.values()[0]['request']['url'], header.values()[0]['request']['params'], header.values()[0]['request']['headers'])
			exp_inject = self._initialization_request(inject)
			head_tmp = deepcopy(header.values()[0])
			for name in exp_inject.exp_req['params']:
				for param in exp_inject.exp_req['params'][name]:
					head_tmp['request']['params'] = param
					response = Repeate(url = head_tmp['request']['url'], 
										params = head_tmp['request']['params'], 
										method = head_tmp['request']['method'], 
										headers = head_tmp['request']['headers']).replay()
					if response:
						content = response.read()
						if self._check_content(content):
							vuln_url = header.values()[0]['request']['url'] + Request.combination_params(header.values()[0]['request']['params'])
							print '*'*80
							print 'url : %s sql inject'%vuln_url
							print head_tmp['request']['params']
							#还原head_tmp结构
							head_tmp['request']['params'] = header.values()[0]['request']['params']
							head_tmp['response']['raw'] = content
							head_tmp['vuln'] = self.__class__.__name__
							result_handle.set(md5(vuln_url), head_tmp)
							break
					else:
						pass
			
			for url in exp_inject.exp_req['urls']:
				response = Repeate(url = url, 
									params = head_tmp['request']['params'], 
									method = head_tmp['request']['method'], 
									headers = head_tmp['request']['headers']).replay()






























