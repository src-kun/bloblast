#! usr/bin/python 
#coding=utf-8 

try: 
	import xml.etree.cElementTree as ET 
except ImportError: 
	import xml.etree.ElementTree as ET 
import sys 

def parse_xml(path):
	root = None
	try: 
		tree = ET.parse(path)
		root = tree.getroot()
	except Exception, e: 
		print "Error:cannot parse file:country.xml."
	return root