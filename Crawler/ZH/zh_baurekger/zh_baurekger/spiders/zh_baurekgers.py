# -*- coding: utf-8 -*-
import scrapy
# from urllib.parse import urljoin
from urlparse import urljoin

class ZhBaurekgersSpider(scrapy.Spider):
    name = 'zh_baurekgers'
    allowed_domains = ['baurekursgericht-zh.ch']
    start_urls = ['http://entscheiddb.baurekursgericht-zh.ch/ruling/search?department_id=0&number=&year=&submit=Suchen/']
    url_base = 'http://entscheiddb.baurekursgericht-zh.ch/'
#    start_urls = ['entscheiddb.baurekursgericht-zh.ch']

    def parse(self, response):
        for sel in response.xpath('//div/div/a[contains(@href, "pdf")]'):
            item = decision() 
            link = sel.xpath('@href').extract_first()
            ref = str(link)
            ref = ref.rsplit('/', 1)[-1]
#            print 'Link: '+link
#            print 'REf: '+ref
            item['referenz'] = ref
            item['file_urls'] = [link]
#            print '------------------------------------------'
            yield item 

        next_page = response.xpath('//div/ul[@class="pagination"]/li/a[contains(@href, "page")][contains(text(), "Vor")]').extract_first()
#        next_page = response.xpath('//div/ul[@class="pagination"]/li/a[contains(@text(), "Vor")]').extract_first()
#        print "Next_page 1: "+next_page

        if next_page is not None:
            nepa = str(next_page)
            nepa = self.url_base+nepa.split('"', 2)[1]
#            next_page = self.url_base+str(next_page)
#            ulla = urljoin(self.url_base, next_page)
#            print "Next_page 2: "+next_page
#            print "Ulla 2: "+ulla
#            print "nepa 2: "+nepa
            yield scrapy.Request(nepa, callback=self.parse)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field() 
