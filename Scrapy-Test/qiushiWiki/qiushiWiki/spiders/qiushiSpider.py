# -*- coding: utf-8 -*-
import scrapy
from qiushiWiki.items import QiushiwikiItem


class QiushispiderSpider(scrapy.Spider):
    name = 'qiushiSpider'
    allowed_domains = ['qiushibaike.com']
    start_urls = []
    for i in range(1,4):
        url = 'http://www.qiushibaike.com/hot/page/' + str(i) + '/'
        start_urls.append(url)

    def parse(self, response):
        subSelector = response.xpath('//div[starts-with(@class,"article block untagged mb15 typs_")]')
        items = []
        for sub in subSelector:
            item = QiushiwikiItem()
            item['author'] = sub.xpath('.//h2/text()').extract()[0]
            item['content'] = sub.xpath('.//div[@class="content"]/span/text()').extract()[0].strip()
            item['img'] = sub.xpath('.//div[@class="thumb"]//img/@src').extract()
            item['funNum'] = sub.xpath('.//i[@class="number"]/text()').extract()[0]
            try:
                item['talkNum'] = sub.xpath('.//i[@class="number"]/text()').extract()[1]
            except IndexError:
                item['talkNum'] = '0'
            items.append(item)
        return items
