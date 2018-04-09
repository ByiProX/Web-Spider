# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtsoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    writer = scrapy.Field()
    size = scrapy.Field()
    type = scrapy.Field()
    time = scrapy.Field()
    expected_price = scrapy.Field()

    real_price1 = scrapy.Field()
    real_price2 = scrapy.Field()
    real_price3 = scrapy.Field()
    real_price4 = scrapy.Field()

    special_performance = scrapy.Field()
    auction_time = scrapy.Field()
    auction_company = scrapy.Field()
    auction = scrapy.Field()
    url = scrapy.Field()
