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
    era = scrapy.Field()
    expected_price = scrapy.Field()

    real_priceRMB = scrapy.Field()
    real_priceHKB = scrapy.Field()
    real_priceUSD = scrapy.Field()
    real_priceEUR = scrapy.Field()

    special_performance = scrapy.Field()
    auction_time = scrapy.Field()
    auction_company = scrapy.Field()
    auction = scrapy.Field()
    url = scrapy.Field()
