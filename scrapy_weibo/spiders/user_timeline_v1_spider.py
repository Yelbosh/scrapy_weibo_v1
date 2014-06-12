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
BASE_URL = 'http://api.t.sina.com.cn/statuses/user_timeline.json?user_id={uid}&page={page}&count=200&source=' + API_KEY

class UserTimelineV1(BaseSpider):
    """usage: scrapy crawl user_timeline_v1 -a from_text=1 -a since_id=1 -a max_id=100 -a mode=onepage or allpages"""
    name = 'user_timeline_v1'
    
    def __init__(self, **kw):
        super(UserTimelineV1, self).__init__(**kw)
        since_id = kw.get('since_id', None)
        max_id = kw.get('max_id', None)
        from_text = kw.get('from_text', False)
        mode = kw.get('mode', 'onepage')
        if from_text == '1':
            from_text = True
        if since_id:
            since_id = int(since_id)
        if max_id:
            max_id = int(max_id)
        self.since_id = since_id
        self.max_id = max_id
        self.from_text = from_text
        self.mode = mode

    def start_requests(self):
        uids = self.prepare(self.from_text, self.since_id, self.max_id)
        for uid in uids:
            request = Request(BASE_URL.format(uid=uid, page=1))
            request.meta['page'] = 1
            request.meta['uid'] = uid
            yield request
    
    def parse(self, response):
        page = response.meta['page']
        uid = response.meta['uid']

        resp = json.loads(response.body)
        results = []

        if resp == []:
            raise ShouldNotEmptyError()

        for status in resp:
            items = resp2item_v1(status)
            results.extend(items)
        
        if self.mode == 'allpages':
            page += 1
            request = Request(BASE_URL.format(uid=uid, page=page))
            request.meta['page'] = page
            request.meta['uid'] = uid
            results.append(request)

        return results

    def prepare(self, fromtext=False, start_idx=0, end_idx=100):
        if not fromtext:
            host = settings.get('REDIS_HOST', REDIS_HOST)
            port = settings.get('REDIS_PORT', REDIS_PORT)
            self.r = _default_redis(host, port)

            uids_set = UIDS_SET.format(spider=self.name)
            log.msg(format='Load uids from %(uids_set)s', level=log.WARNING, uids_set=uids_set)
            uids = self.r.smembers(uids_set)
            if uids == []:
                log.msg(format='Not load any uids from %(uids_set)s', level=log.WARNING, uids_set=uids_set)

        else:
            uids = []
            fname = '20140609_boat_uidlist.txt'
            log.msg(format='Load uids from %(uids_set)s', level=log.WARNING, uids_set=fname)
            f = open('./source/%s' % fname)
            count = 0
            for line in f:
                count += 1
                if count >= start_idx and count <= end_idx:
                    uids.append(int(line.strip()))
                elif count > start_idx:
                    break
                else:
                    pass
            if uids == []:
                log.msg(format='Not load any uids from %(uids_set)s', level=log.WARNING, uids_set=fname)
            f.close()    
        
        return uids
