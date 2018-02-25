# -*- coding: utf-8 -*-
import scrapy


class MeijuttspiderSpider(scrapy.Spider):
    name = 'meijuttSpider'
    allowed_domains = ['meijutt.com']
    start_urls = ['http://meijutt.com/']

    def parse(self, response):
        pass
