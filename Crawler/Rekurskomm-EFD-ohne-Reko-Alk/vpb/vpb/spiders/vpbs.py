# -*- coding: utf-8 -*-
import scrapy

class VpbsSpider(scrapy.Spider):
    name = 'vpbs'
    allowed_domains = ['vpb.admin.ch']
    start_urls = ['http://www.vpb.admin.ch/deutsch/contenu_de.html']

    def parse(self, response):
         ausgang = response.xpath('//a[contains(@href, "heft") or contains(@href, "nouvdoc")]')
         for band in ausgang:
             url = band.xpath('@href').extract_first()
             fullurl = response.urljoin(url)
#             print fullurl
             yield scrapy.Request(url=fullurl, callback=self.weiter)
 
    def weiter(self, response):
        rme = response.xpath('//a[contains(@href, "doc") and contains(@href, "html")]')
        for entsch in rme:
            ref = entsch.xpath('normalize-space(.//text())').extract_first()
            fullref = ref.replace(' ', '-')
            fullref = fullref.replace('.', '-')+'.html'

            link = entsch.xpath('.//@href').extract_first()
            fulllink = response.urljoin(link)
            print fullref
            print fulllink

            item=decision()
            item['referenz'] = fullref
            item['url'] = fulllink
            item['file_urls'] = [fulllink]
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()
             
