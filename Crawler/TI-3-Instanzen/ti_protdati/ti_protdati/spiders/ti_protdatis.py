# -*- coding: utf-8 -*-
import scrapy


class TiProtdatisSpider(scrapy.Spider):
    name = 'ti_protdatis'
    allowed_domains = ['ti.ch']
    start_urls = ['https://www4.ti.ch/can/sgcds/trasparenza/giurisprudenza//']

    def parse(self, response):
        links = response.xpath('//ul/li/a[contains(@href, "pdf")]')
        for link in links:
            url = link.xpath('@href').extract_first()
            url = response.urljoin(url)

#            ref = link.xpath('text()').extract_first()
# Doppelte Bezeichungen
            ref = url.rsplit('/', 1)[-1]
            ref = ref.replace('.','-')
            ref = ref.replace('-pdf','.pdf')
            ref = 'TI-'+ref


#            print 'Link ist: '+url
#            print 'Referenz ist: '+ref
            
            item=decision()
            item['referenz'] = ref
            item['file_urls'] = [url]
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

