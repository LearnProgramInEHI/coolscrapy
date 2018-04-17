#!/usr/bin/env python
# coding:utf-8
# author : w0xffff
# date   : 2018/4/16 20:05
# IDE    : PyCharm

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SecurityReport

'''
https://www.talosintelligence.com/vulnerability_reports#zerodays
https://www.talosintelligence.com/vulnerability_reports#disclosed

'''
class MySpider2(CrawlSpider):
    name = 'report2'
    def __init__(self):
        self.allowed_domain = ['https://www.talosintelligence.com/vulnerability_reports#disclosed']
        self.start_urls = ['https://www.talosintelligence.com/vulnerability_reports#disclosed']
        self.rules = (
            Rule(LinkExtractor(allow=('tencent.com'),restrict_xpaths="//a[@class='next page-numbers']")),
            Rule(LinkExtractor(allow=('tencent.com'),restrict_xpaths="//header/h2/a"),callback='parse_items')
        )
        super(MySpider2,self).__init__()


    def parse_items(self,response):
        item = SecurityReport()
        item['url'] = response.url
        #self.logger.info(response.xpath('//div/footer/span[2]/a/time[1]/text()').extract()[0])
        try:
            item['public_time'] = response.xpath('//div/footer/span[2]/a/time[1]/text()').extract()[0]
        except Exception as e:
            item['public_time'] = 'null'
            self.logger.error(item["public_time"]+"is null and it is in ",item['url'])

        try:
            item['vul_id'] = response.xpath("//html//div[@id='content']//p[1]/text()").extract()[0]
        except Exception as e:
            item['vul_id'] = 'null'
            self.logger.error(item["vul_id"]+"is null and it is in ",item['url'])

        try:
            item["summary"] = response.xpath("//html//p[4]/text()").extract()[0]
        except Exception as e:
            item["summary"] = 'null'
            self.logger.error(item["vul_id"]+"is null and it is in ",item['url'])
        try:
            item['title'] = response.xpath("//h1[@class='entry-title']/text()").extract()[0]
        except Exception as e:
            item['title'] = 'null'
            self.logger.error(item["title"] + "is null and it is in ", item['url'])

        return item




