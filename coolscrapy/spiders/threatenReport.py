#!/usr/bin/env python
# coding:utf-8
# author : w0xffff
# date   : 2018/4/16 23:17
# IDE    : PyCharm
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
    def __init__(self,rule):
        self.rule = rule
        if ',' in rule.start_urls or ',' in rule.allowed_domain:
            self.start_urls = rule.start_urls.split(',')
            self.allowed_domain = rule.allowed_domain.split(",")
        else:
            self.start_urls = [rule.start_urls]
            self.allowed_domain = [rule.allowed_domain]
        self.allow_url = rule.allow_url

        self.rule_list = []
        if rule.next_page_xpath:
            self.rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page_xpath)))
        else:
            self.rule_list.append(Rule(LinkExtractor(allow=self.allow_url)))

        self.rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.detail_page_xpath),callback='parse_items'))
        self.rules = tuple(self.rule_list)
        super(MySpider,self).__init__()


    def parse_items(self,response):
        item = SecurityReport()
        item['url'] = response.url
        #self.logger.info(response.xpath('//div/footer/span[2]/a/time[1]/text()').extract()[0])
        try:
            item['public_time'] = response.xpath(self.rule.public_time_xpath).extract()[0]
        except Exception as e:
            item['public_time'] = 'null'
            #self.logger.error(item["public_time"]+"is null and it is in ",item['url'])

        try:
            item['vul_id'] = response.xpath(self.rule.vul_id_xpath).extract()[0]
        except Exception as e:
            item['vul_id'] = 'null'
            #self.logger.error(item["vul_id"]+"is null and it is in ",item['url'])
        try:
            item["summary"] = response.xpath(self.rule.summary_xpath).extract()[0]
        except Exception as e:
            item["summary"] = 'null'
            #self.logger.error(item["vul_id"]+"is null and it is in ",item['url'])
        try:
            item['title'] = response.xpath(self.rule.title_xpath).extract()[0]
        except Exception as e:
            item['title'] = 'null'
            #self.logger.error(item["title"] + "is null and it is in ", item['url'])

        return item




