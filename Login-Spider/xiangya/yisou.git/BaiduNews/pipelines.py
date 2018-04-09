# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class BaidunewsPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='101.251.222.234',
            db='doododData',
            user='developer',
            passwd='developer',
            charset='utf8',
            port=3306)

        self.cursor = self.connect.cursor()

    def process_item(self , item , spider):

        try:
            self.cursor.execute(
                """select * from auction_xiangya2 where url = %s""",
                [item['url']])
            # 是否有重复数据
            repetition = self.cursor.fetchone()
            # 重复
            if repetition:
                pass
            else:
                self.cursor.execute("""insert into auction_xiangya2(name,url,writer,size,type,time,price_type,expected_price,real_price1,real_price2,real_price3,real_price4,real_price1_type,real_price2_type,real_price3_type,real_price4_type,special_performance,auction_time,auction_company,auction) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(item["name"], item["url"], item["writer"], item["size"], item["type"], item["time"], item["price_type"], item["expected_price"], item["real_price1"], item["real_price2"], item["real_price3"], item["real_price4"], item["real_price1_type"], item["real_price2_type"], item["real_price3_type"], item["real_price4_type"], item["special_performance"], item["auction_time"], item["auction_company"], item["auction"]))

            self.connect.commit()
        except Exception as error:
            print(error)
        return item
