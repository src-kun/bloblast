#! usr/bin/python 
#coding=utf-8 

import attr

from lib.connection import http
from moudle.lurkscan.redis import ScanRedis
from lib.utils import common

response_redis = {'ip':'192.168.5.131', 'port':8888}
request_redis = {'ip':'192.168.5.131', 'port':6379}
redis_handle = ScanRedis(request_redis['ip'], request_redis['port'], db = 0)
sql_redis_handle = ScanRedis(request_redis['ip'], request_redis['port'], db = 1)

class Repeate:
	
	def __init__(self, url, params, method, headers = {}, timeout = 5):
		self.url = url
		self.params = params
		self.header = headers
		self.timeout = timeout
		self.method = method
	
	def get_header(self):
		return self.header
	
	#重放请求
	def replay(self):
		req = http.Request(self.header)
		req.timeout = self.timeout
		method = getattr(req, self.method.lower())
		return method(self.url, self.params)