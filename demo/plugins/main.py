#! usr/bin/python 
#coding=utf-8 

import sys
from pluginmanager import PluginManager
from pluginmanager import __ALLMODEL__

if __name__ == '__main__':
    #加载所有插件
    PluginManager.LoadAllPlugin()

    #遍历所有接入点下的所有插件
    for SingleModel in __ALLMODEL__:
        plugins = SingleModel.GetPluginObject()
        for item in plugins:
            #调用接入点的公共接口
            item.Start()