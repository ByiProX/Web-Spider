# -*- coding: UTF-8 -*-
from urllib import request
from urllib import parse
import json

if __name__ == "__main__":
    Req_URL = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    Form_Data = {
    "type" : "AUTO",
    "i" :"eat",
    "doctype" : "json",
    "version" : "2.1",
    "keyfrom" : "fanyi.web",
    "ue" : "UTF-8",
    "action" : "FY_BY_CLICKBUTTON"
    }

    data = parse.urlencode(Form_Data).encode('utf-8')
    #传递Request对象和转换完格式的数据
    req = request.Request(Req_URL, data)
    response = request.urlopen(req)
    # #读取信息并解码
    html = response.read().decode('utf-8')
    #使用JSON
    translate_results = json.loads(html)
    print(translate_results)
    #找到翻译结果
    t = translate_results['translateResult'][0][0]['tgt']
    #打印翻译信息
    print("翻译的结果是：%s" % t)
