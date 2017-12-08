#! usr/bin/python 
#coding=utf-8 
from pluginmanager import Model_ToolBarObj

class Plugin2(Model_ToolBarObj):
    def __init__(self):
        pass

    def Start(self):
        print "I am plugin2 , I am a ToolBar!"