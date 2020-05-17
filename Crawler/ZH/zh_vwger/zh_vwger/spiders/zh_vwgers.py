# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

# --------------- siehe Glarus

class ZhVwgersSpider(scrapy.Spider):
    name = 'zh_vwgers'
    allowed_domains = ['djiktzh.ch']
    start_urls = ['http://www.vgrzh.djiktzh.ch/cgi-bin/nph-omniscgi.exe?OmnisPlatform=WINDOWS&WebServerUrl=www.vgrzh.djiktzh.ch&WebServerScript=/cgi-bin/nph-omniscgi.exe&OmnisLibrary=JURISWEB&OmnisClass=rtFindinfoWebHtmlService&OmnisServer=JURISWEB,127.0.0.1:7000&Aufruf=loadTemplate&cTemplate=standard/search.fiw&Schema=ZH_VG_WEB&cSprache=GER&Parametername=WWW']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath=('//tr/td/button[@class="suchen"]'),
            callback=self.weiter
        )

    def weiter(self, response):
        for sel in response.xpath('//tr/td/a[contains(@href, "Trefferz")]'):
            item = decision()
            link = sel.xpath('.//@href').extract_first()
            ref = sel.xpath('.//font/text()').extract_first().strip()
            ref = ref.replace('.', '-')+'.html'

            print ref
            print link

            item['referenz'] = ref
            item['file_urls'] = [link]
            yield item

        next_page = response.xpath('//a[contains(@href, "Seite")][contains(text(), "&gt") or contains(text(), ">")]/@href').extract_first()
        if next_page is not None:
            print 'next page ist: '+next_page
            yield scrapy.Request(url=next_page, callback=self.weiter)

#        print '-----------------------------------------------'
#        print 'next page ist: '+next_page

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

