# -*- coding: utf-8 -*-
from urllib import request
import re
import threading

class TestProxy(object):
    """docstring for TestProxy."""
    def __init__(self):
        self.sFile = 'proxy.txt'
        self.dFile = 'aliveProxy.txt'
        self.URL ='https://www.baidu.com'
        self.threads = 10
        self.timeout = 3
        self.regex = re.compile('baidu.com')
        self.aliveList =[]

        self.run()

    def run(self):
        with open(self.sFile, 'r') as fp:
            lines = fp.readlines()
            line = lines.pop()
            while lines:
                for i in range(self.threads):
                    t = threading.Thread(target=self.linkWithProxy,args=(line,))
                    t.start()
                    if lines:
                        line = lines.pop()
                    else:
                        continue

        with open(self.dFile, 'w') as fp:
            for i in range(len(self.aliveList)):
                fp.write(self.aliveList[i])


    def linkWithProxy(self, line):
        lineList = line.split('\t')
        protocol = lineList[2].lower()
        server = lineList[0] + ':' + lineList[1]
        proxy = {protocol:server}

        proxy_support = request.ProxyHandler(proxy)
        opener = request.build_opener(proxy_support)
        request.install_opener(opener)

        try:
            response = request.urlopen(self.URL, timeout=self.timeout)
        except:
            print('%s connect failed' %server)
        else:
            try:
                str = response.read().decode("utf-8")
            except:
                print('%s connect failed' %server)
                return

            if self.regex.search(str):
                print('%s connect success ... ...' %server)
                self.aliveList.append(line)




if __name__ == '__main__':
    TP = TestProxy()
