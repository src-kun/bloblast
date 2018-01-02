#! usr/bin/python 
#coding=utf-8 

import sys

from moudle.lurkscan.redis import ScanRedis
from moudle.lurkscan.repeater import Repeate
from pluginmanager import PluginManager
from pluginmanager import __ALLMODEL__
from moudle.lurkscan.settings import REDIS_IP
from moudle.lurkscan.settings import REDIS_PORT
from moudle.lurkscan.settings import URL_REPERTORY
from moudle.lurkscan.settings import VULN_REPERTORY


request_redis = {'ip':'192.168.5.131', 'port':6379}
redis_handle = ScanRedis(request_redis['ip'], request_redis['port'], db = 0)

#循环一遍所有请求获取到正常response
#TODO多线程
def repeater():
	headers = redis_handle.iteritems()
	for header in headers:
		response = Repeate(header.values()[0]['request'], {'timeout':5}).replay()
		if response:
			redis_handle.set_response(header.keys()[0], str(response.headers), str(response.read()), response.code)
		else:
			pass

def start():
	#repeater()
	#加载所有插件
	PluginManager.LoadAllPlugin()
	redis_handle = ScanRedis(REDIS_IP, REDIS_PORT, db = URL_REPERTORY)
	headers = redis_handle.iteritems()
	#TODO 多线程
	#遍历所有插件
	for SingleModel in __ALLMODEL__:
		plugins = SingleModel.GetPluginObject()
		for item in plugins:
			#调用接口
			item.start(headers)
