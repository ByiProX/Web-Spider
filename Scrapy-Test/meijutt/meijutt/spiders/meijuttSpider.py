# -*- coding: utf-8 -*-
import scrapy
from meijutt.items import MeijuttItem


class MeijuttspiderSpider(scrapy.Spider):
    name = 'meijuttSpider'
    allowed_domains = ['meijutt.com']
    start_urls = ['http://www.meijutt.com/new100.html']

    def parse(self, response):
        subSelector = response.xpath('//div[@class="top-min top-min-long new100"]')

        items = []
        for sub in subSelector:
            item = MeijuttItem()

            item['storyName'] = sub.xpath('.//li/h5//text()').extract()[0]
            item['storyState'] = sub.xpath('.//span[@class="state1 new100state1"]/text()').extract()[0]
            item['tvStation'] = sub.xpath('.//span[@class="mjtv"]/text()').extract()[0]
            item['updateTime'] = sub.xpath('.//span[@class="lasted-time new100time fn-right"]/text()').extract()[0]

            items.append(item)
        return items
