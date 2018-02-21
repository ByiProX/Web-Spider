# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

class TodaymoviePipeline(object):
    def process_item(self, item, spider):
        now = time.strftime('%Y-%m-%d', time.localtime())
        fileNme = 'Beijng' + now + '.txt'
        with open(fileNme, 'a') as fp:
            fp.write(item['movieName'][0].encode('utf-8') + '\n\n')
        return item
