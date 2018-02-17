# -*- coding: UTF-8 -*-
from urllib import request
from urllib import error

def linkBaidu():
    url = 'http://www.baidu.com'
    try:
        response = request.urlopen(url, timeout=1)
        print(response.read())
    except error.URLError as e:
        print('网络地址错误:', e)
        exit()

    with open('./baidu.txt', 'w') as fp:
        fp.write(response.read().decode('utf-8'))

    print(response.geturl())
    print(response.getcode())
    print(response.info())


if __name__ == '__main__':
    linkBaidu()
