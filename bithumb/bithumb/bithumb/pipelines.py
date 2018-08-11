# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymysql
from bithumb.items import BithumbItem

class BithumbJsonPipeline(object):
    def __init__(self):
    	self.file = codecs.open("bithumb.json", "wb", encoding='utf-8')

    def process_item(self, item, spider):
    	line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    	if item:
    		#print ("item :", item.keys())
    		self.file.write(line)
    	return item

class BithumbSQLPipeline(object):
	def __init__(self):
		self.connection = pymysql.connect(host="localhost", user="root", passwd="tmdvy123", db="wordpress", charset="utf8", use_unicode=True)
		self.cursor = self.connection.cursor()

	def process_item(self, item, spider):
		if item:
			query = '''INSERT INTO cc (name, price, date) VALUES (%s, %s, %s)'''
			value = (item['coinName'].encode('utf-8')),\
					(item['coinPrice'].encode('utf-8')),\
					(item['date'].encode('utf-8'))
			self.cursor.execute(query, value)
			self.connection.commit()
		return item

	def close_spider(self, spider):
		self.cursor.close()
		self.connection.close()