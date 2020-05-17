# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import string
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request

class VdVwvfgerPipeline(object):
    def process_item(self, item, spider):
        return item

class MyFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        datei_url = item['file_urls'][0]
        yield scrapy.Request(datei_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        datei_name = item['referenz']
        return datei_name
