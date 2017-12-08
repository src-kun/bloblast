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
	#print header.values()[0]
	pass
#ors.empty()
data = """POST /users HTTP/1.1
Host: api.singulato.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://api.singulato.com/doc.html
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Content-Length: 50
Cookie: qqmail_alias=zhuqingchun@singulato.com; Hm_lvt_abbe4d2f9e02a240991cb8e5c6a5325d=1510730025,1510821102,1511313271,1511834728; singulato_token_product=aecfc9ccab0279eabd7cdf00f369e582; token=e669185f0941859ac81316aa701757a4
Connection: close

{"phone":"15223010203"}"""

#filename = os.path.basename("http://baodi")
#print(filename)
"""print
print
ors.set_header('1', data)
print ors.get('1')['request']
repeate = Repeate(ors.get('1')['request'])
response = repeate.replay()
print response.read()"""
#repeate.test()
data = """GET /metadatas?name=xianghao&system=tboss HTTP/1.1
Host: api.zhicheauto.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://api.zhicheauto.com/doc.html
Authorization: Token c494cb535d69a8918f12df08d19fbdbf
X-Requested-With: XMLHttpRequest
Cookie: token=c494cb535d69a8918f12df08d19fbdbf
Connection: close"""


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











