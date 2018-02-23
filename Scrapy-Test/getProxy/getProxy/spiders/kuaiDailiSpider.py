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
            item = GetproxyItem
            for i in sub:
                item['ip'] = i.xpath('./td[@data-title="IP"]/text()').extract()
                item['port'] = i.xpath('./td[@data-title="PORT"]/text()').extract()
                item['protocol'] = i.xpath('./td[@data-title="类型"]/text()').extract()
                item['crypt'] = i.xpath('./td[@data-title="匿名度"]/text()').extract()
                item['location'] = i.xpath('./td[@data-title="位置"]/text()').extract()
                item['source'] = '快代理'

        return items
