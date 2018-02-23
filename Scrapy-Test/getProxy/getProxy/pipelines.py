# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GetproxyPipeline(object):
    def process_item(self, item, spider):
        fileName = 'proxy.txt'
        with open(fileName, 'a') as fp:
            fp.write(str(item['ip']) + '\t')
            fp.write(str(item['port']) + '\t')
            fp.write(str(item['protocol']) + '\t')
            fp.write(str(item['crypt']) + '\t')
            fp.write(str(item['location']) + '\t')
            fp.write(str(item['source']) + '\n')




        return item
