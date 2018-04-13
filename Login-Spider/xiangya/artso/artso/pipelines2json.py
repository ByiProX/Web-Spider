# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
import codecs

class WeatherPipeline(object):
    def process_item(self, item, spider):
        fileName = xiangyaAuction + '.json'
        with codecs.open(fileName, 'a', encoding='utf-8') as fp:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            fp.write(line)

        return item
