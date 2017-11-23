#! usr/bin/python 
#coding=utf-8 

import sys
import os

from moudle.proxy import socks5
#socks5.start()

from moudle.scan.repeater import Repeate
from lib.core.oredis import ORedis
ors = ORedis('192.168.5.131', 6379)
#ors.empty()
headers = ors.iteritems()
for header in headers:
	print header.values()[0]['request']
data = """GET /re?3943=&uid=-&ref=http%3A%2F%2Fedu.csdn.net%2Fcombos&pid=toolbar&mod=popu_370&dsm=get&mtp=1&con=%E5%86%99%E5%8D%9A%E5%AE%A2%2Chttp%3A%2F%2Fwrite.blog.csdn.net%2Fpostedit%3Fref%3Dtoolbar&ck=-&curl=http%3A%2F%2Fedu.csdn.net%2FcollectCourse&session_id=1511418683262_0.24201990410988838&x-acl-token=status_js_dkuyqthzbajmncbsb_token HTTP/1.1
Host: dc.csdn.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://edu.csdn.net/collectCourse
Cookie: Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1511409011,1511409168,1511418683,1511420360; uuid_tt_dd=-4723239697671566415_20171113; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=1788*1*PC_VC; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1511420594; dc_tos=ozuzld; dc_session_id=1511418683262_0.24201990410988838; kd_user_id=40966a41-7224-476c-b596-e91e0b7dbee4; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2215fe7a5894928a-0052fa18eaa674-12676c4a-2304000-15fe7a5894a584%22%2C%22%24device_id%22%3A%2215fe7a5894928a-0052fa18eaa674-12676c4a-2304000-15fe7a5894a584%22%7D; sajssdk_2015_cross_new_user=1; kd_0e1a1f29-37da-4c44-8a33-b4735dc85f10_kuickDeal_pageIndex=2; kd_0e1a1f29-37da-4c44-8a33-b4735dc85f10_log_id=5a525a7b-8b75-4aad-8814-c8a66501d362%3Ad0bdc46c-becb-4db8-a57f-d4eb5c2d9b72%3A; kd_0e1a1f29-37da-4c44-8a33-b4735dc85f10_view_log_id=f83e7733-5952-4e2d-a00c-fde777edb7a6; kd_0e1a1f29-37da-4c44-8a33-b4735dc85f10_kuickDeal_leaveTime=1511420592991; avh=27488721
Connection: keep-alive

"""
#filename = os.path.basename("http://baodi")
#print(filename)
#ors.set_header('1', data)
#print ors.get('1')
repeate = Repeate()
#repeate.replay()
#repeate.test()
text = 'POST ss'
method = text[:3]
print method