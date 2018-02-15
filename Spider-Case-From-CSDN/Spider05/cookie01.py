from urllib import request
from http import cookiejar

if __name__ == '__main__':
    # 读取cookie内容
    #声明一个CookieJar对象实例来保存cookie
    cookies = cookiejar.CookieJar()
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookies)
    #通过CookieHandler创建opener
    opener = request.build_opener(handler)
    #此处的open方法打开网页
    response = opener.open('http://www.baidu.com')
    #打印cookie信息
    for cookie in cookies:
        print('Name = %s' % cookie.name)
        print('Value = %s' % cookie.value)
