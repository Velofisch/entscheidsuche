# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class decision(scrapy.Item):
    url = scrapy.Field()
    betreff = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()
    entscheiddatum = scrapy.Field()
    bestimmungen = scrapy.Field()
#    pass

#class ShItem(scrapy.Item):
#    # define the fields for your item here like:
#    # name = scrapy.Field()
#    pass
