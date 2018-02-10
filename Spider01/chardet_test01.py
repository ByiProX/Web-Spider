# -*- coding: UTF-8 -*-
from urllib import request
import chardet

if __name__ == "__main__":
    response = request.urlopen("http://www.example.com/")
    html = response.read()
    charset = chardet.detect(html)
    print(charset)
