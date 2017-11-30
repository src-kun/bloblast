#! usr/bin/python 
#coding=utf-8 

import os

import redis
import pickle
import base64
from copy import deepcopy

from lib.connection import http

class ORedis:
	
	def __init__(self, ip, port, db):
		self.__ip = ip
		self.__port = port
		self.__db = db
		self.__output_handle = redis.Redis(host = self.__ip, port = self.__port, db = db)
		self.__storage_struct = {'request':{'method':'', 'url':'', 'headers':{}, 'params':{}}, 'response':{'code': -1, 'headers':'', 'content':''}, 'last_time':0}
	
	def get_storage_struct(self):
		return deepcopy(self.__storage_struct)
	
	def __filter(self, text):
		pass
	
	def set(self, key, value):
		self.__output_handle.set(str(key), base64.b64encode(str(value)))
	
	#TODO 
	def set_header(self, key, data):
		d = str(data)
		static_fix = ['jpg', 'css', 'js', 'png', 'gif', 'swf']
		suffix = ''
		result = http.analysis_header(d.replace('\r\n', '\\r\\n'))
		#TODO 优化过滤
		if result and not result['suffix'] in static_fix:
			storage_struct = self.get_storage_struct()
			storage_struct['request'].update(result)
			self.__output_handle.set(key, base64.b64encode(str(storage_struct)))
	
	def get(self, key):
		return eval(base64.b64decode(self.__output_handle.get(key)))
	
	def delete(self, key):
		self.__output_handle.delete(key)
	
	#遍历所有key，value，d=True 则遍历后删除
	def iteritems(self, d = False):
		result = []
		for key in self.__output_handle.scan_iter():
			#redis数据库内数据不纯净时会报错
			result.append(eval('{\'%s\':%s}'%(key, base64.b64decode(self.__output_handle.get(key)))))
			if d:
				self.__output_handle.delete(key)
		return result
	
	#清空redis
	def empty(self):
		for key in self.__output_handle.scan_iter():
			self.__output_handle.delete(key)
	
	def close(self):
		self.__output_handle.close()
#ors = ORedis('192.168.5.131', 6379)


#print ors.iteritems(True)
