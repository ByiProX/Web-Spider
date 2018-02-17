# -*- coding: UTF-8 -*-
from urllib import request
from urllib import error
import sys, re

def tipUse():
    '''显示提示信息'''
    print('该程序只能输入一个参数，这个参数必须是一个可用的proxy')
    print('usage: python3 testUrllibWithProxy.py http://59.110.221.56:80')
    print('usage: python3 testUrllibWithProxy.py https://59.110.221.56:80')


def testArgument():
    '''测试输入参数，只需要一个参数'''
    if len(sys.argv) != 2:
        print('只需要一个参数就OK')
        tipUse()
        exit()
    else:
        TP = TestProxy(sys.argv[1])

class TestProxy:
    """docstring for TestProxy."""
    def __init__(self, proxy):
        self.proxy = proxy
        self.checkProxyFormat(self.proxy)
        self.url = 'http://www.baidu.com'
        self.timeout = 5
        self.flagWord = '百度'
        self.useProxy(self.proxy)

    def checkProxyFormat(self, proxy):
        try:
            proxyMatch = re.compile('http[s]?://[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}:[\d]{1,5}$')
        except AttributeError:
            tipUse()
            exit()
        flag = 1
        proxy = proxy.replace('//', '')

        try:
            protocal = proxy.split(':')[0]
            ip = proxy.split(':')[1]
            port = proxy.split(':')[2]
        except IndexError:
            print('下标出界')
            tipUse()
            exit()

        flag = flag and len(proxy.split(':'))==3 and (len(ip.split('.'))==4)
        flag = ip.split('.')[0] in map(str,range(1,256)) and flag
        flag = ip.split('.')[1] in map(str,range(256)) and flag
        flag = ip.split('.')[2] in map(str,range(256)) and flag
        flag = ip.split('.')[3] in map(str,range(1,256)) and flag
        flag = protocal in ['http', 'https'] and flag
        falg = port in map(str,range(1,65536)) and flag

        if flag:
            print('输入的代理服务器符合标准')
        else:
            tipUse()
            exit()


    def useProxy(self, proxy):
        '''利用代理访问百度,并查找关键字'''
        protocal = proxy.split('//')[0].replace(':','')
        ip = proxy.split('//')[1]
        # 创建ProxyHandler
        proxy_support = request.ProxyHandler({protocal:ip})
        # 创建Opener
        opener = request.build_opener(proxy_support)
        # 安装OPener
        request.install_opener(opener)

        try:
            response = request.urlopen(self.url, timeout=self.timeout)
        except:
            print('连接错误，退出程序')
            exit()
        content = response.read().decode('utf-8')
        print(content)
        if re.search(self.flagWord, content):  # 如果没有.decode('utf-8')，会报错哦
            print('已取得特征词，该代理可用')
        else:
            print('该代理不可用')


if __name__ == '__main__':
    testArgument()
