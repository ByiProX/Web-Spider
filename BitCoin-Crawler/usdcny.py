import requests
import time
import re


def dollar_currency_rate():
    time_ = int(time.time() * 1000)

    url = 'http://hq.sinajs.cn/rn=' + str(time_) + 'list=fx_susdcny'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    rate = re.search(r'\d\.\d*', response.text[32:]).group(0)
    return rate


# print dollar_currency_rate()
