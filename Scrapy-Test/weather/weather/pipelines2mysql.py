# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb


class WeatherPipeline(object):
    def process_item(self, item, spider):
        cityName = item['cityName']
        week = item['week']
        weather = item['weather']
        air = item['air']
        img = item['img']

        conn = MySQLdb.connect(
        		host='localhost',
        		port=3306,
        		user='root',
        		passwd='root',
        		db='scrapyDB',
        		charset = 'utf8')
        cur = conn.cursor()
        cur.execute("INSERT INTO weather(cityName,week,weather,air,img) values(%s,%s,%s,%s,%s)", (cityName,week,weather,air,img))
        cur.close()
        conn.commit()
        conn.close()

        return item
