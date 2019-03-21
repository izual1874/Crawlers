# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from .items import Qcwy51JobItem
from logging import getLogger


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri= crawler.settings.get('MONGO_URI'),
            mongo_db= crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[Qcwy51JobItem.collection].create_index([('url', pymongo.ASCENDING)])


    def process_item(self, item, spider):
        # self.db[item.collection].insert(dict(item))
        self.db[item.collection].update({'url': item.get('url')}, {'$set': item}, True)
        return item

    def close_spider(self, spider):
        self.client.close()
