# -*- coding: utf-8 -*-
import scrapy
import unidecode
import re

class VdTricansSpider(scrapy.Spider):
    name = 'vd_tricans'
    allowed_domains = ['vd.ch']
    start_urls = ['https://www.findinfo-tc.vd.ch/justice/findinfo-pub/internet/SimpleSearch.action']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
#            formxpath=('//*/tr/td/button[@value="Suchen"][@class="button"][@name="search"]'),
            formxpath=('//tr/td/input[@class="button"][@name="search"]'),
            callback=self.weiter
        )

    def weiter(self, response):
#        response = response.replace(body=response.body.replace('<br />', '\n'))
        for sel in response.xpath('//tr/td/a[contains(@href, "dossier")]'):
#            time.sleep(1)
            link = sel.xpath('.//@href').extract_first()
            link = response.urljoin(link) 

            yield scrapy.Request(url=link, callback=self.nochweiter)

        next_page = response.xpath('//a[contains(@href, "page")][contains(text(), "&gt") or contains(text(), ">")]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.weiter)

    def nochweiter(self, response):
#        for url in response.xpath('//frame[contains(@src, "html")]]'):
        for url in response.xpath('//frame[contains(@src, "html")]'):
            item = decision()
            sprung = url.xpath('//frame[contains(@src, "html")]/@src').extract_first() 
            sprung = response.urljoin(sprung)
#   <title>Entscheid Suche: Arrêt / 2018 / 454</title>
            ref = response.xpath('//title[normalize-space()]').extract_first().strip()  
            ref = ref.rsplit(':',1)[-1]
            ref = ref.replace(' ','')
            ref = ref.replace('/','-')
            ref = ref.rsplit('<',1)[-2]
            ref = 'VD-KG-'+ref+'.html'
#            ref = re.sub('[^A-Za-z0-9\-]+', '', ref)
            ref = unidecode.unidecode(ref)
#            print 'Referenz: '+ref
#            print 'Link: '+sprung
            item['referenz'] = ref
            item['file_urls'] = [sprung]
            yield item


class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

