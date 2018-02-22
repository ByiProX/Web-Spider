# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cityName = scrapy.Field()
    week = scrapy.Field()
    weather = scrapy.Field()
    air = scrapy.Field()
    img = scrapy.Field()
