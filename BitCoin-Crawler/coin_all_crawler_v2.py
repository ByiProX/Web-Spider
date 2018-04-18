# -*- coding: utf-8 -*-
import json

from bs4 import BeautifulSoup
import requests
import re

import logging
from datetime import datetime

from configs.config import db, GLOBAL_RULES_UPDATE_FLAG, GLOBAL_MATCHING_DEFAULT_RULES_UPDATE_FLAG, \
    Coin
from crawler.usdcny import dollar_currency_rate
from models_v2.base_model import CM, BaseModel
from utils.u_time import datetime_to_timestamp_utc_8
from utils.u_transformat import str_to_decimal

logger = logging.getLogger('main')

Cookie = {
    '__cfduid': 'd6a59731e0ff904a2a262055ed2c2840b1520396422',
    '__gads': 'ID=5a810cac25d50aaf:T=1520396439:S=ALNI_Ma9JciRiblSK4ouIgRnguAFchMk_Q',
    '_ga': 'GA1.2.2011694192.1520396436',
    '_gid': 'GA1.2.353732978.1520396436',
    'gtm_session_first': 'Wed%20Mar%2007%202018%2012:22:24%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)',
    'gtm_session_last': 'Wed%20Mar%2007%202018%2012:22:24%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)',

}
Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}

Url = "https://coinmarketcap.com/all/views/all/#"


def get_coin_all():
    result = requests.get(Url, headers = Headers, cookies = Cookie)
    Soup = BeautifulSoup(result.text, 'html.parser')
    priority = 0
    start_time = datetime.now()
    coin_list = list()
    for i in Soup.find_all('tr'):
        coin = dict()
        if priority > 0:
            # print "优先级：", str(priority)
            xx = 0
            for ii in i.children:
                xx += 1
                if xx == 4:
                    # print "coin_name:", ii["data-sort"]
                    coin['coin_name'] = ii["data-sort"]
                    coin_id = re.search(r'\d+', ii.div["class"][0]).group(0)
                    # print 'coin_icon:', 'https://s2.coinmarketcap.com/static/img/coins/16x16/' + coin_id + '.png'
                    coin['coin_icon'] = 'https://s2.coinmarketcap.com/static/img/coins/16x16/' + coin_id + '.png'
                if xx == 6:
                    # print "symbol:", ii.get_text()
                    coin['symbol'] = ii.get_text()
                if xx == 8:
                    if ii['data-usd'] == '?':
                        # print "marketcap:", '0'
                        coin['marketcap'] = 0
                    else:
                        # print "marketcap:", ii['data-usd']
                        coin['marketcap'] = ii['data-usd']
                if xx == 10:
                    if ii.a['data-usd'] == '?':
                        # print "price:", '0'
                        coin['price'] = 0
                    else:
                        # print "price:", ii.a["data-usd"]
                        coin['price'] = ii.a["data-usd"]
                if xx == 12:
                    try:
                        re.search(r'\*', ii.get_text())
                        # print 'Mineable:', '0'
                        coin['Mineable'] = 0
                    except:
                        # print 'Mineable:', '1'
                        coin['Mineable'] = 1
                    try:
                        if ii.a.get_text() == '?':
                            # print "available_supply:", '0'
                            coin['available_supply'] = 0
                        else:
                            # print "available_supply:", ii.a.get_text()
                            coin['available_supply'] = ii.a['data-supply']
                    except:
                        if ii.span.get_text() == '?':
                            # print "available_supply:", '0'
                            coin['available_supply'] = 0
                        else:
                            # print "available_supply:", ii.span.get_text()
                            coin['available_supply'] = ii.span['data-supply']
                if xx == 14:
                    if ii.a.get_text() == '?':
                        # print "volume_ex:", '0'
                        coin['volume_ex'] = 0
                    else:
                        # print "volume_ex:", ii.a.get_text()
                        coin['volume_ex'] = ii.a['data-usd']
                if xx == 16:
                    if ii.get_text() == '?':
                        # print "change1h:", '0'
                        coin['change1h'] = 0
                    else:
                        # print "change1h:", ii.get_text()
                        coin['change1h'] = ii['data-sort']
                if xx == 18:
                    if ii.get_text() == '?':
                        # print "change1d:", '0'
                        coin['change1d'] = 0
                    else:
                        # print "change1d:", ii.get_text()
                        coin['change1d'] = ii['data-sort']
                if xx == 20:
                    if ii.get_text() == '?':
                        # print "change7d:", '0'
                        coin['change7d'] = 0
                    else:
                        # print "change7d:", ii.get_text()
                        coin['change7d'] = ii['data-sort']
            if not (coin.get('volume_ex') and coin.get('marketcap')):
                # 市值和流通盘都没有
                coin['priority'] = 0
                coin['is_integral'] = 0
            else:
                coin['priority'] = priority
                coin['is_integral'] = 1
                priority += 1
            coin_list.append(coin.copy())
        if priority == 0:
            priority += 1
    # print 'coin crawler done', (datetime.now() - start_time)
    return coin_list


def update_coin_all():
    coin_list = get_coin_all()
    usdcny_str = dollar_currency_rate()
    usdcny = str_to_decimal(usdcny_str)
    new_coin_dict = dict()
    for coin_json in coin_list:
        symbol = coin_json.get(u'symbol', u'').upper()
        priority = coin_json.get(u'priority', u'')
        coin_name = coin_json.get(u'coin_name', u'')
        coin_icon = coin_json.get(u'coin_icon', u'')
        is_integral = coin_json.get(u'is_integral', 0)
        marketcap = (str_to_decimal(str(coin_json.get(u'marketcap'))) * usdcny).to_eng_string()
        price = (str_to_decimal(str(coin_json.get(u'price'))) * usdcny).to_eng_string()
        mineable = coin_json.get(u'Mineable')
        available_supply = str_to_decimal(str(coin_json.get(u'available_supply'))).to_eng_string()
        volume_ex = str_to_decimal(str(coin_json.get(u'volume_ex'))).to_eng_string()
        change1h = str_to_decimal(str(coin_json.get(u'change1h'))).to_eng_string()
        change1d = str_to_decimal(str(coin_json.get(u'change1d'))).to_eng_string()
        change7d = str_to_decimal(str(coin_json.get(u'change7d'))).to_eng_string()

        coin_name_cn = u""

        if symbol in new_coin_dict.keys() and new_coin_dict[symbol].rank < priority:
            pass
        else:
            coin = CM(Coin)
            coin.symbol = symbol
            coin.coin_name = coin_name
            coin.coin_name_cn = coin_name_cn
            coin.coin_icon = coin_icon
            coin.available_supply = available_supply
            coin.change1d = change1d
            coin.change7d = change7d
            coin.change1h = change1h
            coin.price = price
            coin.volume_ex = volume_ex
            coin.marketcap = marketcap
            coin.create_time = datetime_to_timestamp_utc_8(datetime.now())
            coin.rank = priority
            coin.is_integral = is_integral

            coin.open = "0"
            coin.close = "0"
            coin.vol = "0"

            new_coin_dict[symbol] = coin

    # 去重插新
    old_coin_list = BaseModel.fetch_all(Coin, "*")
    old_coin_dict = {coin.symbol.upper(): coin for coin in old_coin_list if coin.symbol}
    old_coin_symbol_set = set(old_coin_dict.keys())
    new_coin_symbol_set = set(new_coin_dict.keys())
    comm_coin_symbol_set = new_coin_symbol_set & old_coin_symbol_set
    diff_coin_symbol_set = new_coin_symbol_set - old_coin_symbol_set
    none_coin_symbol_set = old_coin_symbol_set - new_coin_symbol_set

    for diff_coin_symbol in diff_coin_symbol_set:
        new_coin = new_coin_dict[diff_coin_symbol]
        new_coin.save()
    for comm_coin_symbol in comm_coin_symbol_set:
        old_coin = old_coin_dict[comm_coin_symbol]
        new_coin = new_coin_dict[comm_coin_symbol]
        new_coin.coin_id = old_coin.coin_id
        new_coin.save()
    for none_coin_symbol in none_coin_symbol_set:
        none_coin = old_coin_dict[none_coin_symbol]
        none_coin.is_integral = False
        none_coin.save()

    if len(diff_coin_symbol_set) > 0:
        GLOBAL_RULES_UPDATE_FLAG[GLOBAL_MATCHING_DEFAULT_RULES_UPDATE_FLAG] = True

    # logger.info(u"update_coin_info success")


if __name__ == '__main__':
    BaseModel.extract_from_json()
    update_coin_all()
