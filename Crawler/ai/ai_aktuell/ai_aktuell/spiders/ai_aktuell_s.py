# -*- coding: utf-8 -*-
import scrapy

class AiAktuellSSpider(scrapy.Spider):
    name = 'ai_aktuell_s'
    allowed_domains = ['ai.ch']
    start_urls = ['https://www.ai.ch/gerichte/kantonsgericht/rechtsprechung']

    def parse(self, response):
        links = response.xpath('//tr/td/a[contains(@href, "aktuell")]')
        for link in links:
            item = decision()

            url1 = link.xpath('@href').extract_first()
            url = response.urljoin(url1)
#            ref = link.xpath('normalize-space(text())').extract_first().strip()
#            ref =  ref.replace('/','_')
#            ref =  ref.replace(' ','_')

            ref = url.rsplit('/',1)[-1]

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

