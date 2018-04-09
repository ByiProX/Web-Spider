# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import time
import re
from BaiduNews.items import BaiduNewsItem

def data(year,mouth,day):

    a = year + '-' + mouth + '-' + day +' ' +'00:00:00'

    # 将其转换为时间数组
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")

    # 转换为时间戳
    start_time = int(time.mktime(timeArray))
    #end_time = start_time + 2483600 - 1

    return start_time

start_urls = ["http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&Status=0&ClassCode=020800000000&ArtistName=&OrganCode=&StartDate=&EndDate=&listtype=0&order=&EvaluationType=0&Estartvalue=&Eendvalue=&Sstartvalue=&Sendvalue=&page=1"]

cookies = {
    'ALLYESID4':'0F79003EC1E69583','gr_user_id':'be05d6dd-f7a9-4653-a76d-a84350f0525a','growingio_2436986':'var+_giuser+%3D+%7B%0A%09%09uid%3A+%222436986%22%2C+gender%3A+%22%E6%9C%AA%E7%9F%A5%22%2C+source%3A+%221%22%2C+date%3A+%222018-03-24%22%0A%09%7D%3B','artron_67ae_saltkey':'zLJU9Qkk','artron_67ae_lastvisit':'1521859918','artron_auth':'7cd8MTBphajzI2PKMqRRxcWvCOlqycqOEipyqkz9gU9JhL70hgOZh0otil3tURk5ZyYH7NK4ygaj3%2FTQkt%2FssU6fYWZf','artron_loginuser':'%E5%93%91%E6%A2%A2%E5%85%AC92','gr_session_id_276fdc71b3c353173f111df9361be1bb':'8ecdac8b-1322-4f04-a0bb-82720c585e8d','Hm_lvt_851619594aa1d1fb8c108cde832cc127':'1521878512,1521879678,1521881433,1523242758','_at_pt_0_':'2436986','_at_pt_1_':'%E5%93%91%E6%A2%A2%E5%85%AC92','_at_pt_2_':'e62c47543e02faa7638cd4da7b1920b8','artron_67ae_sid':'QcXc7d','artron_67ae_creditnotice':'0D1D0D0D0D0D0D0D0D2238045','artron_67ae_creditbase':'0D0D0D0D0D0D0D0D0','artron_67ae_creditrule':'%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95','artron_67ae_lastact':'1523244321%09uc.php%09','artron_67ae_auth':'a7964Z1W47UtDRjleZZ3KMTy8pNa7%2BCNgEl%2FvQE5lojs%2FmhWh3TI8CpCGkgVoIJiEkJe%2BoL%2FAap4GBrihxbgmp%2BaPYY2','gr_cs1_8ecdac8b-1322-4f04-a0bb-82720c585e8d':'user_id%3A2436986','Hm_lpvt_851619594aa1d1fb8c108cde832cc127':'1523244309'
}
headers = {
'User-Agent':"Mozilla/5.0 (Windows NT 6.1;WOW64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"
}

class BaiduNewsSpider(scrapy.Spider):
    name = "BaiduNews"
    allowed_domains = ["artron.net"]
    start_urls = start_urls
    url_num = 0
    data_num = 0
    expected_data_num = 0

    def parse(self, response):
        self.url_num = self.url_num + 1
        print('正在爬取第' + str(self.url_num) + '个网址')
        Soup = BeautifulSoup(response.text, 'lxml')
        nlistImgs = Soup.find(attrs={'class': 'listImg'})
        nlistImgs = nlistImgs.ul
        for nlistImg in nlistImgs:
            try:
                item = BaiduNewsItem()
                print(nlistImg.h3.get_text())
                item['name'] = nlistImg.h3.get_text()[1:-1]
                item['url'] = nlistImg.h3.a['href']
                self.expected_data_num += 1
                yield response.follow(nlistImg.h3.a['href'],meta={'item':item}, callback=self.parse2, headers=headers, cookies=cookies)
            except:
                pass

            # self.data_num = self.data_num + 1
            #
            # print('新闻id：' + str(self.data_num))
            # print('标题为：' + i.find('a').get_text())
            # print('来源网址：' + i.find('a')['href'])
            # print('来源：' + source.group(0)[0:-1])
            # print('时间：' + times)
            # print('描述：' + content)
        try:
            if self.url_num < 450:
                next_url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&Status=0&ClassCode=020800000000&ArtistName=&OrganCode=&StartDate=2008-01-01&EndDate=&listtype=0&order=&EvaluationType=0&Estartvalue=&Eendvalue=&Sstartvalue=&Sendvalue=&page=' + str(self.url_num+1)
                yield response.follow(next_url, callback=self.parse, headers=headers, cookies=cookies)
            else:
                pass
        except:
            pass
        time.sleep(1)
        #filename = soup.get_text()
        #with open(filename, 'wb') as f:
            #f.write(response.body)

    def parse2(self, response):
        Soup = BeautifulSoup(response.text, 'lxml')
        try:
            info = Soup.find('table').get_text()
            writer = re.search(r'作者\n.*\n.*', info).group(0)
            try:
                writer = re.search(r'  .*', writer).group(0)[2:]
            except:
                writer = ''
            size = re.search(r'尺寸\n.*', info).group(0)
            size = re.search(r'\n.*', size).group(0)[1:]
            type = re.search(r'作品分类\n.*', info).group(0)
            type = re.search(r'\n.*', type).group(0)[1:]
            time = re.search(r'创作年代\n.*', info).group(0)
            time = re.search(r'\n.*', time).group(0)[1:]
            try:
                expected_price = re.search(r'估价\n.*\n.*\n.*', info).group(0)
                price_type = re.search(r'\t\n\t.*', expected_price).group(0)[3:6]
                expected_price = re.search(r'\t\n\t.*', expected_price).group(0)[8:]
            except:
                price_type = ''
                expected_price = '无底价'
            try:
                real_price = re.search(r'成交价\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n', info).group(0)
                print(real_price)
                real_price1 = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[0][5:]
                real_price1_type = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[0][:3]
                print('1')
                real_price2 = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[1][5:]
                real_price2_type = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[1][:3]
                print('2')
                real_price3 = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[2][5:]
                real_price3_type = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[2][:3]
                print('3')
                real_price4 = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[3][5:]
                real_price4_type = re.findall(r'[A-Z]{3} 　[0-9,\,]*', real_price)[3][:3]
                print('4')
            except Exception as e:
                print('zxcvbn',e)
                real_price1 = ''
                real_price2 = ''
                real_price3 = ''
                real_price4 = ''
                real_price1_type = ''
                real_price2_type = ''
                real_price3_type = ''
                real_price4_type = ''
            special_performance = re.search(r'专场\n.*', info).group(0)
            special_performance = re.search(r'\n.*', special_performance).group(0)[1:]
            auction_time = re.search(r'拍卖时间\n.*', info).group(0)
            auction_time = re.search(r'\n.*', auction_time).group(0)[1:]
            auction_company = re.search(r'拍卖公司\n.*', info).group(0)
            auction_company = re.search(r'\n.*', auction_company).group(0)[1:]
            auction = re.search(r'拍卖会\n.*', info).group(0)
            auction = re.search(r'\n.*', auction).group(0)[1:]

            # print('作者：',writer)
            # print('尺寸：', size)
            # print('作品分类：', type)
            # print('创作年代：', time)
            # print('预估价格币种：', price_type)
            # print('估价：', expected_price)
            print('成交价：!!!!!!!!!!!!!!!',real_price1,real_price2,real_price3,real_price4,real_price1_type,real_price2_type,real_price3_type,real_price4_type)
            # print('专场：', special_performance)
            # print('拍卖时间：', auction_time)
            # print('拍卖公司：', auction_company)
            # print('拍卖会：', auction)
            item = response.meta['item']
            item['writer'] = writer
            item['size'] = size
            item['type'] = type
            item['time'] = time
            item['price_type'] = price_type
            item['expected_price'] = expected_price
            item['real_price1'] = real_price1
            item['real_price2'] = real_price2
            item['real_price3'] = real_price3
            item['real_price4'] = real_price4
            item['real_price1_type'] = real_price1_type
            item['real_price2_type'] = real_price2_type
            item['real_price3_type'] = real_price3_type
            item['real_price4_type'] = real_price4_type
            item['special_performance'] = special_performance
            item['auction_time'] = auction_time
            item['auction_company'] = auction_company
            item['auction'] = auction
            self.data_num += 1
            print('爬取数据：', str(self.data_num))
            print('预计数据：', str(self.expected_data_num))
            yield item
        except:
            self.data_num += 1
            print('？？？？？？？？',self.data_num)




