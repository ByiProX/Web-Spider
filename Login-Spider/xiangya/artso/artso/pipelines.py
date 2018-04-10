# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArtsoPipeline(object):
    def process_item(self, item, spider):
        fileName = 'xiangya.txt'
        with open(fileName, 'a') as fp:
            fp.write(str(item['name']) + '\t')
            fp.write(str(item['writer']) + '\t')
            fp.write(str(item['size']) + '\t')
            fp.write(str(item['type']) + '\t')
            fp.write(str(item['era']) + '\t')
            fp.write(str(item['url']) + '\n')

        return item
