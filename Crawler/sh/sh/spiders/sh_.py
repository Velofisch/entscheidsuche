# -*- coding: utf-8 -*-
import scrapy

class ShSpider(scrapy.Spider):
    name = 'shs'
    allowed_domains = ['obergerichtsentscheide.sh.ch']
    start_urls = [
        'http://obergerichtsentscheide.sh.ch/index.php?id=10065', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10066', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10067', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10068', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10069', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10070', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10071', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10072', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10073', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10165', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10178', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10179', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10180', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10185', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10186', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10187', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10189', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10190', 
        'http://obergerichtsentscheide.sh.ch/index.php?id=10192']

    def parse(self, response):
        for sel in response.xpath('//tr/td/p/a'):
            url = response.urljoin(sel.xpath('.//@href').extract_first())
            ref = sel.xpath('.//text()').extract_first()

# ACHTUNG!!!!!!!!!!!!!! https://stackoverflow.com/questions/37925511/error-saving-crawled-page-using-file-urls-and-item-pipelines-missing-scheme-in
# MUSS EINE LISTE SEIN - ALSO ECKIGE KLAMMERN

            ref = ref.replace('.', '-')
            ref = ref.replace('/', '-')
            ref = ref.replace(' ', '-')
            ref = ref.replace('--', '-')+'.pdf'

            item = decision()
#            item['url'] = url            
            item['file_urls'] = [url]            
            item['referenz'] = ref

            print '-------------------------------------------'
            print url
            print ref
            print  '-------------------------------------------'

            yield item            

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()


