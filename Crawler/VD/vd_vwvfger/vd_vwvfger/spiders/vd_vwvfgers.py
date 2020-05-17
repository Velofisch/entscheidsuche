# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
import logging


class VdVwvfgersSpider(scrapy.Spider):
    download_timeout = 50
    name = 'vd_vwvfgers'
    allowed_domains = ['vd.ch']
    start_urls = ['http://www.jurisprudence.vd.ch/scripts/nph-omniscgi.exe?OmnisPlatform=WINDOWS&WebServerUrl=www.jurisprudence.vd.ch&WebServerScript=/scripts/nph-omniscgi.exe&OmnisLibrary=JURISWEB&OmnisClass=rtFindinfoWebHtmlService&OmnisServer=7001&Aufruf=loadTemplate&cTemplate=search/standard/search.fiw&Schema=VD_TA_WEB&cSprache=FRE&Parametername=WWW_V4']
    zaehler = 0

    def parse(self, response):

        return scrapy.FormRequest.from_response(
            response,
            formxpath=('//tr/td/button[@value="submit"][@class="suchen"]'),
            callback=self.weiter
        )

    def weiter(self, response):
#        response = response.replace(body=response.body.replace('<br />', '\n'))
        for sel in response.xpath('//tr/td/a[contains(@href, "zeile")]'):
#            time.sleep(1) 
            item = decision()
            link = sel.xpath('.//@href').extract_first()
            ref = sel.xpath('.//text()[normalize-space()]').extract_first().strip()
            ref = ref+'.html'
#            print 'Referenz: '+ref
#            print 'Link: '+link
            item['referenz'] = ref
            item['file_urls'] = [link]
            yield item

        next_page = response.xpath('//a[contains(@href, "Seite")][contains(text(), "&gt") or contains(text(), ">")]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.weiter)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

