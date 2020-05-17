# -*- coding: utf-8 -*-
import scrapy

class VdTnSSpider(scrapy.Spider):
    name = 'vd_tn_s'
    allowed_domains = ['www.vd.ch']
    start_urls = ['https://www.vd.ch/toutes-les-autorites/tribunal-neutre/']

    def parse(self, response):
        urls = response.xpath('//div/ol/li/a[contains(@href, "pdf")]')
        for url in urls:
            item = decision()
            link = url.xpath('.//@href').extract_first()
#            ref = url.xpath('.//text()').extract_first()
            ref = str(link)
            ref = ref.rsplit('/',1)[-1]

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

