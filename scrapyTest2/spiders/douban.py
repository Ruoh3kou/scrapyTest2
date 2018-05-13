import os
import re
import json

from scrapy import Request,Spider
from scrapy.selector import Selector
from ..items import Scrapytest2Item
from scrapy.linkextractors import LinkExtractor

class douban(Spider):
    name='dbSpider'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    
    def start_requests(self):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'
        yield Request(url,headers=self.headers)
    
    def parse(self,response):
        datas=json.loads(response.body)['subjects']
        item=Scrapytest2Item()
        if datas:
            for data in datas:
                item['title'] = data['title']
                item['rate'] = data['rate']
                item['url'] = data['url']
                yield item

            page_num = re.search(r'start=(\d+)', response.url).group(1)
            page_num = 'start=' + str(int(page_num)+20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            yield Request(next_url, headers=self.headers)
