# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class GlsSpider(scrapy.Spider):
    name = 'gls'
    allowed_domains = ['gl.ch']
    start_urls = ['https://findinfo.gl.ch']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath=('//tr/td/button[@name="evSubmit"]'),
            callback=self.weiter
        )

    def weiter(self, response):
        response = response.replace(body=response.body.replace('<br />', '\n'))  
        for sel in response.xpath('//table[contains(@class, "result")]'):
            item = decision()
            link = sel.xpath('.//*/a/@href').extract_first()
#            print 'Link: '+link
            ref = sel.xpath('.//*/td[2]/text()[normalize-space()]').extract_first().strip()
            ref = ref.replace('(', '')
            ref = ref.replace(')', '')
            ref = 'GL-'+ref.replace('.', '-')+'.html'
#            print 'Referenz: '+ref
            item['referenz'] = ref
            item['file_urls'] = [link]
            yield item

        next_page = response.xpath('//a/img[contains(@src, "arrow_forward.gif")]/../@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.weiter)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

