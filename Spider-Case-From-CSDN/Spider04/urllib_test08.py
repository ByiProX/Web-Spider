# -*- coding: UTF-8 -*-
from urllib import request

if __name__ == "__main__":
    url = 'http://auction.artron.net/paimai-art0073571548/'
    head = {}
    #写入User Agent信息
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    #创建Request对象
    req = request.Request(url, headers=head)
    #传入创建好的Request对象
    response = request.urlopen(req)
    print(dir(response))
    print(response.getheader)
    #读取响应信息并解码
    html = response.read().decode('utf-8')
    #打印信息
    # print(html)
