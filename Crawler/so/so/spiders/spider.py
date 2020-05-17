# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    zaehler = 0
    allowed_domains = ['gerichtsentscheide.so.ch']
    start_urls = ['https://gerichtsentscheide.so.ch/cgi-bin/nph-omniscgi.exe?OmnisPlatform=WINDOWS&WebServerUrl=https://gerichtsentscheide.so.ch&WebServerScript=/cgi-bin/nph-omniscgi.exe&OmnisLibrary=JURISWEB&OmnisClass=rtFindinfoWebHtmlService&OmnisServer=7001&Aufruf=home&Template=home.html&Schema=JGWEB&cSprache=DE&Parametername=WEB&nAnzahlTrefferProSeite=5&nSeite=1&bInstanzInt=all/']

    def parse(self, response):
#        for quote in response.xpath('//tr/td/a/img[contains(@alt, "document.gif")]'):
        for quote in response.xpath('//tr[1]/td[2]'):
            item = decision()
#            link = quote.xpath('../@href').extract_first(),
            link = quote.xpath('.//a/@href').extract_first()
#            print link
#            ref = quote.xpath('.//a/span/text()').extract_first()
#            ref1 = quote.xpath('.//a/img/following-sibling::span/text()').extract_first()
#            ref = quote.xpath('.//a/following-sibling::span/text()').extract_first()
            ref = quote.xpath('.//a/span/text()[normalize-space()]').extract_first()
            ref1 = str(ref)
            ref2 = ref1.replace('(', '')
            ref3 = ref2.replace(')', '')
#            ref4 = 'SO-'+str(self.zaehler)+'-'+ref3.replace('.', '-')+'.html'
            ref4 = 'SO-'+ref3.replace('.', '-')+'.html'

#            print ref4
#            print '---------------------'
#                 'Referenz': quote.xpath('//a/span/text()').extract()
            item['referenz'] = ref4
            item['file_urls'] = [link]

            self.zaehler = self.zaehler+1

            yield item

        next_page_url = response.xpath('//a/img[contains(@src, "arrow_foward.gif")]/../@href').extract_first().encode('utf-8')
        next_page_url = str(next_page_url)
#        next_page_url = response.xpath('//a/href/ & //a/img[contains(@src, "arrow_foward.gif")]').extract_first()
#        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None: 
            yield scrapy.Request(response.urljoin(next_page_url))
#            yield scrapy.Request(next_page_url)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

