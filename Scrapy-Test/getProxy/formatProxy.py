class ProxyFormat(object):
    """docstring for TestProxy."""
    def __init__(self):
        self.sFile = 'aliveProxy.txt'
        self.dFile = 'proxy4use.py'
        self.run()

    def run(self):
        proxiesList = []
        with open(self.sFile, 'r') as fp:
            lines = fp.readlines()
            line = lines.pop()
            while lines:
                lineList = line.split('\t')
                protocol = lineList[2].lower()
                server = lineList[0] + ':' + lineList[1]
                proxy = protocol+ '://' + server
                proxiesList.append(proxy)
                line = lines.pop()

        with open(self.dFile, 'w') as fp:
            fp.write('PROXIES = [ \n')
            for i in proxiesList:
                fp.write("'" + i + "'" + ',' + '\n')
            fp.write(']')



if __name__ == '__main__':
    PF = ProxyFormat()
