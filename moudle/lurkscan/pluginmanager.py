#! usr/bin/python 
#coding=utf-8 

import os
import sys

from imp import find_module
from imp import load_module

from lib.utils.common import current_path
from moudle.lurkscan.redis import ScanRedis

class PluginManager(type):
	#静态变量配置插件路径
	__PluginPath = os.path.split(os.path.realpath(__file__))[0] + '/plugins'

	#调用时将插件注册
	def __init__(self, name, bases, dict):
		if not hasattr(self, 'AllPlugins'):
			self.__AllPlugins = {}
		else:
			self.RegisterAllPlugin(self)

	#设置插件路径
	@staticmethod
	def SetPluginPath(path):
		if os.path.isdir(path):
			PluginManager.__PluginPath = path
		else:
			print '%s is not a valid path' % path
	
	#获取插件文件名
	@staticmethod
	def LoadPluginFile():
		plugins = []
		pluginPath = PluginManager.__PluginPath
		if not os.path.isdir(pluginPath):
			raise EnvironmentError, '%s is not a directory' % pluginPath
		
		items = os.listdir(pluginPath)
		for i in range(0, len(items)):
			if not '__init__' in items[i]:
				plugins.append(items[i] + '.py')
		return plugins
		
			
	#递归检测插件路径下的所有插件，并将它们存到内存中
	@staticmethod
	def LoadAllPlugin():
		fileHandle = None
		filePath = None
		dect = None
		pluginPath = PluginManager.__PluginPath
		items = PluginManager.LoadPluginFile()
		for item in items:
			moduleName = item[:-3]
			if moduleName not in sys.modules:
				fileHandle, filePath, dect = find_module(moduleName, [pluginPath + '/' + item[:-3]])
				try:
					moduleObj = load_module(moduleName, fileHandle, filePath, dect)
				finally:
					if fileHandle : fileHandle.close()

	#返回所有的插件
	@property
	def AllPlugins(self):
		return self.__AllPlugins

	#注册插件
	def RegisterAllPlugin(self, aPlugin):
		pluginName = '.'.join([aPlugin.__module__, aPlugin.__name__])
		pluginObj = aPlugin()
		self.__AllPlugins[pluginName] = pluginObj

	#注销插件
	def UnregisterPlugin(self, pLuginName):
		if pluginName in self.__AllPlugins:
			pluginObj = self.__AllPlugins[pluginName]
			del pluginObj

	#获取插件对象。
	def GetPluginObject(self,  pluginName = None):
		if pluginName is None:
			return self.__AllPlugins.values()
		else:
			result = self.__AllPlugins[pluginName] if pluginName in self.__AllPlugins else None
			return result

	#根据插件名字，获取插件对象。（提供插件之间的通信）
	@staticmethod
	def GetPluginByName(pluginName):
		if pluginName is None:
			return None
		else:
			for SingleModel in __ALLMODEL__:
				plugin = SingleModel.GetPluginObject(pluginName)
				if plugin:
					return plugin

#插件框架的接入点。便于管理各个插件。各个插件通过继承接入点类，利用Python中metaclass的优势，将插件注册。接入点中定义了各个插件模块必须要实现的接口。
class Demo(object):
	__metaclass__ = PluginManager

	def start(self):
		print 'Please write the start() function'

	def test(self, language):
		print 'Please write the test() function'

class ScanSettings:
	
	def __init__(self, redis):
		self.redis = None
		
class Check(object):
	__metaclass__ = PluginManager
	request_redis = {'ip':'192.168.5.131', 'port':6379}
	redis_handle = ScanRedis(request_redis['ip'], request_redis['port'], db = 0)
	
	def __init__(self):
		pass
	
	#反射调用接口
	def start(self):
		pass

__ALLMODEL__ = (Check, Demo)