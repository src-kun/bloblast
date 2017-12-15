#! usr/bin/python 
#coding=utf-8 

import sys
import os

from moudle.lurkscan.repeater import Repeate
from moudle.lurkscan.redis import ScanRedis
from lib.connection.http import analysis_request
from lib.connection.http import analysis_response
from lib.connection import http
ors = ScanRedis('192.168.5.131', 6379, 0)
headers = ors.iteritems()
for header in headers:
	#print header
	pass
#ors.empty()


#filename = os.path.basename("http://baodi")
#print(filename)
#请求存储->取出->转发 测试代码
def test_repeate():
	data = """GET /test/vulnerabilities/sqli_blind/?id=1%27%20AND%20SLEEP(5)%20AND%20%27TgYR%27%3d%27TgYR&Submit=Submit HTTP/1.1
Host: 192.168.5.139
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Cookie: PHPSESSID=j5a9os8qcoprv41hfj5kptkm61; security=low
Connection: close
Upgrade-Insecure-Requests: 1"""
	ors.set_request('1', data)
	print ors.get('1')['request']
	#(self, url, params, method, headers = {}, timeout = 5):
	request = ors.get('1')['request']
	print request['params']
	repeate = Repeate(request['url'], request['params'], request['method'], request['headers'])
	response = repeate.replay()
	#print response.read()


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
res = ScanRedis('192.168.5.131', 6379, 15)
for r in res.iteritems():
	print r
res.empty()












