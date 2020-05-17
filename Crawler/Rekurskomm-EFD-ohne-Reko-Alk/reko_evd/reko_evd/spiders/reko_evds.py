# -*- coding: utf-8 -*-
import scrapy


class RekoEvdsSpider(scrapy.Spider):
    name = 'reko_evds'
    zaehler = 1
    allowed_domains = ['reko-evd.ch']
    start_urls = ['http://www.reko-evd.ch/de/entscheide/index.htm']

    def parse(self, response):
        links = response.xpath('//a[contains(@href, "Files")]')
        for link in links:
            url = response.urljoin(link.xpath('@href').extract_first())
            referenz = link.xpath('normalize-space(text())').extract_first().encode('utf-8')

            ref = str(referenz)
            ref = ref.replace('/', '-')
            ref = ref+'.pdf'
#            ref = str(self.zaehler)+'-'+ref+'.html'

            item=decision()
            item['referenz'] = ref
            item['url'] = url
            item['file_urls'] = [url]
            yield item
            self.zaehler = self.zaehler+1

#            print 'URL: '+str(url)
#            print 'Referenz: '+ref

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

