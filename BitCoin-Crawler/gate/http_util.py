#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import urllib
import json
import hashlib
import hmac


def getSign(params, secretKey):
    bSecretKey = str(secretKey)

    sign = ''
    for key in params.keys():
        value = str(params[key])
        sign += key + '=' + value + '&'
    bSign = str(sign[:-1])

    mySign = hmac.new(bSecretKey, bSign, hashlib.sha512).hexdigest()
    return mySign


def httpGet(url, resource, params = ''):
    _url = url + resource + '/' + params if params else url + resource
    response = requests.get(_url, timeout = 10)
    data = response.content
    return json.loads(data)


def httpPost(url, resource, params, apiKey, secretKey):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "KEY": apiKey,
        "SIGN": getSign(params, secretKey)
    }

    tempParams = urllib.urlencode(params) if params else ''
    print(tempParams)

    response = requests.post(url + resource, timeout = 10, headers = headers, data = tempParams)
    data = response.content
    params.clear()
    return data
