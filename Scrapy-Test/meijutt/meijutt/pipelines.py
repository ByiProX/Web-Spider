# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

class MeijuttPipeline(object):
    def process_item(self, item, spider):
        today = time.strftime('%Y%m%d', time.localtime())
        fileName = today + 'meiju.txt'
        with open(fileName, 'a') as fp:
            fp.write('%-20s' %(item['storyName']))
            fp.write('%-15s' %(item['storyState']))
            fp.write('%-15s' %(item['tvStation']))
            fp.write('%s \n' %(item['updateTime']))


        return item
