# -*- coding: utf-8 -*-
import scrapy
from todayMovie.items import TodaymovieItem


class BeijingmoviespiderSpider(scrapy.Spider):
    name = 'beiJingMovieSpider'
    allowed_domains = ['jycinema.com']
    start_urls = ['http://www.jycinema.com/html/default/index.html']

    def parse(self, response):
        subSelector = response.xpath('//div[@class="col-3"]')

        items = []
        for sub in subSelector:
            item = TodaymovieItem()
            item['movieName'] = sub.xpath('./div/a/span/text()').extract()
            items.append(item)
        return items
