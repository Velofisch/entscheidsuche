# -*- coding: utf-8 -*-
import scrapy


class ZhZivstrNeueentsSpider(scrapy.Spider):
    name = 'zh_zivstr_neueents'
    allowed_domains = ['http://gerichte-zh.ch']
    start_urls = ['http://www.gerichte-zh.ch/entscheide/entscheide-neuheiten.html']

    def parse(self, response):
        tage = response.xpath('//div[@class="neuheit"]/a')
        tage = response.xpath('//div[@class="neuheit"]/a[1]')
        for tag in tage:
            verweis = tag.xpath('.//@href').extract_first()
            verweis = response.urljoin(verweis)
            print verweis
            yield scrapy.Request(url=verweis, callback=self.band, dont_filter=True)

    def band(self, response):
        links = response.xpath('//div/p/a[@class="pdf-icon"]')
        for link in links:
            url = link.xpath('.//@href').extract_first()
            url = response.urljoin(url)
            print url

            ref = str(url)
            ref = ref.rsplit('/',1)[-1]
            print ref

            item = decision()
            item['referenz'] = ref
            item['file_urls'] = [url]
            yield item


class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

