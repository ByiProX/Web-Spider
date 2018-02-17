# -*- coding: UTF-8 -*-
from urllib import request
from urllib import error
import sys, re

def tipUse():
    '''显示提示信息'''
    print('该程序只能输入一个参数，这个参数必须是一个可用的proxy')
    print('usage: python testUrllibWithProxy.py http://59.110.221.56')
    print('usage: python testUrllibWithProxy.py https://59.110.221.56')


def testArgument():
    '''测试输入参数，只需要一个参数'''
    if len(sys.argv) !=2:
        print(只需要一个参数就OK)
        tipUse()
        exit()
    else:
        TP = testProxy(sys.argv[1])
