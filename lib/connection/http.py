#! usr/bin/python 
#coding=utf-8 

import urllib 
import urllib2
import json

from lib.core.base import switch
from lib.core.exception import BloblastConnectionException
from lib.core.exception import BloblastDataException
from lib.core.exception import BloblastNoneDataException
from lib.core.log import logger


GET = 'GET'
POST = 'POST'
DELETE = 'DELETE'
PUT = 'PUT'
PATCH = 'PATCH'
OPTHION = 'OPTHION'

CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'Content-Type'
CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_JAVASCRIPT = 'application/javascript'
CONTENT_TYPE_IMAGE = 'image'

ACCEPT_ENCODING = 'Accept-Encoding'

IF_NONE_MATCH = 'If-None-Match'

HEADER_SPLIT_STR = '\r\n'
#测试时用
#HEADER_SPLIT_STR = '\n'


def analysis_methon(header):
	method = header[:3]
	for case in switch(method.lower()):
		if case('pos'):
			method = POST
		elif case('del'):
			method = DELETE
		elif case('pat'):
			method = PATCH
		elif case('opt'):
			method = OPTHION
	return method

#解析header成字典
def analysis_request(header):
	result = {'headers':{}, 'url':'', 'suffix':'', 'method':'', 'params':{}}
	method = ''
	url = None
	#调试的时候使用 header.split('\n')#
	head = header.split(HEADER_SPLIT_STR)
	if len(head) == 1:
		raise Exception("headers analysis faild: \n" + head[0])
		
	#提取method
	if 'Access-Control-Request-Method' in header:
		result['method'] = result['headers']['Access-Control-Request-Method']
	else:
		result['method'] = analysis_methon(header)
	
	for i in range(1, len(head) - 1):
		try:
			result['headers'].update(eval("{'" + head[i].replace(': ', '\':\'').replace('\r\n', '') + "'}"))
		except ValueError, e:
			#出现ValueError: dictionary update sequence element #0 has length 0; 2 is required错误，因为请求头中存在空行，忽略即可
			print e,head[i]
			pass
		except TypeError, e:
			#可能是因为提交的数据中存在二进制
			print e,head[i]
			pass
	if result['headers']:
		#提取url 协议 + 域名 + 请求资源
		result['url'] = 'http://' + result['headers']['Host'] + head[0][4:-9].strip(' ')
		if result['headers'].has_key('Host'):
			del result['headers']['Host']
		
		#提取参数和请求资源的类型（js/php/jsp..）
		param = ''
		if result['method'] == GET or result['method'] == DELETE:
			try:
				index = head[0][4:-9].index('?')
				param = head[0][4:-9][index + 1:]
				suffix = head[0][4:-9][:index].split('.')
				if len(suffix) >= 2:
					result['suffix'] = suffix[len(suffix) - 1]
			except ValueError, e:
				suffix = head[0][4:-9].split('.')
				if len(suffix) >= 2:
					result['suffix'] = suffix[len(suffix) - 1]
		else:
			param = head[len(head) - 1]

		#识别json
		if param and param[0] == '{' and param[len(param) - 1] == '}':
			result['headers'][CONTENT_TYPE] = CONTENT_TYPE_JSON
			result['params'].update(eval(param))
			param = eval(param)
		elif '=' in param:
			params = param.split('&')
			for ps in params:
				p = ps.split('=')
				if len(p) == 2:
					result['params'][p[0]] = p[1]
		else:
			result['params'][param] = ''
		
		#设置Content-length
		if result['headers'].has_key(CONTENT_LENGTH):
			result['headers'][CONTENT_LENGTH] = len(str(param))
		
		if result['headers'].has_key(ACCEPT_ENCODING):
			del result['headers'][ACCEPT_ENCODING]
		
		if result['headers'].has_key(IF_NONE_MATCH):
			del result['headers'][IF_NONE_MATCH]
		
		print '*'*50
		print result
		print '*'*50
		return result

#TODO 提取出content
def analysis_response(header):
	result = {'headers':{}, 'code':-1}
	index = 0
	head = header.split(HEADER_SPLIT_STR)
	if 'HTTP/' in head[0]:
		result['code'] = int(head[0][9:13])
		index = 1
	for i in range(index, len(head) - 1):
		if not head[i]:
			break
		result['headers'].update(eval("{'" + head[i].replace(': ', '\':\'').replace('\\r\\n', '') + "'}"))
	return result
	
class Request():

	def __init__(self, headers = {}, context = None):
		self.headers = headers
		self.context = context
		self.timeout = 5
	
	def __accept(self, url):
		if url is None:
			errMsg = "url is None !"
			logger.error(errMsg)
			raise BloblastNoneDataException(errMsg)
		elif cmp(url[0:4], "http"):
			errMsg = "{" +url + "}" + " You must start with (http[s]://)"
			logger.error(errMsg)
			raise BloblastDataException(errMsg)
	
	"""def get(self, url = None, lamb = 'GET'):
		self.__accept(url)
		try:
			request = urllib2.Request(url.encode('utf-8'), headers = self.headers)
			request.get_method = lambda: lamb
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
			if not cmp(lamb, 'GET') and response.code == 200:
				logger.info(url + " 200 ok")
		except urllib2.HTTPError,e:
			response = e
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
				#logger.exception("Exception Logged");
		return response"""
	
	def get(self, url, data = None):
		response = self.connect(url, lamb = 'GET')
		if response:
			if response.code == 200:
				logger.info(url + " 200 ok")
			else:
				logger.info(url + " %d "%response.code)
		return response
		
	"""def post(self, url = None, values = None, lamb = 'POST'):
		self.__accept(url)
		response = None
		data = None
		if not cmp(self.headers['Content-Type'], 'application/json'):
			data = json.dumps(values)
		elif values:
			data = urllib.urlencode(values)
		try:
			request = urllib2.Request(url.encode('utf-8'), data, self.headers)
			request.get_method = lambda: lamb
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
			if not cmp(lamb, 'POST') and response.code == 200:
				logger.info(url + " 200 ok")
		except urllib2.HTTPError,e:
			response = e
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
		return response"""
	def post(self, url, values = None):
		response = self.connect(url, values = values, lamb = 'POST')
		if response:
			if response.code == 200:
				logger.info(url + " 200 ok")
			else:
				logger.info(url + " %d "%response.code)
		return response

	def connect(self, url, lamb, values = None):
		self.__accept(url)
		response = None
		data = None
		#JSON 请求
		if values and self.headers.has_key('Content-Type') and not cmp(self.headers['Content-Type'], 'application/json'):
			data = json.dumps(values)
		elif values:
			data = urllib.urlencode(values)
		try:
			request = urllib2.Request(url.encode('utf-8'), data, self.headers)
			request.get_method = lambda: lamb
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
		except urllib2.HTTPError,e:
			response = e
			"""
			print e.code  
			print e.reason
			print e.geturl()  
			print e.read()
			"""
		except Exception,e:
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
		return response

	def put(self, url, values):
		response = self.connect(url, values = values, lamb = 'PUT')
		if response:
			if response.code == 200:
				logger.info(url + " 200 ok")
			else:
				logger.info(url + " %d "%response.code)
		return response
		
	def delete(self, url, data = None):
		response = self.connect(url, lamb = 'DELETE')
		if response:
			if response.code == 200:
				logger.info(url + " 200 ok")
			else:
				logger.info(url + " %d "%response.code)
		return response
		
	def patch(self, url, values = None):
		response = self.connect(url, values = values, lamb = 'PATCH')
		if response:
			if response.code == 200:
				logger.info(url + " 200 ok")
			else:
				logger.info(url + " %d "%response.code)
		return response

	def read(self, response):
		try:
			if response:
				return response.read()
		except urllib2.HTTPError,e:
			errMsg = e.geturl() + " " + str(e)
			logger.error(errMsg)
		except Exception,e:
			pass
		return None
