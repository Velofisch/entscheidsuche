# -*- coding: utf-8 -*-
import scrapy
import os.path
import time
import unidecode 
import codecs

class BgerlesSpider(scrapy.Spider):
    name = 'bgerles'
    allowed_domains = ['bger.ch']
    start_urls = ['https://www.bger.ch/ext/eurospider/live/de/php/clir/http/index_atf.php?lang=de']
#    pfad = '/home/peter/testumgebung/files/entscheide/bund/bger/bge_test/'
    pfad = '/home/peter/testumgebung/files/entscheide/bund/bger/bge/'

    def parse(self, response):
        baende = response.xpath('//tr/td/a[contains(@href, "index_atf")]')
        for entscheid in baende:
            pfad = entscheid.xpath('.//@href').extract_first()
# TEMP -----------------------------------------------------------------------------------
#            print pfad
#            print '---------------------------------------------------'
            yield scrapy.Request(url=pfad, callback=self.band)

    def band(self, response):
        le = response.xpath('//div[@class="eit"]/ol/li/a')
        for singlele in le:

#            item = decision()
            url = singlele.xpath('.//@href').extract_first()
#            referenz1 = singlele.xpath('.//text()').extract_first()
#            referenz = referenz1.replace(" ", "-")
#            item['file_urls'] = [url]
#            item['referenz'] = referenz
#            yield item 

# TEMP -----------------------------------------------------------------------------------
#            print url
#            print '---------------------------------------------------'


# TEMP -----------------------------------------------------------------------------------
            yield scrapy.Request(url=url, callback=self.entscheid)





    def entscheid(self, response):
# ----------i https://stackoverflow.com/questions/11252407/xpath-to-extract-text-after-br-tags-in-r
#        ref1 = response.xpath('//div[contains(text(), "Urteilskopf") and contains(@class, "big bold")]/text()').extract_first()
        ref2 = response.xpath('//div[contains(text(), "Urteilskopf") and contains(@class, "big bold")]/following-sibling::br/following-sibling::text()').extract_first().encode('utf-8')
# --- https://stackoverflow.com/questions/10413649/xpath-to-get-all-the-childrens-text

        html2stern = response.xpath('//div[@class="main"]/div/div/div[@class="content"]/*').extract()

#        [x.decode('utf-8') for x in html2stern]
#             https://www.html-seminar.de/befehlsuebersicht.htm

#        h2s = '<head><meta charset="UTF-8"><title>BGE</title></head>'.encode('utf-8')
        h2s = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"><title>BGE '+ref2+'</title></head><body><h3>'+ref2+'</h3>'.encode('utf-8')

        for x in html2stern:
#            x = unidecode.unidecode(x)
            x = x.encode('utf-8')
            h2s +=x
            print x

        h2s +='</body></html>'.encode('utf-8')
        fid = 'BGE-'+ref2.replace(' ', '-')+'.html'

#        print '----------------------------------------------' 

# https://www.datacamp.com/community/tutorials/reading-writing-files-python

        if os.path.isfile(self.pfad+fid):
            self.logger.info('CHECK: File existiert.')
            pass
        else:
#            with codecs.open(os.path.join(self.pfad+fid), 'w', codecs.encode('utf-8')) as f:
            with open(os.path.join(self.pfad+fid), 'wb') as f:
#                f.write(html2stern)
                f.write(h2s)

# ----------- https://stackoverflow.com/questions/7123387/should-i-create-pipeline-to-save-files-with-scrapy
    def save_html(self, response):
        path = self.get_path(response.url)
        with open(path, "wb") as f:
            f.write(response.body)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()
   

