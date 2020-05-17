# -*- coding: utf-8 -*-
import scrapy
from bl.items import BlItem

class BssSpider(scrapy.Spider):
    name = 'bls'
    allowed_domains = ['baselland.ch']
    start_urls = ['https://www.baselland.ch/politik-und-behorden/gerichte/rechtsprechung/kantonsgericht/chronologische-anordnung/']

    def parse(self, response):
        for quote in response.xpath('//div/div/*/a[contains(@href, "chrono")]'):
            Jahrgangssuche = quote.xpath('.//@href').extract_first()
            yield scrapy.Request(Jahrgangssuche, callback=self.jahre)


    def jahre(self, response):
        for entscheid in response.xpath('//tr/td/div/a[contains(@href, "kantonsgericht")]'):
            item = decision()
            link = entscheid.xpath('.//@href').extract_first().encode('utf-8')
            ref = str(link)
#            ref = ref.rsplit('/', 1)[-1]

            if 'pdf' in ref.rsplit('.', 1)[-1]:
                referenz = ref.rsplit('/', 1)[-1]
            else:
                referenz = 'BL-'+ref.rsplit('/', 2)[-2]+'-'+ref.rsplit('/', 2)[-1]+'.html'
#                print 'Referenz: '+referenz

            item['referenz'] = referenz
            item['file_urls'] = [link]
#            print 'ref: '+ref
#            print 'Referenz: '+referenz
#            print 'Link: '+link
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

