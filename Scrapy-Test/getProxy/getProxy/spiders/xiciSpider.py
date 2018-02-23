# -*- coding: utf-8 -*-
import scrapy
from getProxy.items import GetproxyItem


class XicispiderSpider(scrapy.Spider):
    name = 'xiciSpider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://xicidaili.com/']

    def parse(self, response):
