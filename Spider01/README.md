## 从零开始搞爬虫
### 本节关键字 ###
*urllib | chardet*


在Python3.x中，我们可以使用urlib这个组件抓取网页，urllib是一个URL处理包，这个包中集合了一些处理URL的模块，如下：


>1.urllib.request模块是用来打开和读取URLs的；

>2.urllib.error模块包含一些有urllib.request产生的错误，可以使用try进行捕捉处理；

>3.urllib.parse模块包含了一些解析URLs的方法；

>4.urllib.robotparser模块用来解析robots.txt文本文件.它提供了一个单独的RobotFileParser类，通过该类提供的can_fetch()方法测试爬虫是否可以下载一个页面。

使用urllib.request.urlopen()这个接口函数就可以访问一个网站，读取并打印信息。
urlopen有一些可选参数，具体信息可以查阅Python自带的documentation。

了解到这些，我们就可以写一个最简单的程序，文件名为urllib_test01.py，感受一个urllib库的魅力：
```python
# -*- coding: UTF-8 -*-
from urllib import request

if __name__ == "__main__":
    response = request.urlopen("http://www.example.com")
    html = response.read()
    print(html)
```

urllib使用使用request.urlopen()访问和读取URLs信息，返回的对象response如同一个文本对象，我们可以调用read()，进行读取。再通过print()屏幕打印。

浏览器就是作为客户端从服务器端获取信息，然后将信息解析，再展示给我们的。但是显然他们都是二进制的乱码。

我们可以通过简单的decode()命令将网页的信息进行解码，并显示出来，我们新创建一个文件，命名为urllib_test02.py，编写如下代码：

```python
# -*- coding: UTF-8 -*-
from urllib import request

if __name__ == "__main__":
    response = request.urlopen("http://fanyi.baidu.com/")
    html = response.read()
    html = html.decode("utf-8")
    print(html)
```

这样我们就可以得到这样的结果，显然解码后的信息看起来工整和舒服多了：


当然这个前提是我们已经知道了这个网页是使用utf-8编码的，怎么查看网页的编码方式呢？非常简单的方法是使用使用浏览器审查元素，只需要找到head标签开始位置的chareset，就知道网页是采用何种编码。

这样我们就知道了这个网站的编码方式，但是这需要我们每次都打开浏览器，并找下编码方式，显然有些费事，使用几行代码解决更加省事并且显得酷一些。

我们需要安装第三方库chardet，它是用来判断编码的模块。安装好后，我们就可以使用chardet.detect()方法，判断网页的编码方式了。至此，我们就可以编写一个小程序判断网页的编码方式了，新建文件名为chardet_test01.py：
```Python
# -*- coding: UTF-8 -*-
from urllib import request
import chardet

if __name__ == "__main__":
    response = request.urlopen("http://www.example.com/")
    html = response.read()
    charset = chardet.detect(html)
    print(charset)
```
