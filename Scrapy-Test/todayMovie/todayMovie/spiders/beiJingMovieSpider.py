# -*- coding: utf-8 -*-
import scrapy
from todayMovie.items import TodaymovieItem


class BeijingmoviespiderSpider(scrapy.Spider):
    name = 'beiJingMovieSpider'
    allowed_domains = ['dianying.taobao.com']
    start_urls = ['https://dianying.taobao.com/']

    def parse(self, response):
        subSelector = response.xpath('//div[@class="movie-card-name"]')

        items = []
        for sub in subSelector:
            item = TodaymovieItem()
            item['movieName'] = sub.xpath('./span[@class="bt-l"]/text()').extract()
            items.append(item)
        return items
