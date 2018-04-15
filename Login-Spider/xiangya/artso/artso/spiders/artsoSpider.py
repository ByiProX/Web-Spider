# -*- coding: utf-8 -*-
import scrapy
import time
import re
from urllib import request
from artso.items import ArtsoItem
from bs4 import BeautifulSoup
from lxml import etree
from random import randrange
from .myLogging import MyLogging
from artso.CookieResources import Cookies
from random import choice

LOG = MyLogging()


class ArtsospiderSpider(scrapy.Spider):
    name = 'artsoSpider'
    allowed_domains = ['artso.artron.net']
    # 此处可以优化，以后再说
    start_urls = []
    for i in range(5, 201):
        url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&Status=0&ClassCode=&ArtistName=&OrganCode=&StartDate=&EndDate=&listtype=0&order=&EvaluationType=0&Estartvalue=&Eendvalue=&Sstartvalue=&Sendvalue=&page=' + \
               str(i) + '/'
        start_urls.append(url)

    # LOG.warning('当前正在爬取的网页页码为第%d页' %i)

    def parse(self, response):
        innerPageNum = 0
        subSelector = response.xpath('//div[@class="listImg"]/ul/li')

        while True:
            items = []
            for sub in subSelector:
                item = ArtsoItem()
                try:
                    innerURL = sub.xpath('./div/a/@href').extract()[0]
                    innerPageNum += 1
                except IndexError:
                    continue
                item['url'] = innerURL

                print('正在爬取当前页面中的第%d个网址 %s' %(innerPageNum,innerURL))

                head = {}
                #写入User Agent信息
                head['Referer'] = 'http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&page=' + str(randrange(100))
                head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
                # head['Cookie'] = 'gsScrollPos-1276=0; tulu_pop=1; Hm_lvt_851619594aa1d1fb8c108cde832cc127=1523465820; artron_67ae_saltkey=G4smTtVQ; artron_67ae_lastvisit=1523462228; artron_loginuser=%E7%8E%8B%E5%9D%A4%E7%A5%A5; _at_pt_0_=2446806; _at_pt_1_=%E7%8E%8B%E5%9D%A4%E7%A5%A5; _at_pt_2_=314a3bb686fc0a54947b5b28ca495680; artron_67ae_sid=ylg5RB; artron_67ae_lastact=1523468001%09uc.php%09; artron_67ae_auth=989eh1%2BzHnhY3UpkSJMF5LxuIjnUSOBuhq6zJrqG5h3zRkpHZ7SwHlRqzsyJgjX4sSySmAg2bqHFq4cx6guUEVGXeIIH; artron_auth=8781oe5hdToWYvQy%2FRe0WDjAV8CaLbGNxY6pFOeNeJPMDB9PG610fKUrVKr4O1W217geSLqdUOGENIK%2F6lRkzXW2zxXj; growingio_2446806=var+_giuser+%3D+%7B%0A%09%09uid%3A+%222446806%22%2C+gender%3A+%22%E6%9C%AA%E7%9F%A5%22%2C+source%3A+%221%22%2C+date%3A+%222018-04-09%22%0A%09%7D%3B; gr_user_id=6f425c58-a8f5-4ef7-ab6d-b9243a0dcc53; Hm_lpvt_851619594aa1d1fb8c108cde832cc127=1523499477'
                head['Cookie'] = choice(Cookies)

                #创建Request对象
                req = request.Request(innerURL, headers=head)
                #传入创建好的Request对象
                res = request.urlopen(req)
                context = res.read().decode('utf-8')
                soup = BeautifulSoup(context, 'lxml')

                selector = etree.HTML(str(soup))
                item['name'] = selector[0].xpath('//div[@class="titLeft"]/h1/text()')[0].strip()
                item['writer'] = selector[0].xpath('//tr[1]/td[1]/text()')[0].strip()
                item['size'] = selector[0].xpath('//tr[1]/td[2]//text()')[0].strip()
                item['type'] = selector[0].xpath('//tr[2]/td[1]//text()')[0].strip()
                item['era'] = selector[0].xpath('//tr[2]/td[2]//text()')[0].strip()
                item['expected_price'] = ' '.join(selector[0].xpath('//tr[3]/td[1]//text()')[1].strip().split())

                if selector[0].xpath('//tr[4]/th[1]//text()')[0].strip() == '专场':
                    item['real_priceRMB'] = '--'
                    item['real_priceHKD'] = '--'
                    item['real_priceUSD'] = '--'
                    item['real_priceEUR'] = '--'

                    item['special_performance'] = selector[0].xpath('//tr[4]/td[1]/a//text()')[0].strip()
                    item['auction_time'] = selector[0].xpath('//tr[4]/td[2]//text()')[0].strip()
                    item['auction_company'] = selector[0].xpath('//tr[5]/td[1]//text()')[0].strip()
                    item['auction'] = selector[0].xpath('//tr[5]/td[2]//text()')[0].strip()

                elif selector[0].xpath('//tr[4]/th[1]//text()')[0].strip() == '成交价':
                    target = selector[0].xpath('//tr[4]/td[1]/ul/li[1]/text()')[0].strip()
                    if target in ['未提供', '流标', '流拍']:
                        item['real_priceRMB'] = target
                        item['real_priceHKD'] = target
                        item['real_priceUSD'] = target
                        item['real_priceEUR'] = target

                        item['special_performance'] = selector[0].xpath('//tr[5]/td[1]/a//text()')[0].strip()
                        item['auction_time'] = selector[0].xpath('//tr[5]/td[2]//text()')[0].strip()
                        item['auction_company'] = selector[0].xpath('//tr[6]/td[1]//text()')[0].strip()
                        item['auction'] = selector[0].xpath('//tr[6]/td[2]//text()')[0].strip()
                    else:
                        try:
                            item['real_priceRMB'] = selector[0].xpath('//tr[4]/td/ul/li[1]/text()')[0].strip()
                        except:
                            item['real_priceRMB'] = '--'

                        try:
                            item['real_priceHKD'] = selector[0].xpath('//tr[4]/td/ul/li[2]/text()')[0].strip()
                        except:
                            item['real_priceHKD'] = '--'

                        try:
                            item['real_priceUSD'] = selector[0].xpath('//tr[4]/td/ul/li[3]/text()')[0].strip()
                        except:
                            item['real_priceUSD'] = '--'

                        try:
                            item['real_priceEUR'] = selector[0].xpath('//tr[4]/td/ul/li[4]/text()')[0].strip()
                        except:
                            item['real_priceEUR'] = '--'

                        try:
                            item['special_performance'] = selector[0].xpath('//tr[5]/td[1]/a//text()')[0].strip()
                        except:
                            item['special_performance'] = '--'

                        try:
                            item['auction_time'] = selector[0].xpath('//tr[5]/td[2]//text()')[0].strip()
                        except:
                            item['auction_time'] = '--'

                        try:
                            item['auction_company'] = selector[0].xpath('//tr[6]/td[1]//text()')[0].strip()
                        except:
                            item['auction_company'] = '--'

                        try:
                            item['auction'] = selector[0].xpath('//tr[6]/td[2]//text()')[0].strip()
                        except:
                            item['auction'] = '--'

                items.append(item)
                time.sleep(2)
                LOG.warning(str(innerPageNum) + '  ' + str(req.full_url) + '  ' + str(res.status))

            if len(items) == 40:
                break

        time.sleep(0.02)
        return items
