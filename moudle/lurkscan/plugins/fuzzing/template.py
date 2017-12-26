#! usr/bin/python 
#coding=utf-8 

import re
from copy import deepcopy

from moudle.lurkscan.pluginmanager import Check
from moudle.lurkscan.plugins.fuzzing.fuzzing import Fuzzing
from moudle.lurkscan.plugins.fuzzing.fuzzing import TestEntity
from moudle.lurkscan.plugins.fuzzing.fuzzing import FuzzingEntity
from moudle.lurkscan.comment import parse_xml
from lib.core.settings import bash_obj_path

#目录泄露
class DirectoryDisclosure(Fuzzing, Check):
	
	def __init__(self):
		pass
	
	def _load_payloads(self):
		return [TestEntity(key = 'bd6046897b0e4af69d054c856b8741fd', payload = '/../', title = 'list dir', errors = ['<title>Index of '], describe = 'list file')]
	
	def _check(self, xssety):
		for error in xssety.tety.errors:
			if re.search(error, xssety.content, re.I):
				return xssety


class File(Fuzzing, Check):
	
	def __init__(self):
		pass
		
	def _load_payloads(self):
		root = parse_xml(bash_obj_path + 'moudle/lurkscan/plugins/fuzzing/data/dirbuster.xml')
		result = []
		for child in root:
			for uri in child:
				result.append(TestEntity(key = child.attrib['key'], payload = uri.attrib['payload']))
		return result
	
	def _check(self, xssety):
		if xssety.code != 404:
			return True