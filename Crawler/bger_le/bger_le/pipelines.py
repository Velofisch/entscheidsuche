# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import string
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request

class BgerLePipeline(object):
    def process_item(self, item, spider):
        return item

#class MyFilesPipeline(FilesPipeline):
#    def file_path(self, request, response=None, info=None):
#        return string.split(request.url, '/')[-1]



class MyFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
#        for datei_url in item['image_urls']:
#           yield Request(datei_url, meta={'item': item})
        datei_url = item['file_urls'][0]
        yield scrapy.Request(datei_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        datei_name = item['referenz']+'.html'
#        image_guid = request.url.split('/')[-1]
#        datei_name = item['image_titles']+image_guid[-8:]
        return datei_name

#
