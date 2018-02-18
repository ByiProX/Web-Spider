# -*- coding: UTF-8 -*-
from urllib import request
from urllib import error
import sys, re
import userAgents

class UrllibWithModifyHeader:
    """docstring for UrllibWithModifyHeader."""
    def __init__(self):
        # 这是一个PC + IE的UA
        PIUA = userAgents.pcUserAgent.get('IE 9.0')
        # 这是一个Mobile + UC的UA
        MUUA = userAgents.mobileUserAgent.get('UC standard')
        # 测试用的网站选择的有单翻译
        self.url = 'http://fanyi.youdao.com'

        self.useUA(PIUA, 1)
        self.useUA(MUUA, 2)


    def useUA(self, userAgent, name):
        req = request.Request(self.url)
        req.add_header(userAgent.split(':')[0],userAgent.split(':')[1])
        response = request.urlopen(req)
        fileName = str(name) + '.html'
        with open(fileName, 'a') as fp:
            fp.write('%s\n\n' %userAgent)
            fp.write(response.read().decode('utf-8'))

if __name__ == '__main__':
    test = UrllibWithModifyHeader()
