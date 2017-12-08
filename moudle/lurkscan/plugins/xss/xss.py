#! usr/bin/python 
#coding=utf-8 
from moudle.lurkscan.pluginmanager import Check

class Xss(Check):
    def __init__(self):
        pass

    #实现接入点的接口
    def start(self):
        print "I am xss"