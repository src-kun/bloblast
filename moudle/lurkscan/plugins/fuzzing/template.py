#! usr/bin/python 
#coding=utf-8 

import re
from copy import deepcopy

from moudle.lurkscan.pluginmanager import Check
from moudle.lurkscan.plugins.fuzzing.fuzzing import Fuzzing
from moudle.lurkscan.plugins.fuzzing.fuzzing import TestEntity

class File(Fuzzing, Check):
	
	def __init__(self):
		pass
	
	def _load_payloads(self):
		return [TestEntity('list dir', payload = '../', errors = ['<title>Index of '], describe = 'Download the file')]
		#return ['../', '../boot.ini', '../../../../', '../../../../ all', '../../../../../../../../../../etc/*', '../../../../../../../../../../etc/passw*', '../../../../../../../../../../etc/passwd', '../../../../../../../../../boot.ini', '../../../../../../../../boot.ini', '../../../../../../../boot.ini', '../../../../../../Scandisk.log', '../../../../../../boot.ini', '../../../../../boot.ini', '../../../../../etc/passwd', '../../../../../winnt/repair/sam._', '../../../../boot.ini', '../../../../config.sys', '../../../../etc/hosts', '../../../../etc/passwd']
	
	def _check(self, xssety):
		for error in xssety.tety.errors:
			if re.search(error, xssety.content, re.I):
				return xssety