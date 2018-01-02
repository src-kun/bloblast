#! usr/bin/python 
#coding=utf-8 

import sys
import os

from moudle.lurkscan.repeater import Repeate
from moudle.lurkscan.redis import ScanRedis
from lib.connection.http import analysis_request
from lib.connection.http import analysis_response
from lib.connection import http

from moudle.lurkscan.settings import REDIS_IP
from moudle.lurkscan.settings import REDIS_PORT
from moudle.lurkscan.settings import URL_REPERTORY
from moudle.lurkscan.settings import VULN_REPERTORY
ors = ScanRedis(REDIS_IP, REDIS_PORT, URL_REPERTORY)
headers = ors.iteritems()
for header in headers:
	#print header
	pass
#ors.empty()


#filename = os.path.basename("http://baodi")
#print(filename)
#请求存储->取出->转发 测试代码
def test_repeate():
	data = """POST /test/vulnerabilities/xss_s/ HTTP/1.1
Accept-Encoding: identity
Content-Length: 45
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Connection: close
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Upgrade-Insecure-Requests: 1
Host: 192.168.5.139
Referer: http://192.168.5.139/test/vulnerabilities/xss_s/
Cookie: security=low; PHPSESSID=c314v7e1ua1pdkms9qefsr4gq4
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0
Content-Type: application/x-www-form-urlencoded

btnSign=Sign%2BGuestbook&mtxMessage=4"><img src=x>&txtName=4"""
	ors.set_request('1', data)
	print ors.get('1')['request']
	#(self, url, params, method, headers = {}, timeout = 5):
	request = ors.get('1')['request']
	print request['params']
	repeate = Repeate(request['url'], request['params'], request['method'], request['headers'])
	response = repeate.replay()
	print response.read()

#test_repeate()
"""header = analysis_request(data)
print header['headers']
req = http.Request(header['headers'])
#http://192.168.5.132:8111
print header['url']
response = req.get(header['url'], header['params'])
print response.headers
print response.read()

#ors.set_request('2', data)"""
#req = http.Request({})
#print req.combination_params({'pass':'p','user':'u'})


data = """HTTP/1.1 200 OK
Date: Mon, 04 Dec 2017 09:28:40 GMT
Server: Apache/2.4.29 (Debian)
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Vary: Accept-Encoding
Content-Length: 161
Connection: close
Content-Type: imagse

test
"""

#print analysis_response(data)
#ors.set_response('2', data)

from moudle.lurkscan import scan
scan.start()
res = ScanRedis(REDIS_IP, REDIS_PORT, VULN_REPERTORY)

for vulns in res.iteritems():
	for key in vulns:
		print vulns[key]['request']['url']
		print vulns[key]['request']['params']
		print vulns[key]['vuln']
		print vulns[key]['response']['code']
		print vulns[key]
res.empty()












