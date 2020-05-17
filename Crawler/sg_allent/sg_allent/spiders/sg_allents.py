# -*- coding: utf-8 -*-
import scrapy
import re

class SgAllentsSpider(scrapy.Spider):
    name = 'sg_allents'
    allowed_domains = ['sg.ch']
    start_urls = ['https://www.gerichte.sg.ch/g/sitemap_gerichte.html']

# --------------https://stackoverflow.com/questions/45384382/scrapy-select-xpath-with-a-regular-expression
#  -------------------------------- response.xpath('//ul/li/b[text()[re:test(., '^Name.*')]]/../descendant::text()') 

    def parse(self, response):
#        links = response.xpath('//ul/li/a[contains(@href, "dienstleistungen/rechtsprechung")][contains(text(), "Entscheid")]')
#        links = response.xpath('//ul/li/a[contains(@href, "dienstleistungen/rechtsprechung")][re:test(@href, "[-_][0-9][0-9][0-9][0-9][-_]")][contains(text(), "Entscheid")]')
        links = response.xpath('//ul/li/a[contains(@href, "dienstleistungen/rechtsprechung") and contains(@href, "html")][re:test(@href, "[-_][0-9][0-9][0-9][0-9][-_]")]')
 #       links = response.xpath('//ul/li/a[contains(@href, "dienstleistungen/rechtsprechung")][re:test(@href, "[0-9][0-9]")][contains(text(), "Entscheid")]')
        for link in links:
            url = link.xpath('.//@href').extract_first()
            url = response.urljoin(url)
            ref = url.rsplit('/', 1)[-1]

#            print url
#            print ref

            item = decision()
            item['referenz'] = ref
            item['file_urls'] = [url]
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

