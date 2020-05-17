# -*- coding: utf-8 -*-
import scrapy


class ZhKassgersSpider(scrapy.Spider):
    name = 'zh_kassgers'
    allowed_domains = ['gerichte-zh.ch']
    start_urls = ['http://www.gerichte-zh.ch/entscheide/kassationsgericht-rb/entscheide.html']

    def parse(self, response):
        jg = response.xpath('//div/p/a[contains(@href, "Kassationsgericht")]')
        for band in jg:
            item = decision()
            link = band.xpath('.//@href').extract_first()
            link = response.urljoin(link)
            ref = band.xpath('.//text()').extract_first()
            ref = 'ZH-KassGer-'+ref+'.pdf'
            print link
            print ref
            item['referenz'] = ref
            item['file_urls'] = [link]
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

