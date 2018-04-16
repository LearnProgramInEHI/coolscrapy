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
class MySpider(CrawlSpider):
    name = 'report'
    allowed_domain = ['tencent.com']
    start_urls = ['https://xlab.tencent.com/cn/category/advisories/']
    rules = (
        Rule(LinkExtractor(allow=('tencent.com'),restrict_xpaths="//a[@class='next page-numbers']")),
        Rule(LinkExtractor(allow=('tencent.com'),restrict_xpaths="//header/h2/a"),callback='parse_items')
    )

    def parse_items(self,response):
        item = SecurityReport()
        #self.logger.info(response.xpath('//div/footer/span[2]/a/time[1]/text()').extract()[0])
        try:
            item['public_time'] = response.xpath('//div/footer/span[2]/a/time[1]/text()').extract()[0]
            item['vul_id'] = response.xpath("//html//div[@id='content']//p[1]/text()").extract()[0]
            item["summary"] = response.xpath("//html//p[4]/text()").extract()[0]
            item['url'] = response.url
            item['title'] = response.xpath("//h1[@class='entry-title']/text()").extract()[0]
        except Exception as e:
            self.logger.error(e)

        return item




