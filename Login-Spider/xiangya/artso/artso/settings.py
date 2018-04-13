# -*- coding: utf-8 -*-

# Scrapy settings for artso project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from random import randrange

BOT_NAME = 'artso'

SPIDER_MODULES = ['artso.spiders']
NEWSPIDER_MODULE = 'artso.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'artso (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
  'Cookies':'gsScrollPos-1276=0; tulu_pop=1; Hm_lvt_851619594aa1d1fb8c108cde832cc127=1523465820; artron_67ae_saltkey=G4smTtVQ; artron_67ae_lastvisit=1523462228; artron_loginuser=%E7%8E%8B%E5%9D%A4%E7%A5%A5; _at_pt_0_=2446806; _at_pt_1_=%E7%8E%8B%E5%9D%A4%E7%A5%A5; _at_pt_2_=314a3bb686fc0a54947b5b28ca495680; artron_67ae_sid=ylg5RB; artron_67ae_lastact=1523468001%09uc.php%09; artron_67ae_auth=989eh1%2BzHnhY3UpkSJMF5LxuIjnUSOBuhq6zJrqG5h3zRkpHZ7SwHlRqzsyJgjX4sSySmAg2bqHFq4cx6guUEVGXeIIH; artron_auth=8781oe5hdToWYvQy%2FRe0WDjAV8CaLbGNxY6pFOeNeJPMDB9PG610fKUrVKr4O1W217geSLqdUOGENIK%2F6lRkzXW2zxXj; growingio_2446806=var+_giuser+%3D+%7B%0A%09%09uid%3A+%222446806%22%2C+gender%3A+%22%E6%9C%AA%E7%9F%A5%22%2C+source%3A+%221%22%2C+date%3A+%222018-04-09%22%0A%09%7D%3B; gr_user_id=6f425c58-a8f5-4ef7-ab6d-b9243a0dcc53; Hm_lpvt_851619594aa1d1fb8c108cde832cc127=1523499477',
  'Referer': 'http://artso.artron.net/auction/search_auction.php?keyword=%E8%B1%A1%E7%89%99&page=' + str(randrange(100)),
  # 'Referer': 'www.baidu.com'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'artso.middlewares.ArtsoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'artso.middlewares.RandomProxy': None,
   'artso.middlewares.RandomUserAgent':20,
   # 'artso.middlewares.ArtsoDownloaderMiddleware': 543,
   'artso.middlewares.ArtsoDownloaderMiddleware': None,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'artso.pipelines.ArtsoPipeline': 300,
   'artso.pipelines2json.ArtsoPipeline': 300,
   # 'artso.pipelines2mysql.ArtsoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
