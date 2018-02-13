# -*- coding: UTF-8 -*-
from urllib import request
from pprint import pprint

if __name__ == "__main__":
    #访问网址
    url = 'http://ip.chinaz.com/getip.aspx'
    # url = 'http://www.whatismyip.com.tw/'
    # url = 'http://www.ip.cn/'
    #这是代理IP

    # proxy = {'https':'59.110.221.56:80'}
    proxy = {'https':'111.155.116.247:8123'}

    #创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    #创建Opener
    opener = request.build_opener(proxy_support)
    #添加User Angent
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')]
    #安装OPener
    request.install_opener(opener)
    #使用自己安装好的Opener
    response = request.urlopen(url)
    #读取相应信息并解码
    html = response.read().decode("utf-8")
    #打印信息
    pprint(html)
