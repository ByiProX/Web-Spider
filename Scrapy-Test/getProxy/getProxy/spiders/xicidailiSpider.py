# -*- coding: utf-8 -*-
import scrapy


class XicidailispiderSpider(scrapy.Spider):
    name = 'xicidailiSpider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://xicidaili.com/']

    def parse(self, response):
        pass
