#-*-coding:utf-8-*-
"""spider for showing user personal information"""

import simplejson as json
from scrapy.spider import BaseSpider
from utils4scrapy.utils import resp2item_v1
from utils4scrapy.tk_maintain import _default_redis
from scrapy import log
from scrapy.conf import settings
from scrapy.http import Request


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
API_KEY = '3105114937'
UIDS_SET = '{spider}:uids'
BASE_URL = 'http://api.t.sina.com.cn/users/show.json?user_id={uid}&source=' + API_KEY


class UserInfoSpiderV1(BaseSpider):
    """usage: scrapy crawl user_info_v1 -a from_text=1 -a since_id=1 -a max_id=100"""
    name = 'user_info_v1'

    def __init__(self, **kw):
        super(UserInfoSpiderV1, self).__init__(**kw)
        since_id = kw.get('since_id', None)
        max_id = kw.get('max_id', None)
        from_text = kw.get('from_text', False)
        if from_text == '1':
            from_text = True
        if since_id:
            since_id = int(since_id)
        if max_id:
            max_id = int(max_id)
        self.since_id = since_id
        self.max_id = max_id
        self.from_text = from_text
        
    def start_requests(self):
        uids = self.prepare(self.from_text, self.since_id, self.max_id)
        for uid in uids:
            request = Request(BASE_URL.format(uid=uid), headers=None)
            yield request

    def parse(self, response):
        resp = json.loads(response.body)

        items = resp2item_v1(resp)
        return items

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
            fname = 'uid_about_marine'
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
