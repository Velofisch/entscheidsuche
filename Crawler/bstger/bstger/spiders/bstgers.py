# -*- coding: utf-8 -*-
import scrapy


class BstgersSpider(scrapy.Spider):
    name = 'bstgers'
    allowed_domains = ['https://bstger.weblaw.ch/pdf/']
    start_urls = ['https://bstger.weblaw.ch/pdf']

    def parse(self, response):
        alles = response.xpath('//td/a[contains(@href, "pdf")]')
        for sel in alles:
            referenz = sel.xpath('.//text()').extract_first()
            origurl = sel.xpath('.//@href').extract_first()
            url = str(response.urljoin(origurl))

            item = decision()
            item['url'] = url
            item['referenz'] = referenz
            item['file_urls'] = [url]

            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()
