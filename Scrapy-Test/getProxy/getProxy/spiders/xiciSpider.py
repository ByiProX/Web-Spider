# -*- coding: utf-8 -*-
import scrapy
from getProxy.items import GetproxyItem


class XicispiderSpider(scrapy.Spider):
    name = 'xiciSpider'
    allowed_domains = ['xicidaili.com']
    # start_urls = ['http://xicidaili.com/']
    kinds = ['nn', 'nt', 'wn', 'wt']
    pages = 20 #暂时爬取20个页面
    start_urls =[]
    for kind in kinds:
        for i in range(1, pages+1):
            start_urls.append('http://xicidaili.com/' + kind + '/' + str(i))


    def parse(self, response):
