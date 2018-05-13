# -*- coding: utf-8 -*-

# IDE问题，import time无报错
import traceback

import time
import threading
import logging

from datetime import datetime

from configs.config import CRAWLER_CIRCLE_INTERVAL
from crawler.coin_all_crawler_v2 import update_coin_all

logger = logging.getLogger('main')


class CrawlerThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.go_work = True
        self.run_start_time = None
        self.run_end_time = None

    def run(self):
        logger.info(u"Start thread id: %s." % str(self.thread_id))
        self.run_start_time = datetime.now()

        while self.go_work:
            try:
                circle_start_time = time.time()

                CrawlerThread._process()

                # crawler_log = CrawlerLog(status = True).generate_create_time()
                # db.session.add(crawler_log)
                # db.session.commit()

                circle_now_time = time.time()
                time_to_rest = CRAWLER_CIRCLE_INTERVAL - (circle_now_time - circle_start_time)
                if time_to_rest > 0:
                    time.sleep(time_to_rest)
                else:
                    pass
            except Exception:
                logger.critical("发生未知错误，捕获所有异常，待查")
                logger.critical(traceback.format_exc())
                # self.go_work = False
                logger.critical("循环继续运行")
        logger.info(u"End thread id: %s." % str(self.thread_id))
        self.run_end_time = datetime.now()

    def stop(self):
        logger.info(u"停止进程")
        self.go_work = False

    @staticmethod
    def _process():
        # update_coin_info()
        update_coin_all()
        # update_notice_info()


crawler_thread = CrawlerThread(thread_id = 'crawler_zclaiqcc')
