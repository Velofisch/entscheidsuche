# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class TiSentenzesSpider(scrapy.Spider):
    name = 'ti_sentenzes'
    allowed_domains = ['sentenze.ti.ch']
    start_urls = ['http://www.sentenze.ti.ch/cgi-bin/nph-omniscgi?OmnisPlatform=WINDOWS&WebServerUrl=www.sentenze.ti.ch&WebServerScript=/cgi-bin/nph-omniscgi&OmnisLibrary=JURISWEB&OmnisClass=rtFindinfoWebHtmlService&OmnisServer=JURISWEB,193.246.182.54:6000&Aufruf=loadTemplate&cTemplate=cerca.fiw&Schema=TI_WEB&cLanguage=ITA&Parametername=WWWTI&cSuchstringZiel=testo']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath=('//input[@id="cButtonAction"]'),
            callback=self.weiter
        )

    def weiter(self, response):
# in Glarner Original        response = response.replace(body=response.body.replace('<br />', '\n'))
        alles = response.xpath('//tr/td/a[contains(@href, "Trefferzeile")]')
        for sel in alles:
            item = decision()
            link = sel.xpath('@href').extract_first()
#            print 'Link: '+link
#            ref = sel.xpath('text()').extract_first().encode('utf-8').strip()
#            ref = ref.replace('(', '')
#            ref = ref.replace(')', '')
#            ref = 'GL-'+ref.replace('.', '-')+'.html'
#            print 'Referenz: '+ref
            alter = link
            alter = alter.rsplit('=', 4)[-4]
            alter = 'TI-sentenze-'+alter.rsplit('&', 1)[-2]+'.html'
#            print 'Referenz: ALTERNATIVE: '+alter
            item['referenz'] = alter
            item['file_urls'] = [link]
            yield item

#        next_page = response.xpath('//a[contains(@href, "TrefferProSeite") and contains(@href, ">")]/@href').extract_first()
#        next_page = response.xpath('//tr/td/a[contains(@href, ">") or contains(@href, "&amp;")]/@href').extract_first()
        next_page = response.xpath('//tr/td/a[contains(@href, "Seite")][contains(text(), ">") or contains(@href, "&gt")]/@href').extract_first()
        if next_page is not None:
            print 'Nextpage ist: '+next_page.encode('utf-8')
            yield scrapy.Request(url=next_page, callback=self.weiter)
        else:
            print 'Nextpage ist: '+next_page.encode('utf-8')

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()


