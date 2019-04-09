# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
import json, re
from bilibili_user.items import *

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['api.bilibili.com']
    # start_urls = ['http://www.bilibili.com/']
    user_url = 'https://api.bilibili.com/x/space/acc/info?mid={mid}&jsonp=jsonp'
    count_url = 'https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp'
    followings_url = 'https://api.bilibili.com/x/relation/followings?vmid={mid}&pn={page}&ps=20&order=desc&jsonp=jsonp'
    fans_url = 'https://api.bilibili.com/x/relation/followers?vmid={mid}&pn={page}&ps=20&order=desc&jsonp=jsonp'
    start_user = ['8209464', '102885422', '20247643', '8034163', '3404595']

    def start_requests(self):
        for mid in self.start_user:
            yield Request(self.user_url.format(mid= mid), callback= self.parse_user)

    def parse_user(self, response):
        result = json.loads(response.text)
        user_item = UserItem()
        if result.get('data'):
            data = result.get('data')
            official = data.get('official')
            vip = data.get('vip')
            mid = data.get('mid')
            user_item['mid'] = mid
            user_item['name'] = data.get('name')
            user_item['sex'] = data.get('sex')
            user_item['face'] = data.get('face')
            user_item['sign'] = data.get('sign')
            user_item['rank'] = data.get('rank')
            user_item['level'] = data.get('level')
            user_item['jointime'] = data.get('jointime')
            user_item['moral'] = data.get('moral')
            user_item['silence'] = data.get('silence')
            user_item['birthday'] = data.get('birthday')
            user_item['coins'] = data.get('coins')
            user_item['fans_badge'] = data.get('fans_badge')
            user_item['role'] = official.get('role')
            user_item['title'] = official.get('title')
            user_item['desc'] = official.get('desc')
            user_item['types'] = vip.get('type')
            user_item['status'] = vip.get('status')
            user_item['theme_type'] = vip.get('theme_type')
            user_item['is_followed'] = data.get('is_followed')
            user_item['top_photo'] = data.get('top_photo')
            yield user_item

            yield Request(self.fans_url.format(mid=mid, page=1), callback=self.parse_fans, meta={'mid': mid, 'page': 1})
            yield Request(self.followings_url.format(mid=mid, page=1), callback=self.parse_followings, meta={'mid': mid, 'page': 1})
            yield Request(self.count_url.format(mid=mid), callback=self.parse_counts, meta={'mid': mid})


    def parse_followings(self, response):
        result = json.loads(response.text)
        if result.get('data') and len(result.get('data').get('list')):
            followings = result.get('data').get('list')
            for following in followings:
                mid = following.get('mid')
                yield Request(self.user_url.format(mid= mid), callback= self.parse_user)

            mid = response.meta.get('mid')
            user_ff_item = UserFFItem()
            user_ff_item['mid'] = mid
            user_ff_item['followings'] = [{'mid': following.get('mid')} for following in followings]
            user_ff_item['fans'] = []
            yield user_ff_item
            page = response.meta.get('page') + 1
            yield Request(self.followings_url.format(mid= mid, page= page), callback= self.parse_followings, meta= {'mid': mid, 'page': page})

    def parse_fans(self, response):
        result = json.loads(response.text)
        if result.get('data') and len(result.get('data').get('list')):
            fans = result.get('data').get('list')
            for fan in fans:
                mid = fan.get('mid')
                yield Request(self.user_url.format(mid=mid), callback=self.parse_user)

            mid = response.meta.get('mid')
            user_ff_item = UserFFItem()
            user_ff_item['mid'] = mid
            user_ff_item['followings'] = []
            user_ff_item['fans'] = [{'mid': fan.get('mid') } for fan in fans]
            yield user_ff_item
            page = response.meta.get('page') + 1
            yield Request(self.fans_url.format(mid= mid, page= page), callback= self.parse_fans, meta= {'mid': mid, 'page': page})

    def parse_counts(self, response):
        result = json.loads(response.text)
        counts_item = UserFFCountsItem()
        if result.get('data'):
            data = result.get('data')
            counts_item['mid'] = data.get('mid')
            counts_item['following_counts'] = data.get('following')
            counts_item['fan_counts'] = data.get('follower')
            yield counts_item