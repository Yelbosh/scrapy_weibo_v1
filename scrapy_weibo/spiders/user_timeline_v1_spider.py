# -*- coding: utf-8 -*-

import simplejson as json
from scrapy.spider import BaseSpider
from utils4scrapy.utils import resp2item_v1
from utils4scrapy.tk_maintain import _default_redis
from utils4scrapy.middlewares import ShouldNotEmptyError
from scrapy import log
from scrapy.http import Request


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
API_KEY = '3105114937'
BASE_URL = 'http://api.t.sina.com.cn/statuses/user_timeline.json?user_id={uid}&page={page}&count=100&source=' + API_KEY

class UserTimelineV1(BaseSpider):
    """usage: scrapy crawl user_timeline -a since_id=3021438975589423 -a max_id=3645300671902176"""
    name = 'user_timeline_v1'

    def start_requests(self):
        uid = 3044080932#3264543895#1813080181
        request = Request(BASE_URL.format(uid=uid, page=1))
        request.meta['page'] = 1
        request.meta['uid'] = uid
        yield request
    
    def parse(self, response):
        page = response.meta['page']
        uid = response.meta['uid']
        print page

        resp = json.loads(response.body)
        results = []

        if resp == []:
            raise ShouldNotEmptyError()

        for status in resp:
            items = resp2item_v1(status)
            results.extend(items)

        page += 1
        request = Request(BASE_URL.format(uid=uid, page=page))
        request.meta['page'] = page
        request.meta['uid'] = uid
        results.append(request)

        return results