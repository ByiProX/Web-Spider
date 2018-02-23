# -*- coding: utf-8 -*-
import scrapy
from getProxy.items import GetproxyItem


class XicispiderSpider(scrapy.Spider):
    name = 'xiciSpider'
    allowed_domains = ['xicidaili.com']
    kinds = ['nn', 'nt', 'wn', 'wt']
    # kinds = ['nn']
    pages = 10 #暂时爬取20个页面
    start_urls =[]
    for kind in kinds:
        for i in range(1, pages+1):
            start_urls.append('http://www.xicidaili.com/' + kind + '/' + str(i))


    def parse(self, response):
        subSelector = response.xpath('//tr[@class=""]|//tr[@class="odd"]') # 使用逻辑表达式 '|'
        items =[]
        for sub in subSelector:
            item = GetproxyItem()
            item['ip'] = sub.xpath('./td[2]/text()').extract()[0]
            item['port'] = sub.xpath('./td[3]/text()').extract()[0]
            item['protocol'] = sub.xpath('./td[6]/text()').extract()[0]
            item['crypt'] = sub.xpath('./td[5]/text()').extract()[0]

            if sub.xpath('.//td[4]/a/text()'):
                item['location'] = sub.xpath('.//td[4]/a/text()').extract()[0].strip()
            else:
                item['location'] = sub.xpath('.//td[4]/text()').extract()[0].strip()

            item['source'] = '西刺代理'
            items.append(item)

        return items
