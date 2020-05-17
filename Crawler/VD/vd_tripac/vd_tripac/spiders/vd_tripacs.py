# -*- coding: utf-8 -*-
import scrapy


class VdTripacsSpider(scrapy.Spider):
    name = 'vd_tripacs'
    allowed_domains = ['vd.ch']
    start_urls = ['https://www.vd.ch/themes/justice/jurisprudence-et-lois/jurisprudence-du-tribunal-cantonal-et-du-tripac/jurisprudence-du-tripac/']

    def parse(self, response):
        urls = response.xpath('//div/ul/li/a[contains(@href, "pdf")]')
        for url in urls:
            item = decision()
            link = url.xpath('.//@href').extract_first()
#            ref = url.xpath('.//text()').extract_first()
            ref = str(link)
            ref = ref.rsplit('/',1)[-1]
            ref = ref.rsplit('_',1)[-1]
            ref = ref.replace('.', '-', 1)

#            print link
#            print ref
#            print '----------------'

            item['referenz'] = ref
            item['file_urls'] = [link]
            yield item



class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field() 
