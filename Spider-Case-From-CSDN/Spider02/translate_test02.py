import urllib.request

import urllib.parse
import json
import time
import random
import hashlib

content = 'python'

url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

data = {}

u = 'fanyideskweb'
d = content
f = str(int(time.time()*1000) + random.randint(0,10))
c = 'ebSeFb%=XZ%T[KZ)c(sy!'

sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()
print(sign)
data['i'] = content
data['from'] = 'AUTO'
data['to'] = 'AUTO'
data['smartresult'] = 'dict'
data['client'] = 'fanyideskweb'
data['salt'] = f
data['sign'] = sign
data['doctype'] = 'json'
data['version'] = '2.1'
data['keyfrom'] = 'fanyi.web'
data['action'] = 'FY_BY_CL1CKBUTTON'
data['typoResult'] = 'false'

data = urllib.parse.urlencode(data).encode('utf-8')
req = urllib.request.Request(url=url, data=data, method='POST')
response = urllib.request.urlopen(req)
# print(dir(response))
# print(response.read())
print(response.read().decode('utf-8'))
