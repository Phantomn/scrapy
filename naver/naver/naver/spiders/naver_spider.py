# -*- coding: utf-8 -*-
import scrapy
from naver.items import NaverItem
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
from urllib.parse import *
from scrapy.utils.markup import remove_tags
import re


class NaverSpider(scrapy.Spider):
    name = 'naver'
    handle_httpstatus_list = [401]

    def __init__(self, page=10, keyword=None, *args, **kwargs):
    	super(NaverSpider, self).__init__(*args, **kwargs)
    	self.start_urls = ["https://openapi.naver.com/v1/search/blog.xml?query=%s&st=sim&display=%d"%(quote(keyword), int(page))]
    def start_requests(self):
    	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0','X-Naver-Client-Id':'xpXG0w9zhu38TTo6Dt6Y','X-Naver-Client-Secret':'_rRmYGxbcA'}
    	#meta = Handle_httpstatus_list = [401]
    	for url in self.start_urls:
    		yield Request(url, headers=headers)
    def parse(self, response):
        item = NaverItem()
        for sel in response.xpath('//item'):
        	title = sel.select('title/text()').extract_first()
        	re_title = re.sub('[\<\>b/]+', ' ', title)
        	item['title'] = re_title
        	item['link'] = sel.select('link/text()').extract()
        	yield item