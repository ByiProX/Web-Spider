# -*- coding: UTF-8 -*-
from urllib import request
import chardet
# from pprint import pprint

if __name__ == "__main__":
    response = request.urlopen("http://www.example.com/")
    html = response.read().decode("utf-8")
    charset = chardet.detect(html)
    print(html)
