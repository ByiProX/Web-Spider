## 爬虫攻防

#### 1 封锁间隔时间破解

Scrapy在两次请求之间的时间设置是DOWNLOAD_DELAY。如果不考虑反爬虫的因素，该值当然越小越好。如果
DOWNLOAD_DELAY设为0.001，也就是每1毫秒请求一次网页，这简直非人类干的事情。有些网站会检测一个ip
的访问时间，异常情况下会封锁该ip

#### 2 封锁Cookies
众所周知，网站是通过Cookie来确定用户身份的，Scrapy在爬取数据时使用同一个Cookies发起请求。该做法和把
DOWNLOAD_DELAY设为0.001没有本质区别。在scrapy中，直接社禁用Cookies就可以了。在settings.py中设置
```python
# Disable cookies (enabled by default)
COOKIES_ENABLED = False
```

#### 3 封锁user-agent和proxy破解
user-agent是浏览器的身份标识。网站通过UA来确定浏览器类型。很多浏览器拒绝不符合一定标准的UA请求网页。同一个UA高频率的访问网站会有被网站列入黑名单的危险。破解的方法很简单，可以准备一个**UA池**，每次请求时随机挑选一个进行请求。

在middlewares.py同级目录下创建UAResource.py,文件内容如下：

```python
#-*- coding: utf-8 -*-

UserAgents = [
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
  "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
  "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
  "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
  "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


Proxies = [
'http://122.114.31.177:808',
'http://1.2.3.4:80',
]
```

修改middlewares.py，添加内容为
```python
from .UAResource import UserAgents
from .UAResource import Proxies
import random

class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(Proxies)
        request.meta['proxy'] = proxy

class RandomUserAgent(object):
    """docstring for RandomUerAgent."""
    def process_request(self, request, spider):
        ua = random.choice(UserAgents)
        request.headers.setdefault('User-Agent', ua)
```

最后修改setting.py,将RandomUserAgent和RandomProxy添加到DOWNLOADER_MIDDLEWARES中，注意RandomProxy要放到RandomUserAgent之前，即将RandomProxy的值比RandomUserAgent后的值小
```python
DOWNLOADER_MIDDLEWARES = {
   # 'meijutt.middlewares.MeijuttDownloaderMiddleware': 543,
   'meijutt.middlewares.RandomProxy': 10,
   'meijutt.middlewares.RandomUserAgent': 30,

   # 禁止内置的(在 DOWNLOADER_MIDDLEWARES_BASE 中设置并默认启用的)中间件
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

```

免费代理不够稳定，如果不想用proxy，设置RandomProxy为None,即禁止使用
```python
'meijutt.middlewares.RandomProxy': None,
```
