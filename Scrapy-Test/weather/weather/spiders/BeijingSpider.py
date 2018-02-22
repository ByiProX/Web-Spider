# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem


class BeijingspiderSpider(scrapy.Spider):
    name = 'BeijingSpider'
    allowed_domains = ['beijing.tianqi.com']
    # start_urls = ['http://beijing.tianqi.com/']
    citys = ['beijing', 'shanghai']
    start_urls = []
    for city in citys:
        start_urls.append('https://www.tianqi.com/' + city)

    def parse(self, response):
        subSelector = response.xpath('//dl[@class="weather_info"')
        items = []
        for sub in subSelector:
            item =WeatherItem()
            item['cityName'] = sub.xpath('./dd[@class="name"]/h2/text()')
            item['week'] = sub.xpath('./dd[@class="week"]/text()')

            weather = sub.xpath('./dd[@class="weather"]/p//text()') + \
                    sub.xpath('./dd[@class="weather"]/span//text()')
            item['weather'] = weather
            item['air'] = sub.xpath('./dd[@class="kongqi"]/h5//text()')
            items.append(item)
        return items
