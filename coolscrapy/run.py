#!/usr/bin/env python
# coding:utf-8
# author : w0xffff
# date   : 2018/4/16 21:39
# IDE    : PyCharm

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from coolscrapy.models import ReportRules,Session

from contextlib import contextmanager

@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

r = ReportRules(start_urls="tencent.com",
            allowed_domain="tencent.com",
            vul_id_xpath="//html//div[@id='content']//p[1]/text()",
            public_time_xpath="//div/footer/span[2]/a/time[1]/text()",
            title_xpath="//h1[@class='entry-title']/text()",
            summary_xpath="//html//p[4]/text()",
            enable=1,)

with session_scope(Session) as session:
    session.add(r)

# 加入项目配置文件
runner = CrawlerRunner(get_project_settings())
# 导入爬虫
from coolscrapy.spiders.securityReport import MySpider
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
d = runner.crawl(MySpider)
# 关闭reactor
d.addBoth(lambda _: reactor.stop())
reactor.run()