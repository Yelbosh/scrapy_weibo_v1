# -*- coding: utf-8 -*-

import os

SPIDER_MODULES = ['scrapy_weibo.spiders']
NEWSPIDER_MODULE = 'scrapy_weibo.spiders'
BOT_NAME = 'weibo'


# enables scheduling storing requests queue in redis
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# don't cleanup redis queues, allows to pause/resume crawls
# SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# Schedule requests using a queue (FIFO).
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

# Schedule requests using a stack (LIFO).
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

# Max idle time to prevent the spider from being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at the first time (because the queue is empty).

# SCHEDULER_IDLE_BEFORE_CLOSE = 10

# The amount of time (in secs) that the downloader should wait 
# before downloading consecutive pages from the same spider
DOWNLOAD_DELAY = 0.05 # 50 ms of delay

# If enabled, Scrapy will wait a random amount of time 
# (between 0.5 and 1.5 * DOWNLOAD_DELAY) while fetching requests 
# from the same spider.
# This randomization decreases the chance of the crawler 
# being detected (and subsequently blocked) by sites which analyze 
# requests looking for statistically significant similarities in 
# the time between their requests.
# RANDOMIZE_DOWNLOAD_DELAY = True


# 期望减少mongodb的压力
# Maximum number of concurrent items (per response) to process in parallel in ItemPipeline, Default 100
CONCURRENT_ITEMS = 100
# The maximum number of concurrent (ie. simultaneous) requests that will be performed by the Scrapy downloader, Default 16.
CONCURRENT_REQUESTS = 16
# The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain, Default: 8.
CONCURRENT_REQUESTS_PER_DOMAIN = 8


# 不需要默认的180秒,更多的机会留给重试
# The amount of time (in secs) that the downloader will wait before timing out, Default: 180.
DOWNLOAD_TIMEOUT = 15

AUTOTHROTTLE_ENABLED = True # Enables the AutoThrottle extension.
AUTOTHROTTLE_START_DELAY = 2.0 # The initial download delay (in seconds).Default: 5.0
AUTOTHROTTLE_MAX_DELAY = 60.0 # The maximum download delay (in seconds) to be set in case of high latencies.
AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD = 100 # How many responses should pass to perform concurrency adjustments.
AUTOTHROTTLE_DEBUG = True


# middlewares 的意思是在engine和download handler之间有一层，包括进入download
# handler之前和从download handler出来之后，同理spider (handler)
# retry 直接在downloader middlewares这一层处理
# 将400 403等有用的预知的错误留给spider middlewares处理

# ** ** ** ** ** ** ** ** ** **
# downloadermiddleware 1 process_request
# ** ** ** ** ** ** ** ** ** **
# downloadermiddleware 2 process_request
# ** ** ** ** ** ** ** ** ** **
# downloadermiddleware 2 process_response
# ** ** ** ** ** ** ** ** ** **
# downloadermiddleware 1 process_response
# ** ** ** ** ** ** ** ** ** **
# spidermiddleware 1 process_spider_input
# ** ** ** ** ** ** ** ** ** **
# spidermiddleware 2 process_spider_input
# spider parse
# ** ** ** ** ** ** ** ** ** **
# spidermiddleware 2 process_spider_output
# ** ** ** ** ** ** ** ** ** **
# spidermiddleware 1 process_spider_output

RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

SPIDER_MIDDLEWARES = {
    'utils4scrapy.middlewares.ErrorRequestMiddleware': 40,
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': None,
    'scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware': None,
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': None,
    # 如果process_spider_input或spider里抛出错误，
    # process_spider_exception是反向执行的，即要想记录错误得先过sentry，在捕获重试
    'utils4scrapy.middlewares.RetryErrorResponseMiddleware': 940,
    #'utils4scrapy.middlewares.SentrySpiderMiddleware': 950
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': None,
    #'utils4scrapy.middlewares.RequestTokenMiddleware': 310,
    'utils4scrapy.middlewares.RequestApiv1AuthMiddleware': 310,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': None,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': None,
    #'utils4scrapy.middlewares.SentryDownloaderMiddleware': 950,
}

ITEM_PIPELINES = [
    'utils4scrapy.pipelines.MongodbPipeline',
    #'scrapy_weibo.pipelines.JsonWriterPipeline'
]

EXTENSIONS = {
    'scrapy.webservice.WebService': None,
    'scrapy.telnet.TelnetConsole': None
}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

#dev
REDIS_HOST = '219.224.135.60'
REDIS_PORT = 6379
MONGOD_HOST = '219.224.135.60'
MONGOD_PORT = 27017
MASTER_TIMELINE_V1_MONGOD_HOST = '219.224.135.60'
MASTER_TIMELINE_V1_MONGOD_PORT = 27017
API_KEY = '3105114937'
API_SECRET = '985e8f106a5db148d1a96abfabcd9043'
PER_TOKEN_HOURS_LIMIT = 2000
PER_IP_HOURS_LIMIT = 30000
BUFFER_SIZE = 20
RETRY_TIMES = 3 - 1