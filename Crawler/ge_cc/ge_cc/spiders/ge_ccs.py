# -*- coding: utf-8 -*-
import scrapy


class GeCcsSpider(scrapy.Spider):
    name = 'ge_ccs'
    allowed_domains = ['justice.geneve.ch']
    start_urls = ['http://justice.geneve.ch/tdb/Decis/CJ/ACJC/acjc.tdb?SFT=&S=*']

    def parse(self, response):
        alles = response.xpath('//div/div/b/a')
        for sel in alles:
            link = sel.xpath('.//@href').extract_first()
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.weiter)

        next_page = response.xpath('//a[contains(text(), "Suivant")]/@href').extract_first()
        next_page = response.urljoin(next_page)
#        print next_page
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def weiter(self, response):
        url = response.xpath('//tr/td/div/a/@href').extract_first().encode('utf-8')
        url = response.urljoin(url)
        ref = url.rsplit('/', 1)[-1]
#        print url
#        print ref

        item = decision()
        item['referenz'] = ref
        item['file_urls'] = [url]
        yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()



