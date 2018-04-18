# -*- coding: utf-8 -*-
import logging
import json
from datetime import datetime

import requests

from configs.config import db, GLOBAL_RULES_UPDATE_FLAG, GLOBAL_NOTICE_UPDATE_FLAG
from models.synchronous_announcement_models import BlockCCCrawlNotice

logger = logging.getLogger('main')

headers = {
    "Host": "block.cc",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36 encors/0.0.6",
    "lan": "zh",
    "DNT": 1,
    "Referer": "https://block.cc/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": "Hm_lvt_e5950dd990c06938d5c1010c07ba467c=1519713610; Hm_lpvt_e5950dd990c06938d5c1010c07ba467c=1519732238"
}


# def get_total_notice_list():
#     page_count = 10
#     page = 0
#     start_time = datetime.now()
#     notice_list = list()
#     while page < page_count:
#         url = u"https://block.cc/api/v1/getNoticesInfo?lang=zh&page=" + str(page) + u"&size=10"
#         try:
#             response = requests.get(url, timeout = 600, headers = headers)
#             data_json = json.loads(response.content).get('data')
#             notice_list += data_json.get('data')
#             page_count = data_json.get('pageCount')
#             page += 1
#         except Exception as e:
#             print 'err'
#
#         print 'done', page, '|', page_count, (datetime.now() - start_time)
#
#     end_time = datetime.now()
#     print end_time - start_time
#
#     return notice_list

notice_size = 10


def get_notice_list():
    success_flag = False
    # start_time = datetime.now()
    notice_list = list()
    while not success_flag:
        url = u"https://block.cc/api/v1/getNoticesInfo?lang=zh&page=0&size=" + str(notice_size)
        try:
            response = requests.get(url, timeout = 600, headers = headers)
            data_json = json.loads(response.content).get('data')
            notice_list += data_json.get('data')
            success_flag = True
        except Exception as e:
            print 'err'

    # end_time = datetime.now()
    # print end_time - start_time

    return notice_list


def update_notice_info():
    notice_list = get_notice_list()
    if len(notice_list) > 0:
        new_notice_dict = dict()
        for notice_json in notice_list:
            uid = notice_json.get(u'_id', u'')
            lang = notice_json.get(u'lang', u'')
            origin_url = notice_json.get(u'originUrl', u'')
            created_at = notice_json.get(u'createdAt', u'')
            updated_at = notice_json.get(u'updatedAt', u'')
            zh_name = notice_json.get(u'zh_name', u'')
            from_source = notice_json.get(u'from', u'')
            title = notice_json.get(u'title', u'')
            description = notice_json.get(u'description', u'')
            timestamp = notice_json.get(u'timestamp')

            notice = BlockCCCrawlNotice(uid, lang, origin_url, created_at, updated_at, zh_name, from_source, title, description, timestamp)
            new_notice_dict[uid] = notice

        # 去重插新
        old_notice_list = db.session.query(BlockCCCrawlNotice).order_by(BlockCCCrawlNotice.timestamp.desc()).limit(notice_size * 10).all()
        # old_notice_list = db.session.query(BlockCCCrawlNotice).all()
        old_notice_dict = {notice.uid: notice for notice in old_notice_list}
        old_notice_uid_set = set(old_notice_dict.keys())
        new_notice_uid_set = set(new_notice_dict.keys())
        comm_notice_uid_set = new_notice_uid_set & old_notice_uid_set
        diff_notice_uid_set = new_notice_uid_set - old_notice_uid_set
        if len(diff_notice_uid_set) > 0:
            GLOBAL_RULES_UPDATE_FLAG[GLOBAL_NOTICE_UPDATE_FLAG]["blockcc"] = True

        for diff_notice_uid in diff_notice_uid_set:
            new_notice = new_notice_dict[diff_notice_uid]
            new_notice.is_handled = False
            db.session.add(new_notice)
        for comm_notice_uid in comm_notice_uid_set:
            old_notice = old_notice_dict[comm_notice_uid]
            new_notice = new_notice_dict[comm_notice_uid]
            new_notice.aid = old_notice.aid
            if new_notice.timestamp > old_notice.timestamp:
                new_notice.is_handled = False
                GLOBAL_RULES_UPDATE_FLAG[GLOBAL_NOTICE_UPDATE_FLAG]["blockcc"] = True
            else:
                new_notice.is_handled = old_notice.is_handled
            db.session.merge(new_notice)

        db.session.commit()
        # logger.info(u"update_notice_info success")


# update_notice_info()
