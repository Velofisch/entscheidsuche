# -*- coding: utf-8 -*-
import scrapy
# from ai.items import AiItem

class AiSpiderSpider(scrapy.Spider):
    name = 'ai_spider'
    allowed_domains = ['ai.ch']
    start_urls = ['https://www.ai.ch/themen/staat-und-recht/veroeffentlichungen/verwaltungs-und-gerichtsentscheide']

    def parse(self, response):
        for sel in response.xpath('//tr/td/span/a[contains(text(), "entschei")]'):
            item = decision()
#            ref = sel.xpath('.//text()').extract_first()
            ref = sel.xpath('.//text()').extract_first()
            ref = ref.replace(' ', '-')+'.pdf'
            item['referenz'] = ref
            link = response.urljoin(sel.xpath('@href').extract_first())
            item['file_urls'] = [link]
#            print link
#            print ref
#            print '---------------------------------------'

            yield item


class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

