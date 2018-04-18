# -*- coding: utf-8 -*-
import logging
import json

import requests


from datetime import datetime

from configs.config import db, GLOBAL_RULES_UPDATE_FLAG, GLOBAL_MATCHING_DEFAULT_RULES_UPDATE_FLAG
from crawler.usdcny import dollar_currency_rate
from models.real_time_quotes_models import RealTimeQuotesDefaultSettingInfo
from utils.u_transformat import str_to_decimal

logger = logging.getLogger('main')

headers = {
    "Host": "block.cc",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.186 Safari/537.36 encors/0.0.6',
    "lan": "zh",
    "DNT": 1,
    "Referer": "https://block.cc/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": "Hm_lvt_e5950dd990c06938d5c1010c07ba467c=1519713610; Hm_lpvt_e5950dd990c06938d5c1010c07ba467c=1519732238"
}


def get_coin_list():
    page_count = 10
    page = 0
    start_time = datetime.now()
    coin_list = list()
    while page < page_count:
        url = u"https://block.cc/api/v1/coin/list?page=" + str(page) + u"&size=200"
        try:
            response = requests.get(url, timeout = 600, headers = headers)
            data_json = json.loads(response.content).get('data')
            coin_list += data_json.get('list')
            page_count = data_json.get('pageCount')
            page += 1
        except Exception:
            print 'err'

    print 'coin crawler done', (datetime.now() - start_time)

    end_time = datetime.now()
    print end_time - start_time

    return coin_list


def update_coin_info():
    coin_list = get_coin_list()
    usdcny_str = dollar_currency_rate()
    usdcny = str_to_decimal(usdcny_str)
    if len(coin_list) > 0:
        new_coin_dict = dict()
        for coin_json in coin_list:
            coin_id = coin_json.get(u'id', u'')
            symbol = coin_json.get(u'symbol').upper()
            if not symbol:
                continue
            coin_name = coin_json.get(u'name', u'')
            coin_name_cn = coin_json.get(u'zhName', u'')

            available_supply = str_to_decimal(str(coin_json.get(u'available_supply')))
            change1d = str_to_decimal(str(coin_json.get(u'change1d')))
            change1h = str_to_decimal(str(coin_json.get(u'change1h')))
            change7d = str_to_decimal(str(coin_json.get(u'change7d')))
            price = str_to_decimal(str(coin_json.get(u'price'))) * usdcny
            volume_ex = str_to_decimal(str(coin_json.get(u'volume_ex')))
            marketcap = str_to_decimal(str(coin_json.get(u'marketCap'))) * usdcny
            suggest_ex1 = u""
            suggest_ex2 = u""
            suggest_ex1_url = u""
            suggest_ex2_url = u""
            suggest_ex_list = coin_json.get(u'suggest_ex')
            if suggest_ex_list and len(suggest_ex_list) > 0:
                suggest_ex1 = suggest_ex_list[0].get(u'zh_name')
                suggest_ex1_url = suggest_ex_list[0].get(u'link')
                if len(suggest_ex_list) > 1:
                    suggest_ex2 = suggest_ex_list[1].get(u'zh_name')
                    suggest_ex2_url = suggest_ex_list[1].get(u'link')
            coin = RealTimeQuotesDefaultSettingInfo(symbol, coin_name, coin_name_cn, coin_id, available_supply,
                                                    change1d, change7d, change1h, price, volume_ex, marketcap,
                                                    suggest_ex1, suggest_ex2, suggest_ex1_url, suggest_ex2_url)
            new_coin_dict[symbol] = coin

        # 去重插新
        old_coin_list = db.session.query(RealTimeQuotesDefaultSettingInfo).all()
        old_coin_dict = {coin.symbol.upper(): coin for coin in old_coin_list if coin.symbol}
        old_coin_symbol_set = set(old_coin_dict.keys())
        new_coin_symbol_set = set(new_coin_dict.keys())
        comm_coin_symbol_set = new_coin_symbol_set & old_coin_symbol_set
        diff_coin_symbol_set = new_coin_symbol_set - old_coin_symbol_set
        if len(diff_coin_symbol_set) > 0:
            GLOBAL_RULES_UPDATE_FLAG[GLOBAL_MATCHING_DEFAULT_RULES_UPDATE_FLAG] = True

        for diff_coin_symbol in diff_coin_symbol_set:
            new_coin = new_coin_dict[diff_coin_symbol]
            db.session.add(new_coin)
        for comm_coin_symbol in comm_coin_symbol_set:
            old_coin = old_coin_dict[comm_coin_symbol]
            new_coin = new_coin_dict[comm_coin_symbol]
            new_coin.ds_id = old_coin.ds_id
            db.session.merge(new_coin)

        db.session.commit()
        logger.info(u"update_coin_info success")


# update_coin_info()
