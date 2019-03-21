# -*- coding: utf-8 -*-
import scrapy, re
from scrapy import Request
from qcwy_51job.items import Qcwy51JobItem
from logging import getLogger

class QcwySpider(scrapy.Spider):
    name = 'qcwy'
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']
    #可以换成自己所需要爬取的

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
            item['com_nature'] = response.xpath('//div[@class="com_tag"]/p[1]/text()').extract_first()
            item['com_p'] = response.xpath('//div[@class="com_tag"]/p[2]/text()').extract_first()
            fuli = response.xpath('//span[@class="sp4"]/text()').extract()
            item['fuli'] = '，'.join(fuli)
            msg_job = response.xpath('//div[@class="bmsg job_msg inbox"]/p/span/text()')
            if msg_job == []:
                msg_job = response.xpath('//div[@class="bmsg job_msg inbox"]/p/text()')
                if msg_job == []:
                    msg_job = response.xpath('//div[@class="bmsg job_msg inbox"]/text()')
            msg_job = re.findall('(\S+)', ''.join(msg_job))
            item['msg_job'] = ' '.join(msg_job)
            msg_ltype = response.xpath('//p[@class="msg ltype"]/@title').extract_first() 
            if isinstance(msg_ltype, str):
                item['exp'] = ''.join(re.findall('(无工作经验|\d-\d年经验|\d年经验)', msg_ltype))
                item['xueli'] = ''.join(re.findall('(大专|本科|硕士|博士)', msg_ltype))
                item['count'] = ''.join(re.findall('(若干人|招\d+人)', msg_ltype))
                item['date'] = re.findall('(\d\d-\d\d发布)', msg_ltype)[0]
                item['area'] = [i.strip() for i in msg_ltype.split('|')][0]

            yield item