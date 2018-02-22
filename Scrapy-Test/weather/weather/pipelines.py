# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import os.path
import urllib

class WeatherPipeline(object):
    def process_item(self, item, spider):
        today = time.strftime('%Y%m%d', time.localtime())
        fileName = today + '.txt'
        with open(fileName, 'a') as fp:
            fp.write(str(item['cityName'][0]) + '\t')
            fp.write(str(item['week'][0]) + '\t')
            fp.write(str(item['weather'][0]) + '\t')
            fp.write(str(item['air'][0]) + '\n\n')

        return item
