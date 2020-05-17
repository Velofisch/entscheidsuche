# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BlItem(scrapy.Item):
    # define the fields for your item here like:
    Entscheiddatum = scrapy.Field()
    Rubrum = scrapy.Field()
    Rechtsgebiet = scrapy.Field()
    Gericht = 'Kantonsgericht BL'
    Betreff = scrapy.Field()
    url = scrapy.Field()
#    pass
