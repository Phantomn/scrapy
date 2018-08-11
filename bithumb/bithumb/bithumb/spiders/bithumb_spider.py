# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bithumb.items import BithumbItem
import pymysql


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
            coinName = sel.xpath('td[@class="click left_l"]/span[@class="tx_coin"]/text()').extract_first()
            if coinName:
                item['coinName'] = coinName
            coinPrice = sel.xpath('td[@class="right click padding_right50 line_td stb"]/strong/text()').extract_first()
            if coinPrice:
                item['coinPrice'] = coinPrice
            if coinName and coinPrice:
                item['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

            '''self.conn = pymysql.connect(
    			user = 'root',
    			password = 'tmdvy123',
    			host = 'localhost',
    			database = 'wordpress',
                use_unicode=True,
    		)
            self.cursor = self.conn.cursor()
            sql = """INSERT INTO cc (name, price, date) VALUES (%s %s %s)"""
            val = item['coinName'], item['coinPrice'], item['date']
            self.cursor.execute(sql, val)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            print("================")'''
            yield item