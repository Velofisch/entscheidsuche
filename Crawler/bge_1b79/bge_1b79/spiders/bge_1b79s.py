# -*- coding: utf-8 -*-
import scrapy


class Bge1b79sSpider(scrapy.Spider):
    name = 'bge_1b79s'
    allowed_domains = ['servat.unibe.ch']
    start_urls = [
                  'http://www.servat.unibe.ch/dfr/dfr_bge00.html',
                  'http://www.servat.unibe.ch/dfr/dfr_bge01.html',
                  'http://www.servat.unibe.ch/dfr/dfr_bge02.html',
                  'http://www.servat.unibe.ch/dfr/dfr_bge03.html',
                  'http://www.servat.unibe.ch/dfr/dfr_bge04.html',
                  'http://www.servat.unibe.ch/dfr/dfr_bge05.html',
                  'http://www.servat.unibe.ch/dfr/dfr_bge06.html',
                  'http://www.servat.unibe.ch/dfr/dfr_bge07.html'
                 ]

    def parse(self, response):
        alles = response.xpath('//tr/td/a[contains(@href, ".html") or contains(@href, ".pdf")][re:test(@href, "c[0-9]{6}")]')
#        alles = response.xpath('//tr/td/a[contains(@href, ".html") or contains(@href, ".pdf")]')
        for sel in alles:
            url = sel.xpath('@href').extract_first()
            url = response.urljoin(url)
#            print url

#            ersten beiden Ziffern sind roemische fuer das Rechtsgebiet
#            Ziffern drei und vier sind fuer die BGE-Jahreszahl 
#            letzte drei Ziffern sind die Seitenzahlen 

            suf = url.rsplit('.', 1)[-1]
            ref = url.rsplit('.',2)[-2]
            ref = ref.rsplit('/',1)[-1]
            ref = 'BGE-'+ref[3]+ref[4]+'-'+ref[1]+'-'+ref[5]+ref[6]+ref[7]+'.'+suf
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

