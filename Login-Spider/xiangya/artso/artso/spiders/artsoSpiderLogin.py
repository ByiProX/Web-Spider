# -*- coding: utf-8 -*-
import scrapy
import time
from urllib import request
from artso.items import ArtsoItem
from bs4 import BeautifulSoup
from lxml import etree
from random import randrange

class ArtsospiderloginSpider(scrapy.Spider):
    name = 'artsoSpiderLogin'
    # allowed_domains = ['artso.artron.net']
    # start_urls = ['https://passport.artron.net/login']

    def start_request(self, response):
        return scrapy.Request('https://passport.artron.net/login', callback = self.post_login)

    def post_login(self, response):
        print('start login')
        return scrapy.FormRequest.from_response(
            response,
            meta = {'cookiejar' : 1},
            formdata = {'account': '17888816733', 'passwd': 'doodo123456789'},
            callback = self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in str(response.body):
            # self.logger.error("Login failed")
            print("Login failed")
            return

        # continue scraping with authenticated session...
        else:
            for i in range(4,5):
                url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&Status=0&ClassCode=&ArtistName=&OrganCode=&StartDate=&EndDate=&listtype=0&order=&EvaluationType=0&Estartvalue=&Eendvalue=&Sstartvalue=&Sendvalue=&page=' + \
                       str(i) + '/'
                yield scrapy.Request(
                                url=url,
                                meta={'cookiejar': response.meta['cookiejar']},
                                callback=self.parse_tastypage
                                )

    def parse_tastypage(self, response):
        subSelector = response.xpath('//div[@class="listImg"]/ul/li')

        items = []
        for sub in subSelector:
            item = ArtsoItem()
            try:
                innerURL = sub.xpath('./div/a/@href').extract()[0]
            except IndexError:
                continue
            item['url'] = innerURL

            head = {}
            #写入User Agent信息
            # head['Referer'] = 'http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&page=' + str(randrange(100))
            head['Referer'] = 'www.baidu.com'
            head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
            #创建Request对象
            req = request.Request(innerURL, meta={'cookiejar': response.meta['cookiejar']}, headers=head)
            #传入创建好的Request对象
            res = request.urlopen(req)
            context = res.read().decode('utf-8')
            soup = BeautifulSoup(context,'lxml')

            selector = etree.HTML(str(soup))
            item['name'] = selector[0].xpath('//div[@class="titLeft"]/h1/text()')[0].strip()
            item['writer'] = selector[0].xpath('//tr[1]/td[1]/text()')[0].strip()
            item['size'] = selector[0].xpath('//tr[1]/td[2]//text()')[0].strip()
            item['type'] = selector[0].xpath('//tr[2]/td[1]//text()')[0].strip()
            item['era'] = selector[0].xpath('//tr[2]/td[2]//text()')[0].strip()
            item['expected_price'] = ' '.join(selector[0].xpath('//tr[3]/td[1]//text()')[1].strip().split())

            if selector[0].xpath('//tr[4]/th[1]//text()')[0].strip() == '成交价':
                print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                if selector[0].xpath('//tr[4]/td[1]//text()')[0].strip() in ['未提供', '流标']:
                    print('++++++++++++++++++++++')
                    item['real_priceRMB'] = item['real_priceHKD'] = item['real_priceUSD'] = item['real_priceEUR'] = selector[0].xpath('//tr[4]/td[1]//text()')[0].strip()

                else:
                    # item['real_priceRMB'] = selector[0].xpath('//tr[4]/td[1]//li[1]/text()')[0].strip()
                    # item['real_priceHKD'] = selector[0].xpath('//tr[4]/td[1]//li[2]/text()')[0].strip()
                    # item['real_priceUSD'] = selector[0].xpath('//tr[4]/td[1]//li[3]/text()')[0].strip()
                    # item['real_priceEUR'] = selector[0].xpath('//tr[4]/td[1]//li[4]/text()')[0].strip()

                    item['real_priceRMB']= ''
                    item['real_priceHKD']=  ''
                    item['real_priceUSD']=''
                    item['real_priceEUR']=''


            item['special_performance'] = ''
            item['auction_time'] = ''
            item['auction_company'] = ''
            item['auction'] = ''

            items.append(item)
            # time.sleep(0.05)
        return items
