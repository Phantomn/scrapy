# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class BithumbItem(scrapy.Item):
	coinName = scrapy.Field()
	coinPrice = scrapy.Field()
	date = scrapy.Field()
	pass