# -*- coding: utf-8 -*-
import scrapy


class XiushispiderSpider(scrapy.Spider):
    name = 'xiushiSpider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['http://qiushibaike.com/']

    def parse(self, response):
        pass
