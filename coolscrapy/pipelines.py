# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .models import Session,Report
from contextlib import contextmanager

@contextmanager
def session_scope(session):
    """Provide a transactional scope around a series of operations."""
    #session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class CoolscrapyPipeline(object):
    def __init__(self):
        self.session = Session()

    def process_item(self, item, spider):
        vul_id = item['vul_id']
        result = self.session.query(Report).filter_by(vul_id=vul_id).first()
        if result:
            pass
        else:
            title = item['title']
            summary = item['summary']
            public_time = item['public_time']
            url = item['url']
            r = Report(vul_id=vul_id,title=title,summary=summary,public_time=public_time,url=url)
            with session_scope(self.session) as session:
                session.add(r)


