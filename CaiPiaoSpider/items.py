# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import peewee

class CaipiaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    issue = scrapy.Field()
    reds = scrapy.Field()
    blue = scrapy.Field()
    url = scrapy.Field()
    sale = scrapy.Field()
    residue = scrapy.Field()
    prize_1 =scrapy.Field()
    prize_2 =scrapy.Field()
    prize_3 =scrapy.Field()
    prize_4 =scrapy.Field()
    prize_5 =scrapy.Field()
    prize_6 =scrapy.Field()


