# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Qcwy51JobItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'job_python'
    url = Field()
    title = Field()
    salary = Field()
    company = Field()
    com_nature = Field()
    com_p = Field()
    fuli = Field()
    msg_job = Field()
    area = Field()
    exp = Field()
    xueli = Field()
    count = Field()
    date = Field()
    url = Field()
