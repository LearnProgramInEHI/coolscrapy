#!/usr/bin/env python
# coding:utf-8
# author : w0xffff
# date   : 2018/4/16 21:12
# IDE    : PyCharm


from sqlalchemy import create_engine,String,Column,Integer,Text,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
from .settings import MYSQL_USER,MYSQL_PASSWORD,MYSQL_HOST,MYSQL_DB,MYSQL_PORT

engine = create_engine('mysql+pymysql://'+MYSQL_USER+':'+MYSQL_PASSWORD+'@'+MYSQL_HOST+':'+str(MYSQL_PORT)+'/'+MYSQL_DB+'?charset=utf8',encoding='utf-8')
Session = sessionmaker(bind=engine)
Base = declarative_base()



class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer,primary_key=True)
    vul_id=Column(String(64))
    title = Column(String(256))
    summary = Column(Text)
    public_time = Column(String(64))
    url = Column(String(500))
    catched_day = Column(Date,default=date.today)

    def __repr__(self):
        return "<report: %s>"%self.title

def initDB():
    Base.metadata.create_all(engine)

initDB()