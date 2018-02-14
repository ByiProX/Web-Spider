**一、为什么要使用Cookie**

    Cookie，指某些网站为了辨别用户身份、进行session跟踪而储存在用户本地终端上的数据（通常经过加密)。   
    比如说有些网站需要登录后才能访问某个页面，在登录之前，你想抓取某个页面内容，登陆前与登陆后是不同的，或者不允许的。   
    使用Cookie和使用代理IP一样，也需要创建一个自己的opener。在HTTP包中，提供了cookiejar模块，用于提供对Cookie的支持。

![](http://img.blog.csdn.net/20170409144243654?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    http.cookiejar功能强大，我们可以利用本模块的CookieJar类的对象来捕获cookie并在后续连接请求时重新发送，比如可以实现模拟登录功能。该模块主要的对象有CookieJar、FileCookieJar、MozillaCookieJar、LWPCookieJar。

    **它们的关系：** CookieJar–派生–>FileCookieJar–派生–>MozillaCookieJar和LWPCookieJar

    **工作原理：**创建一个带有cookie的opener，在访问登录的URL时，将登录后的cookie保存下来，然后利用这个cookie来访问其他网址。查看登录之后才能看到的信息。

    同样，我们以实例进行讲解，爬取伯乐在线的面向对象的漂亮MM的邮箱联系方式。

**二、实战**

**1.背景介绍**

    在伯乐在线有这么一个有趣的模块，面向对象，它说白了就是提供了一个程序员(媛)网上相亲的平台。

    **URL:**[http://date.jobbole.com/](http://date.jobbole.com/)

    它的样子是这样的：

![](http://img.blog.csdn.net/20170409144753813?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    可以看到，这里有很多的相亲贴，随便点进去就会有网上相亲MM的详细信息，想获取MM的联系方式，需要积分，积分可以通过签到的方式获取。如果没有登陆账户，获取联系方式的地方是这个样子的：

![](http://img.blog.csdn.net/20170409144912938?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    如果登陆了账号，获取联系方式的地方是这个样子的：

![](http://img.blog.csdn.net/20170409144955289?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    想要爬取MM的联系邮箱，就需要用到我们本次讲到的知识，Cookie的使用。当然，首先你积分也得够。

    在讲解之前，推荐一款抓包工具–Fiddler，可以在Google Chrome的Google商店下载这个插件，它的样子是这样的：

![](http://img.blog.csdn.net/20170409145106869?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    可以看到，通过这个插件，我们可以很容易找到Post的Form Data等信息，很方便，当然也可以用之前讲得浏览器审查元素的方式查看这些信息。

**2.过程分析**

    在伯乐在线首页点击登陆的按钮，Fiddler的抓包内容如下：

![](http://img.blog.csdn.net/20170409145240590?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    从上图可以看出，真正请求的url是

> [http://www.jobbole.com/wp-admin/admin-ajax.php](http://www.jobbole.com/wp-admin/admin-ajax.php)

    Form Data的内容记住，这些是我们编程需要用到的。user_login是用户名，user_pass是用户密码。

    在点击取得联系邮箱按钮的时候，Fiddler的抓包内容如下：

![](http://img.blog.csdn.net/20170409145403065?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    从上图可以看出，此刻真正请求的url是

> [http://date.jobbole.com/wp-admin/admin-ajax.php](http://date.jobbole.com/wp-admin/admin-ajax.php)

    同样Form Data中内容要记下来。postId是每个帖子的id。例如，打开一个相亲贴，它的URL是[http://date.jobbole.com/4128/](http://date.jobbole.com/4128/)，那么它的这个postId就是4128。为了简化程序，这里就不讲解如何自动获取这个postId了，本实例直接指定postId。如果想要自动获取，可以使用beautifulsoup解析[http://date.jobbole.com/](http://date.jobbole.com/)返回的信息。beautifulsoup的使用。有机会的话，会在后面的爬虫笔记中进行讲解。

**3.测试**

    **1)将Cookie保存到变量中**

    首先，我们先利用CookieJar对象实现获取cookie的功能，存储到变量中，先来感受一下：

    # -*- coding: UTF-8 -*- from urllib import request from http import cookiejar if __name__ == '__main__': #声明一个CookieJar对象实例来保存cookie cookie = cookiejar.CookieJar() #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler handler=request.HTTPCookieProcessor(cookie) #通过CookieHandler创建opener opener = request.build_opener(handler) #此处的open方法打开网页 response = opener.open('http://www.baidu.com') #打印cookie信息 for item in cookie: print('Name = %s' % item.name) print('Value = %s' % item.value)

      * 1
      * 2
      * 3
      * 4
      * 5
      * 6
      * 7
      * 8
      * 9
      * 10
      * 11
      * 12
      * 13
      * 14
      * 15
      * 16
      * 17

    我们使用以上方法将cookie保存到变量中，然后打印出了cookie中的值，运行结果如下:

![](http://img.blog.csdn.net/20170409145652613?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    **2)保存Cookie到文件**

    在上面的方法中，我们将cookie保存到了cookie这个变量中，如果我们想将cookie保存到文件中该怎么做呢？方便以后直接读取文件使用，这时，我们就要用到FileCookieJar这个对象了，在这里我们使用它的子类MozillaCookieJar来实现Cookie的保存，编写代码如下：

    # -*- coding: UTF-8 -*- from urllib import request from http import cookiejar if __name__ == '__main__': #设置保存cookie的文件，同级目录下的cookie.txt filename = 'cookie.txt' #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件 cookie = cookiejar.MozillaCookieJar(filename) #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler handler=request.HTTPCookieProcessor(cookie) #通过CookieHandler创建opener opener = request.build_opener(handler) #此处的open方法打开网页 response = opener.open('http://www.baidu.com') #保存cookie到文件 cookie.save(ignore_discard=True, ignore_expires=True)

      * 1
      * 2
      * 3
      * 4
      * 5
      * 6
      * 7
      * 8
      * 9
      * 10
      * 11
      * 12
      * 13
      * 14
      * 15
      * 16
      * 17
      * 18

    cookie.save的参数说明：

  * ignore_discard的意思是即使cookies将被丢弃也将它保存下来；

  * ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入。

    在这里，我们将这两个全部设置为True。

    运行之后，cookies将被保存到cookie.txt文件中。我们可以查看自己查看下cookie.txt这个文件的内容。

    **3)从文件中获取Cookie并访问**

    我们已经做到把Cookie保存到文件中了，如果以后想使用，可以利用下面的方法来读取cookie并访问网站，感受一下：

    # -*- coding: UTF-8 -*- from urllib import request from http import cookiejar if __name__ == '__main__': #设置保存cookie的文件的文件名,相对路径,也就是同级目录下 filename = 'cookie.txt' #创建MozillaCookieJar实例对象 cookie = cookiejar.MozillaCookieJar() #从文件中读取cookie内容到变量 cookie.load(filename, ignore_discard=True, ignore_expires=True) #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler handler=request.HTTPCookieProcessor(cookie) #通过CookieHandler创建opener opener = request.build_opener(handler) #此用opener的open方法打开网页 response = opener.open('http://www.baidu.com') #打印信息 print(response.read().decode('utf-8'))

      * 1
      * 2
      * 3
      * 4
      * 5
      * 6
      * 7
      * 8
      * 9
      * 10
      * 11
      * 12
      * 13
      * 14
      * 15
      * 16
      * 17
      * 18
      * 19

    了解到以上内容，我们那就可以开始正式编写模拟登陆伯乐在线的程序了。同时，我们也可以获取相亲MM的联系方式。

**4.编写代码**

    我们利用CookieJar对象实现获取cookie的功能，存储到变量中。然后使用这个cookie变量创建opener，使用这个设置好cookie的opener即可模拟登陆，同笔记四中讲到的IP代理的使用方法类似。

    创建cookie_test.py文件，编写代码如下：

    # -*- coding: UTF-8 -*- from urllib import request from urllib import error from urllib import parse from http import cookiejar if __name__ == '__main__': #登陆地址 login_url = 'http://www.jobbole.com/wp-admin/admin-ajax.php' #User-Agent信息  user_agent = r'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36' #Headers信息 head = {'User-Agnet': user_agent, 'Connection': 'keep-alive'} #登陆Form_Data信息 Login_Data = {} Login_Data['action'] = 'user_login' Login_Data['redirect_url'] = 'http://www.jobbole.com/' Login_Data['remember_me'] = '0' #是否一个月内自动登陆 Login_Data['user_login'] = '********' #改成你自己的用户名 Login_Data['user_pass'] = '********' #改成你自己的密码 #使用urlencode方法转换标准格式 logingpostdata = parse.urlencode(Login_Data).encode('utf-8') #声明一个CookieJar对象实例来保存cookie cookie = cookiejar.CookieJar() #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler cookie_support = request.HTTPCookieProcessor(cookie) #通过CookieHandler创建opener opener = request.build_opener(cookie_support) #创建Request对象 req1 = request.Request(url=login_url, data=logingpostdata, headers=head) #面向对象地址 date_url = 'http://date.jobbole.com/wp-admin/admin-ajax.php' #面向对象 Date_Data = {} Date_Data['action'] = 'get_date_contact' Date_Data['postId'] = '4128' #使用urlencode方法转换标准格式 datepostdata = parse.urlencode(Date_Data).encode('utf-8') req2 = request.Request(url=date_url, data=datepostdata, headers=head) try: #使用自己创建的opener的open方法 response1 = opener.open(req1) response2 = opener.open(req2) html = response2.read().decode('utf-8') index = html.find('jb_contact_email') #打印查询结果 print('联系邮箱:%s' % html[index+19:-2]) except error.URLError as e: if hasattr(e, 'code'): print("HTTPError:%d" % e.code) elif hasattr(e, 'reason'): print("URLError:%s" % e.reason)

      * 1
      * 2
      * 3
      * 4
      * 5
      * 6
      * 7
      * 8
      * 9
      * 10
      * 11
      * 12
      * 13
      * 14
      * 15
      * 16
      * 17
      * 18
      * 19
      * 20
      * 21
      * 22
      * 23
      * 24
      * 25
      * 26
      * 27
      * 28
      * 29
      * 30
      * 31
      * 32
      * 33
      * 34
      * 35
      * 36
      * 37
      * 38
      * 39
      * 40
      * 41
      * 42
      * 43
      * 44
      * 45
      * 46
      * 47
      * 48
      * 49
      * 50
      * 51
      * 52
      * 53
      * 54

**5.运行结果如下：**

![](http://img.blog.csdn.net/20170409150252854?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYzQwNjQ5NTc2Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**三、总结**

    获取成功！如果看过之前的笔记内容，我想这些代码应该很好理解吧。
