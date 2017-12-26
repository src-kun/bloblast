#! usr/bin/python 
#coding=utf-8 

try: 
	import xml.etree.cElementTree as ET 
except ImportError: 
	import xml.etree.ElementTree as ET 
import sys 
	
try: 
	tree = ET.parse("dirbuster.xml")		 #打开xml文档 
	#root = ET.fromstring(country_string) #从字符串传递xml 
	root = tree.getroot()				 #获得root节点	
except Exception, e: 
	print "Error:cannot parse file:country.xml."
	sys.exit(1) 
print root.tag, "---", root.attrib
for child in root:
	for grandson in child:
		print grandson.tag, "---", grandson.attrib 