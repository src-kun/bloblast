#! usr/bin/python 
#coding=utf-8 

import attr

from lib.connection import http
from lib.core.oredis import ORedis
from lib.utils import common

response_redis = {'ip':'192.168.5.131', 'port':8888}
request_redis = {'ip':'192.168.5.131', 'port':6379}
redis_handle = ORedis(request_redis['ip'], request_redis['port'], db = 0)
sql_redis_handle = ORedis(request_redis['ip'], request_redis['port'], db = 1)

class Repeate:
	
	def __init__(self, header):
		self.__header = header
	
	def get_header(self):
		return self.__header
	
	#重放请求
	def replay(self):
		method = getattr(http.Request(self.__header['headers']), self.__header['method'].lower())
		return method(self.__header['url'], self.__header['params'])

		def test(self):
			pass
		#print self.__redis_handle.iteritems()
		#print self.__redis_handle.empty()

class Base(object):
	
	def __init__(self):
		self.__responses = []
		#redis 句柄
	
	#控制数据流入对外提供的接口，具体的漏洞测试模板覆写这个接口
	def inflow(self):
		return headers
	
	def test(self):
		headers = self.inflow()
		for header in headers:
			response = Repeate(header.values()[0]['request']).replay()
			if response:
				#print '='*20
				#print response.headers
				header.values()[0]['response']['headers'] = str(response.headers)
				header.values()[0]['response']['content'] = str(response.read())
				header.values()[0]['response']['code'] = response.code
				self.outflow(header)
			else:
				#TODO 访问失败处理
				pass
	
	#控制数据流出对外提供的接口，具体的漏洞测试模板覆写这个接口
	def outflow(self, header):
		pass

class Sql(Base):
	
	def inflow(self):
		return redis_handle.iteritems()
		
	def outflow(self, header):
		print header
		sql_redis_handle.set(header.keys()[0], header.values()[0])
			
	def main(self):
		
		test()
			
			
			
			
			
			
			
			
			
			