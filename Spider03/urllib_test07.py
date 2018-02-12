# -*- coding: UTF-8 -*-
from urllib import request
from urllib import error

if __name__ == "__main__":
    #一个不存在的连接
    url = "http://www.douyu.com/wkx.html"
    req = request.Request(url)
    try:
        responese = request.urlopen(req)
    except error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError")
            print(e.code)
        elif hasattr(e, 'reason'):
            print("URLError")
            print(e.reason)
