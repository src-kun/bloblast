#! usr/bin/python 
#coding=utf-8 

from lib.connection import http
from lib.core.oredis import ORedis
from lib.utils import common

response_redis = {'ip':'192.168.5.131', 'port':8888}
request_redis = {'ip':'192.168.5.131', 'port':6379}

class Repeate:
	
	def __init__(self):
		self.__als_headers = []
		self.__responses = []
		#redis 句柄
		self.__reqest_redis_handle = ORedis(request_redis['ip'], request_redis['port'])
	
	def replay(self):
		headers = self.__reqest_redis_handle.iteritems()
		for header in headers:
			key = header.keys()[0]
			values = header.values()[0]
			if values['request']['headers']:
				respose = http.Request(values['request']['headers']).get(values['request']['url'])
				if respose:
					#print '='*20
					#print respose.headers
					values['response']['headers'] = str(respose.headers)
					values['response']['content'] = str(respose.read())
					values['response']['code'] = respose.code
					self.__reqest_redis_handle.set(key, str(values))
				else:
					#TODO 访问失败处理
					pass
			else:
				#清理解析不了的数据
				self.__reqest_redis_handle.delete(key)
	
	def test(self):
		pass
		#print self.__reqest_redis_handle.iteritems()
		#print self.__reqest_redis_handle.empty()
