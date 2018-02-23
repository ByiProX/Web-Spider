# -*- coding: utf-8 -*-
import scrapy
from getProxy.items import GetproxyItem

class KuaidailispiderSpider(scrapy.Spider):
    name = 'kuaiDailiSpider'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['http://kuaidaili.com/free']

    def parse(self, response):
        subSelector = response.xpath('//div[@id="list"]/table//tbody/tr')
        items = []
        for sub in subSelector:
            item = GetproxyItem()
            item['ip'] = sub.xpath('./td[@data-title="IP"]/text()').extract()[0]
            item['port'] = sub.xpath('./td[@data-title="PORT"]/text()').extract()[0]
            item['protocol'] = sub.xpath('./td[@data-title="类型"]/text()').extract()[0]
            item['crypt'] = sub.xpath('./td[@data-title="匿名度"]/text()').extract()[0]
            item['location'] = sub.xpath('./td[@data-title="位置"]/text()').extract()[0]
            item['source'] = '快代理'
            items.append(item)
        return items
