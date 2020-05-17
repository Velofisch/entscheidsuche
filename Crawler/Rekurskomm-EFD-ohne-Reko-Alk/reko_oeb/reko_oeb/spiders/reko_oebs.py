# -*- coding: utf-8 -*-
import scrapy


class RekoOebsSpider(scrapy.Spider):
    name = 'reko_oebs'
    allowed_domains = ['reko-efd.ch']
    start_urls = ['http://www.reko-efd.ch/de/brk/entscheide/index.htm']

    def parse(self, response):
        links = response.xpath('//tr/td/a[contains(@href, "pdf")]')
        for link in links:
            item = decision()

            url = link.xpath('@href').extract_first()
            url = response.urljoin(url)
            ref = link.xpath('normalize-space(text())').extract_first()
            ref =  ref.replace('/','_')
            ref =  ref.replace(' ','_')+'.pdf'
            item['referenz'] = ref
            item['file_urls'] = [url]
#            print url
#            print ref
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

