# -*- coding: utf-8 -*-
import scrapy, re
from scrapy import Request
from qcwy_51job.items import Qcwy51JobItem

class QcwySpider(scrapy.Spider):
    name = 'qcwy'
    # allowed_domains = ['www.51job.com', 'https://search.51job.com', 'https://jobs.51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']

    def parse(self, response):
        jobs = response.xpath('//div[@id="resultList"]/div/p/span/a/@href').extract()
        for job in jobs:
            yield Request(url= job, callback= self.one_job)

        nextpage = response.xpath('//div[@class="p_in"]/ul/li[last()]/a/@href').extract_first()
        if nextpage is not None:
            nextpage = response.urljoin(nextpage)
            yield Request(url= nextpage, callback= self.parse)

    def one_job(self, response):
            item = Qcwy51JobItem()
            item['url'] = response.url
            item['title'] = response.xpath('//div[@class="tHeader tHjob"]/div/div/h1/@title').extract_first()
            item['salary'] = response.xpath('//div[@class="tHeader tHjob"]/div/div/strong/text()').extract_first()
            item['company'] = response.xpath('//p[@class="cname"]/a/@title').extract_first()
            msg_ltype = response.xpath('//p[@class="msg ltype"]/@title').extract_first() 
            fuli = response.xpath('//span[@class="sp4"]/text()').extract()
            msg_job = response.xpath('//div[@class="bmsg job_msg inbox"]/p/text()').extract()
            item['com_nature'] = response.xpath('//div[@class="com_tag"]/p[1]/text()').extract_first()
            item['com_p'] = response.xpath('//div[@class="com_tag"]/p[2]/text()').extract_first()
            msg_list = [i.strip() for i in msg_ltype.split('|')]
            item['fuli'] = '，'.join(fuli)
            item['msg_job'] = ' '.join(msg_job)
            if len(msg_list) == 5:
                item['area'] = msg_list[0]
                item['exp'] = msg_list[1]
                item['xueli'] = msg_list[2]
                item['count'] = msg_list[-2]
                item['date'] = msg_list[-1]
            elif len(msg_list) == 4:
                item['area'] = msg_list[0]
                item['exp'] = '无'
                item['count'] = msg_list[-2]
                item['date'] = msg_list[-1]
                if '专科' in ','.join(msg_job):
                    item['xueli'] = '大专'
                else:
                    item['xueli'] = 'msg_job中'

            yield item