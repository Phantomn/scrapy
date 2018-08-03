# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bithumb.items import BithumbItem
import mysql.connector


class BithumbSpider(scrapy.Spider):
    name = 'bithumb'
    allowed_domains = ['bithumb.com']
    start_urls = ['https://bithumb.com/'] #, https://www.bithumb.com/tradeview"]

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.driver = webdriver.Firefox(firefox_options=self.options, executable_path='/root/scrapy/bithumb/bithumb/geckodriver')
        print("Firefox Headless Browser Invoked")

    def parse(self, response):
        self.driver.get('https://www.bithumb.com')
        html = self.driver.find_element_by_xpath('//*').get_attribute('outerHTML')
        self.driver.close()
        selector = Selector(text=html)


        for sel in selector.xpath('//table[@id="tableAsset"]/tbody/tr'):
            item = BithumbItem()
            item['coinName'] = sel.xpath('td[@class="click left_l"]/span[@class="tx_coin"]/text()').extract()
            item['coinPrice'] = sel.xpath('td[@class="right click padding_right50 line_td stb"]/strong/text()').extract()
            item['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

            '''self.conn = mysql.connector.connect(
    			user = 'root',
    			password = 'tmdvy123',
    			host = '127.0.0.1',
    			database = 'wordpress',
    		)
            self.cursor = self.conn.cursor()

            self.cursor.execute("INSERT INTO cc (name, price, date) VALUES(\'%s\', \'%s\', \'%s\')" %(item['coinName'], item['coinPrice'], item['date']))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            print("================")'''
            yield item
        print("================")
