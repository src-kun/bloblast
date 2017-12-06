#! usr/bin/python 
#coding=utf-8 

import os

import redis

from lib.connection import http

class ORedis:
	
	def _init_(self, ip, port, db):
		self._ip = ip
		self._port = port
		self._db = db
		self._output_handle = redis.Redis(host = self._ip, port = self._port, db = db)

	def set(self, key, value):
		self._output_handle.set(str(key), base64.b64encode(str(value)))
	
	def get(self, key):
		return self._output_handle.get(key)
	
	def delete(self, key):
		self._output_handle.delete(key)
	
	#遍历所有key，value，d=True 则遍历后删除
	def iteritems(self, d = False):
		result = []
		for key in self._output_handle.scan_iter():
			#redis数据库内数据不纯净时会报错
			result.append((key, self._output_handle.get(key)))
			if d:
				self._output_handle.delete(key)
		return result
	
	#清空redis
	def empty(self):
		for key in self._output_handle.scan_iter():
			self._output_handle.delete(key)
	
	def close(self):
		self._output_handle.close()
#ors = ORedis('192.168.5.131', 6379)


#print ors.iteritems(True)
