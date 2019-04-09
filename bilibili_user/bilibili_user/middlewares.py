# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging, requests, json
import asyncio, aiohttp
from aiohttp import ClientError


class ProxyMiddleware():
    def __init__(self, proxy_url, test_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.test_url = test_url

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL'),
            test_url =settings.get('TEST_URL'),

        )

    def get_proxies(self):
        try:
            proxies = []
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                result = json.loads(response.text)
                if result.get('status') == 0:
                    for i in result.get('data'):
                        proxy = str(i.get('ip')) + ':' + str(i.get('http_port'))
                        proxies.append(proxy)
                    return proxies
        except requests.ConnectionError:
            return False


    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        proxies = self.get_proxies()
        if proxies:
            for proxy in proxies:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + proxy)
                request.meta['proxy'] = uri


