# -*- coding: utf-8 -*-
import scrapy


class TiConmagsSpider(scrapy.Spider):
    name = 'ti_conmags'
    allowed_domains = ['ti.ch']
    start_urls = ['https://www4.ti.ch/poteri/giudiziario/consiglio-della-magistratura/giurisprudenza/']

    def parse(self, response):
        links = response.xpath('//ul/li/a[contains(@href, "PDF")]')
        for link in links:
            url = link.xpath('@href').extract_first()
            url = response.urljoin(url)

#            ref = link.xpath('text()').extract_first()
            ref = url.rsplit('/', 1)[-1]
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


