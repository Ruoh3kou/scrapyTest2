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
        url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=0&genres=%E6%82%AC%E7%96%91'
        yield Request(url,headers=self.headers)
    
    def parse(self,response):
        datas=json.loads(response.body)['data']
        item=Scrapytest2Item()
        if datas:
            for data in datas:
                item['title'] = data['title']
                item['rate'] = data['rate']
                item['url'] = data['url']
                item['director'] = data['directors'][0]
                yield item

            page_num = re.search(r'start=(\d+)', response.url).group(1)
            page_num = 'start=' + str(int(page_num)+20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            yield Request(next_url, headers=self.headers)
