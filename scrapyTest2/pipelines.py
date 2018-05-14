# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class Scrapytest2Pipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost", user="root", password="ruohua3kou", db="test", port=3306, charset="utf8")
        self.cur = self.conn.cursor()
        self.cur.execute("SET NAMES utf8")
        sql_tables = """create table IF NOT EXISTS doubanXuanyi(title varchar(50),rate float(3,2),url varchar(100),director varchar(100));"""
        self.cur.execute(sql_tables)


    def process_item(self, item, spider):
        title=item.get('title')
        rate = item.get('rate')
        url = item.get('url')
        director = item.get('director')
        
        sql_insert="""insert into doubanxuanyi(title, rate, url,director)
            VALUES (%s, %s, %s, %s);
        """
        self.cur.execute(sql_insert,(title,rate,url,director))
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
