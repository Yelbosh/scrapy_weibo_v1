# -*- coding: utf-8 -*-

from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider

class LoginSpider(BaseSpider):
    name = 'weibo_login'
    start_urls = ['https://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F%3Fs2w%3Dlogin&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt=']

    def parse(self, response):
        return [FormRequest.from_response(response,
                    formname='login_form',
                    formdata={'mobile': '1257819385@qq.com', 'password_9279': '822851'},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        # continue scraping with authenticated session...