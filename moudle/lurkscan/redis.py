#! usr/bin/python 
#coding=utf-8 

import os

import redis
import pickle
import base64
from copy import deepcopy

from lib.connection import http
from lib.connection.http import CONTENT_TYPE
from lib.core.oredis import ORedis

class ScanRedis(ORedis):
	
	def __init__(self, ip, port, db):
		ORedis._init_(self, ip, port, db)
		self._storage_struct = {'request':{'method':'', 'url':'', 'headers':{}, 'params':{}, 'raw':''}, 'response':{'code': -1, 'headers':{}, 'content':'', 'raw':''}, 'last_time':0}
	
	def get_storage_struct(self):
		return deepcopy(self._storage_struct)
	
	def _filter(self, text):
		pass
	
	def set_response(self, key, value, content = None, code = None):
		result = http.analysis_response(value)
		#过滤非执行脚本
		if result['headers'].has_key(CONTENT_TYPE) and result['headers'][CONTENT_TYPE].find('image') != 0:
			data = self.get(key)
			data['response']['headers'] = result['headers']
			if code:
				data['response']['code'] = code
			else:
				data['response']['code'] = result['code']
			data['response']['content'] = content
			data['response']['raw'] = value
			self._output_handle.set(str(key), base64.b64encode(str(data)))
		else:
			#删除无用请求
			pass
	
	#保存request请求实体
	def set_request(self, key, value):
		header = str(value)
		static_fix = ['jpg', 'css', 'js', 'png', 'gif', 'swf']
		suffix = ''
		result = http.analysis_request(header)
		#过滤
		if result and not result['suffix'] in static_fix:
			storage_struct = self.get_storage_struct()
			storage_struct['request'].update(result)
			storage_struct['request']['raw'] = header
			self._output_handle.set(key, base64.b64encode(str(storage_struct)))
	
	def get(self, key):
		return eval(base64.b64decode(self._output_handle.get(key)))
	
	def delete(self, key):
		self._output_handle.delete(key)
	
	#遍历所有key，value，d=True 则遍历后删除
	def iteritems(self, d = False):
		result = []
		for key in self._output_handle.scan_iter():
			#redis数据库内数据不纯净时会报错
			result.append(eval('{\'%s\':%s}'%(key, base64.b64decode(self._output_handle.get(key)))))
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
