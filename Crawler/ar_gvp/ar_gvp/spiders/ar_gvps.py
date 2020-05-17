# -*- coding: utf-8 -*-
import scrapy


class ArGvpsSpider(scrapy.Spider):
    name = 'ar_gvps'
    allowed_domains = ['ar.ch']
    start_urls = ['https://www.ar.ch/verwaltung/kantonskanzlei/rechtsdienst/ausserrhoder-gerichts-und-verwaltungspraxis/']

    def parse(self, response):
#        links = response.xpath('//tr/td/a[contains(@href, "GVP") and contains(text(), "")]')
#        links = response.xpath('//tr/td/a[contains(@href, "GVP")]').re(r'\S*\d\d\d\d')
#        links = response.xpath('//li/a[contains(@href, "juHash")]').re(r'\S*\d\d\d\d')
#        links = response.xpath('//li/a[contains(@title, "GVP")]').re(r'\S*\d\d\d\d')
        links = response.xpath('//li/a[contains(@title, "GVP") and not (contains(@title, "verzeichnis")) and not (contains(@title, "register"))]')
        for link in links:
            item = decision()

            url = link.xpath('@href').extract_first()
            url = response.urljoin(url)
            ref = link.xpath('normalize-space(text())').extract_first()
#            ref =  ref.replace('/','_')
            ref =  ref.replace(' ','-')+'.pdf'
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

