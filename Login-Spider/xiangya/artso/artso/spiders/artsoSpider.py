# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from artso.items import ArtsoItem
from bs4 import BeautifulSoup
from lxml import etree


class ArtsospiderSpider(scrapy.Spider):
    name = 'artsoSpider'
    allowed_domains = ['artso.artron.net']
    # start_urls = ['http://artso.artron.net/']
    # start_urls = ['http://artso.artron.net/auction/search_auction.php?keyword=象牙']
    start_urls = []
    for i in range(1,11):
        url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&Status=0&ClassCode=&ArtistName=&OrganCode=&StartDate=&EndDate=&listtype=0&order=&EvaluationType=0&Estartvalue=&Eendvalue=&Sstartvalue=&Sendvalue=&page=1' +\
        str(i) + '/'
        start_urls.append(url)

    def parse(self, response):
        subSelector = response.xpath('//div[@class="listImg"]/ul/li')

        items = []
        for sub in subSelector:
            item = ArtsoItem()
            innerURL = sub.xpath('./div/a/@href').extract()[0]
            item['url'] = innerURL

            head = {}
            #写入User Agent信息
            head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
            #创建Request对象
            req = request.Request(innerURL, headers=head)
            #传入创建好的Request对象
            res = request.urlopen(req)
            context = res.read().decode('utf-8')
            soup = BeautifulSoup(context,'lxml')

            selector = etree.HTML(str(soup))
            item['name'] = selector[0].xpath('//div[@class="titLeft"]/h1/text()')[0].strip()
            item['writer'] = selector[0].xpath('//tr[1]/td[1]/text()')[0].strip()
            item['size'] = selector[0].xpath('//tr[1]/td[2]//text()')[0].strip()
            item['type'] = selector[0].xpath('//tr[2]/td[1]//text()')[0].strip()
            item['time'] = selector[0].xpath('//tr[2]/td[2]//text()')[0].strip()
            item['expected_price'] = ' '.join(selector[0].xpath('//tr[3]/td[1]//text()')[1].strip().split())

            item['real_price1'] = ''
            item['real_price2'] = ''
            item['real_price3'] = ''
            item['real_price4'] = ''

            item['special_performance'] =
            item['auction_time'] =
            item['auction_company'] =
            item['auction'] =


            items.append(item)
        return items
