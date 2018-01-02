#! usr/bin/python 
#coding=utf-8 

import re
from copy import deepcopy

from moudle.lurkscan.pluginmanager import Check
from moudle.lurkscan.plugins.sqlinject.sqlinject import SqlInject
from moudle.lurkscan.plugins.xss.xss import Xss
class Reflection(Xss, Check):
	
	def __init__(self):
		pass
	
	def _load_payloads(self):
		return ['"><img src=x onerror=alert(1);>']
	
	def _check(self, xssety):
		print xssety.payload
		if re.search(xssety.payload, xssety.content, re.I):
			print '*'*100
			return xssety.payload