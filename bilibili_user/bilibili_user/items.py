# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    col = 'users'

    mid = Field()
    name = Field()
    sex = Field()
    face = Field()
    sign = Field()
    rank = Field()
    level = Field()
    jointime = Field()
    moral = Field()
    silence = Field()
    birthday = Field()
    coins = Field()
    fans_badge = Field()
    role = Field()
    title = Field()
    desc = Field()
    types = Field()
    status = Field()
    theme_type = Field()
    is_followed = Field()
    top_photo = Field()

class UserFFItem(Item):
    col = 'users'
    mid = Field()
    followings = Field()
    fans = Field()

class UserFFCountsItem(Item):
    col = 'users'
    mid = Field()
    following_counts = Field()
    fan_counts = Field()
