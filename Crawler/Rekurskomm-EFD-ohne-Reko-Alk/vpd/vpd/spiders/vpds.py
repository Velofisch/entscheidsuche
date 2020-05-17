# -*- coding: utf-8 -*-
import scrapy

class VpbsSpider(scrapy.Spider):
    name = 'vpds'
    allowed_domains = ['vpb.admin.ch']
    start_urls = ['http://www.vpb.admin.ch/deutsch/cont/aut/aut_1.2.3.5.html']

    def parse(self, response):
        links = response.xpath('//a[contains(text(), "VPB")]')
        for link in links:
            url = response.urljoin(link.xpath('@href').extract_first())
            referenz = link.xpath('normalize-space(text())').extract_first()
            ref = str(referenz)
            ref = ref.replace(' ', '-')
            ref = ref.replace('.', '-')+'.html'

            item=decision()
            item['referenz'] = ref
            item['url'] = url
            item['file_urls'] = [url]
            yield item

#            print 'URL: '+str(url)
#            print 'Referenz: '+ref

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

