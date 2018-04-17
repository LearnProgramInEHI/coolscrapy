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

def Insert_ReportRules(name,start_urls,allowed_domain,
                       vul_id_xpath,public_time_xpath,title_xpath,summary_xpath,
                       detail_page_xpath,next_page_xpath=None,allow_url=None,enable=0):
    r = ReportRules(name=name,start_urls=start_urls,
            allowed_domain=allowed_domain,
            vul_id_xpath=vul_id_xpath,
            public_time_xpath=public_time_xpath,
            title_xpath=title_xpath,
            summary_xpath=summary_xpath,
            next_page_xpath = next_page_xpath,
            detail_page_xpath = detail_page_xpath,
            allow_url=allow_url,
            enable=enable,)
    return r

xlab_rules = Insert_ReportRules(name="xlab",start_urls="https://xlab.tencent.com/cn/category/advisories/",
                allowed_domain="tencent.com",vul_id_xpath="//html//div[@id='content']//p[1]/text()",
                public_time_xpath="//div/footer/span[2]/a/time[1]/text()",
                title_xpath="//h1[@class='entry-title']/text()",
                summary_xpath="//html//p[4]/text()",
                next_page_xpath = "//a[@class='next page-numbers']",
                detail_page_xpath = "//header/h2/a",
                enable=1)

talos_rules = Insert_ReportRules(name='talos',start_urls="https://www.talosintelligence.com/vulnerability_reports#disclosed",
                                 allowed_domain="talosintelligence.com",
                                 vul_id_xpath='//*[@id="page_wrapper"]/div/div/div/div/div/h3',
                                 public_time_xpath='//*[@id="page_wrapper"]/div/div/div/div/div/h5[1]',
                                 title_xpath='//*[@id="page_wrapper"]/div/div/div/div/div/h2',
                                 summary_xpath='//*[@id="page_wrapper"]/div/div/div/div/div/div[1]/p[1]',
                                 detail_page_xpath='//*[@id="vul-report"]/td[2]/a',
                                 allow_url=(r'https://www.talosintelligence.com/vulnerability_reports/TALOS-.*'),
                                 enable=1)

def Exists_in_db(name):
    r = session.query(ReportRules).filter_by(name=name).first()
    if r:
        return True
    else:
        return False

with session_scope(Session) as session:
    if Exists_in_db('xlab'):
        pass
    else:
        session.add(xlab_rules)

    if Exists_in_db('talos'):
        pass
    else:
        session.add(talos_rules)


rules = session.query(ReportRules).filter(ReportRules.enable == 1).all()

# 加入项目配置文件
runner = CrawlerRunner(get_project_settings())
# 导入爬虫
from coolscrapy.spiders.threatenReport import MySpider
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
for rule in rules:
    runner.crawl(MySpider,rule=rule)

d = runner.join()
# 关闭reactor
d.addBoth(lambda _: reactor.stop())
reactor.run()