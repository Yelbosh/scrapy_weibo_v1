# -*- coding: UTF-8 -*-

import sys
import importlib
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy_weibo.spiders.user_info_v1_spider import UserInfoSpiderV1
from scrapy.utils.project import get_project_settings
from scrapy_weibo.settings import SPIDER_MODULES, NEWSPIDER_MODULE, \
                                  BOT_NAME, DOWNLOAD_DELAY, CONCURRENT_ITEMS, \
                                  CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_PER_DOMAIN, \
                                  DOWNLOAD_TIMEOUT, AUTOTHROTTLE_ENABLED, \
                                  AUTOTHROTTLE_START_DELAY, AUTOTHROTTLE_MAX_DELAY, \
                                  AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD, AUTOTHROTTLE_DEBUG, \
                                  RETRY_HTTP_CODES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES, \
                                  ITEM_PIPELINES, EXTENSIONS, REDIS_HOST, REDIS_HOST, REDIS_PORT, \
                                  MONGOD_HOST, MONGOD_PORT, MASTER_TIMELINE_V1_MONGOD_HOST, \
                                  MASTER_TIMELINE_V1_MONGOD_PORT, API_KEY, API_SECRET, \
                                  PER_TOKEN_HOURS_LIMIT, PER_IP_HOURS_LIMIT, BUFFER_SIZE, RETRY_TIMES

since_id = int(sys.argv[1])
max_id = int(sys.argv[2])
spider = UserInfoSpiderV1(from_text=True, since_id=since_id, max_id=max_id)
settings = get_project_settings()
scrapy_weibo_settings_dict = {
    'SPIDER_MODULES': SPIDER_MODULES,
    'NEWSPIDER_MODULE': NEWSPIDER_MODULE,
    'BOT_NAME': BOT_NAME,
    'DOWNLOAD_DELAY': DOWNLOAD_DELAY,
    'CONCURRENT_ITEMS': CONCURRENT_ITEMS,
    'CONCURRENT_REQUESTS': CONCURRENT_REQUESTS,
    'CONCURRENT_REQUESTS_PER_DOMAIN': CONCURRENT_REQUESTS_PER_DOMAIN,
    'DOWNLOAD_TIMEOUT': DOWNLOAD_TIMEOUT,
    'AUTOTHROTTLE_ENABLED': AUTOTHROTTLE_ENABLED,
    'AUTOTHROTTLE_START_DELAY': AUTOTHROTTLE_START_DELAY,
    'AUTOTHROTTLE_MAX_DELAY': AUTOTHROTTLE_MAX_DELAY,
    'AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD': AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD,
    'AUTOTHROTTLE_DEBUG': AUTOTHROTTLE_DEBUG,
    'RETRY_HTTP_CODES': RETRY_HTTP_CODES,
    'SPIDER_MIDDLEWARES': SPIDER_MIDDLEWARES,
    'DOWNLOADER_MIDDLEWARES': DOWNLOADER_MIDDLEWARES,
    'ITEM_PIPELINES': ITEM_PIPELINES,
    'EXTENSIONS': EXTENSIONS,
    'REDIS_HOST': REDIS_HOST,
    'REDIS_PORT': REDIS_PORT,
    'MONGOD_HOST': MONGOD_HOST,
    'MONGOD_PORT': MONGOD_PORT,
    'MASTER_TIMELINE_V1_MONGOD_HOST': MASTER_TIMELINE_V1_MONGOD_HOST,
    'MASTER_TIMELINE_V1_MONGOD_PORT': MASTER_TIMELINE_V1_MONGOD_PORT,
    'API_KEY': API_KEY,
    'API_SECRET': API_SECRET,
    'PER_TOKEN_HOURS_LIMIT': PER_TOKEN_HOURS_LIMIT,
    'PER_IP_HOURS_LIMIT': PER_IP_HOURS_LIMIT,
    'BUFFER_SIZE': BUFFER_SIZE,
    'RETRY_TIMES': RETRY_TIMES
}
settings.overrides.update(scrapy_weibo_settings_dict)
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run() # the script will block here until the spider_closed signal was sent