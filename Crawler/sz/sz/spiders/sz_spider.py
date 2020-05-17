# -*- coding: utf-8 -*-
import scrapy

class SzSpiderSpider(scrapy.Spider):
    name = 'sz_spider'
    allowed_domains = ['kgsz.ch']
    start_urls = ['http://www.kgsz.ch/rechtsprechung']
    zaehler = 0
    def parse(self, response):
        for sel in response.xpath('//li[@class="li-pdf"]/a'):
           item = decision()
           link = sel.xpath('.//@href').extract_first()
           link = response.urljoin(link)
           name = sel.xpath('.//text()').extract_first().encode('utf-8')
           name = name.replace('.', '')
           name = name.replace(' ', '-')+'.pdf'
           print 'Link: '+link
           print 'Titel: '+name
           self.zaehler = self.zaehler+1
           print 'Zaehler: ------------------'+str(self.zaehler)
           item['referenz'] = name
           item['file_urls'] = [link]
           yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field() 
