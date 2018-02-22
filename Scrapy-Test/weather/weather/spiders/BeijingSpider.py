# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem


class BeijingspiderSpider(scrapy.Spider):
    name = 'BeijingSpider'
    allowed_domains = ['beijing.tianqi.com']
    # start_urls = ['http://beijing.tianqi.com/']
    citys = ['beijing', 'shanghai', 'weifang']
    start_urls = []
    for city in citys:
        start_urls.append('https://www.tianqi.com/' + city)

    def parse(self, response):
        subSelector = response.xpath('//dl[@class="weather_info"]')
        items = []
        for sub in subSelector:
            item =WeatherItem()
            item['img'] = sub.xpath('./dt/img/@src').extract()
            item['cityName'] = sub.xpath('./dd[@class="name"]/h2/text()').extract()
            item['week'] = sub.xpath('./dd[@class="week"]/text()').extract()

            weather = ''.join(sub.xpath('./dd[@class="weather"]/p//text()').extract()) + '  ' + \
                    ''.join(sub.xpath('./dd[@class="weather"]/span//text()').extract())
            item['weather'] = weather
            item['air'] = sub.xpath('./dd[@class="kongqi"]/h5//text()').extract()

            items.append(item)
        return items
