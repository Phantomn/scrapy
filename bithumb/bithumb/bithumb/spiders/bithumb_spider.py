# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import datetime
from selenium import webdriver
from bithumb.items import BithumbItem
import mysql.connector


class BithumbSpider(scrapy.Spider):
    name = 'bithumb'
    allowed_domains = ['bithumb.com']
    start_urls = ['https://bithumb.com/'] #, https://www.bithumb.com/tradeview"]

    def __init__(self):
    	self.browser = webdriver.Firefox()

    def parse(self, response):
    	self.browser.get(response.url)
    	html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
    	self.browser.close()
    	selector = Selector(text=html)

    	for sel in selector.xpath('//table[@id="tableAsset"]/tbody/tr'):
    		item = BithumbItem()
    		item['coinName'] = sel.xpath('td[@class="click left_l"]/span[@class="tx_coin"]/text()').extract()[0]
    		item['coinPrice'] = sel.xpath('td[@class="right click padding_right50 line_td stb"]/strong/text()').extract()[0]
    		item['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    		self.conn = mysql.connector.connect(
    			user = 'root',
    			password = 'tmdvy123',
    			host = '127.0.0.1',
    			database = 'wordpress',
    		)
    		self.cursor = self.conn.cursor()

    		self.cursor.execute("INSERT INTO cc VALUES(\'%s\', \'%s\', \'%s\')" %(item['coinName'], item['coinPrice'], item['date']))
    		self.conn.commit()
    		self.cursor.close()
    		self.conn.close()
    		print("================")

    		yield item
    	print("================")