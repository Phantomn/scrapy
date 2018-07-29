# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import codecs
import json

class NaverCsvPipeline(object):

	def __init__(self):
		self.csvwriter = csv.writer(codecs.open('naver.csv', 'wb', encoding='euc-kr'))

	def process_item(self, item, spider):
		#print (item['title'][0])
		self.csvwriter.writerow([item['title'], item['link'][0]])
		return item

class NaverJsonPipeline(object):

	def __init__(self):
		self.file = codecs.open('naver.json', 'wb', encoding='euc-kr')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False) + "\n"
		self.file.write(line)
		return item