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
	
	def _initialization_request(self, inject):
		result = []
		#有参数
		if inject.params:
			for key in inject.params:
				if not inject.exp_req['params'].has_key(key):
					inject.exp_req['params'][key] = []
				for payload in self._payloads:
					tmp = deepcopy(inject.params)
					tmp[key] += payload
					inject.exp_req['params'][key].append(tmp)
		else:
			#无参数
			for payload in self._payloads:
				inject.exp_req['urls'].append(inject.url + payload)
		return inject
	
	def _check_content(self, content):
		for error in self.__errors:
			if re.search(error, content, re.I):
				return error
		
class TimeInject(SqlInject):
	pass

class UnionInject(SqlInject):
	pass