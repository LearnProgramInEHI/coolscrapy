#!/usr/bin/env python
# coding:utf-8
# author : w0xffff
# date   : 2018/4/16 21:39
# IDE    : PyCharm

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
# 加入项目配置文件
runner = CrawlerRunner(get_project_settings())
# 导入爬虫
from coolscrapy.spiders.securityReport import MySpider
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
d = runner.crawl(MySpider)
# 关闭reactor
d.addBoth(lambda _: reactor.stop())
reactor.run()