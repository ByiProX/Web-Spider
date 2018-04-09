# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BaiduNewsItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    writer = scrapy.Field()
    size = scrapy.Field()
    type = scrapy.Field()
    time = scrapy.Field()
    price_type = scrapy.Field()
    expected_price = scrapy.Field()
    real_price1 = scrapy.Field()
    real_price2 = scrapy.Field()
    real_price3 = scrapy.Field()
    real_price4 = scrapy.Field()
    real_price1_type = scrapy.Field()
    real_price2_type = scrapy.Field()
    real_price3_type = scrapy.Field()
    real_price4_type = scrapy.Field()
    special_performance = scrapy.Field()
    auction_time = scrapy.Field()
    auction_company = scrapy.Field()
    auction = scrapy.Field()
