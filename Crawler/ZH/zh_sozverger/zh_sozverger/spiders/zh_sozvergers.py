# -*- coding: utf-8 -*-
import scrapy
import time

class ZhSozvergersSpider(scrapy.Spider):
    name = 'zh_sozvergers'
    allowed_domains = ['sozialversicherungsgericht.zh.ch']
    start_urls = ['http://www.sozialversicherungsgericht.zh.ch/index.php/rechtsprechung-sp-1726307829']
    base_url_1 = 'http://findex.sozialversicherungsgericht.zh.ch/c050018/svg/findexweb.nsf/$$Search/?SearchView&Query=%5BForm%5D="Gerichtsurteil"+AND+%5BProzessnummer%5D='
    base_url_2 = '&SearchOrder=4&SearchMax=10000&SearchWV=FALSE&SearchThesaurus=FALSE&squerystring=&sprozessnr='
    base_url_3 = '&sdatumvornach=2&sdatum=&srechtsgebiet=-Alle-'
    start_jahr = 1994

# http://findex.sozialversicherungsgericht.zh.ch/c050018/svg/findexweb.nsf/$$Search/?SearchView&Query=%5BForm%5D="Gerichtsurteil"+AND+%5BProzessnummer%5D=1994&SearchOrder=4&SearchMax=10000&SearchWV=FALSE&SearchThesaurus=FALSE&squerystring=&sprozessnr=1994&sdatumvornach=2&sdatum=&srechtsgebiet=-Alle-
    def parse(self, response):
# Festlegen des aktuellen Jahres
        end_jahr = int(time.strftime('%Y'))
# --------------- https://www.python-kurs.eu/for-schleife.php
        for i in xrange(self.start_jahr, end_jahr):
            ausgangspunkt = self.base_url_1+str(i)+self.base_url_2+str(i)+self.base_url_3 

            yield scrapy.Request(url=ausgangspunkt, callback=self.weiter)
# ACHTUNG: Dauert teilweise mehrere Sekunden, bis alle records aufgelistet sind

    def weiter(self, response):
        links = response.xpath('//tr/td/font/a')
        for link in links:
            item = decision()
            url = response.urljoin(link.xpath('.//@href').extract_first())
            ref = link.xpath('.//text()').extract_first()+'.html'
#            print 'LINK: '+url
#            print 'REF: '+ref

            item['referenz'] = ref
            item['file_urls'] =[url]
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

