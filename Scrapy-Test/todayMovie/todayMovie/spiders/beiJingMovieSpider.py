# -*- coding: utf-8 -*-
import scrapy


class BeijingmoviespiderSpider(scrapy.Spider):
    name = 'beiJingMovieSpider'
    allowed_domains = ['jycinema.com']
    start_urls = ['http://jycinema.com/']

    def parse(self, response):
        pass
