# -*- coding: UTF-8 -*-
from urllib import request

if __name__ == "__main__":
    response = request.urlopen("http://www.example.com")
    html = response.read()
    print(html)
