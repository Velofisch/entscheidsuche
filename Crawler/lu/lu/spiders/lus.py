# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import unidecode

class LusSpider(scrapy.Spider):
    name = 'lus'
    allowed_domains = ['gerichte.lu.ch']
    start_urls = ['https://gerichte.lu.ch/recht_sprechung/lgve']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath=('//*[@id="maincontent_1_btnSearch"]'),
            callback=self.weiter
        )

    def weiter(self, response):
        for sel in response.xpath('//tr/td/a[contains(@href, "lgve")]'):
            item = decision()
            link = sel.xpath('@href').extract_first()
            url = response.urljoin(link)
            referenz = sel.xpath('normalize-space(.//text())').extract_first().encode('utf-8').strip()
            ref = str(referenz)
            ref = ref.replace('/','-')
            ref = unidecode.unidecode(ref)
            ref = 'LU-'+ref.replace(' ', '-')+'.html'
#            print 'URL: '+url
#            print 'Referenz: '+ref

            item['referenz'] = ref
            item['file_urls'] = [url]

            yield item

# https://stackoverflow.com/questions/18810850/scrapy-next-button-uses-javascript
# http://www.harman-clarke.co.uk/answers/javascript-links-in-scrapy.php
        yield FormRequest.from_response(response,
        formdata={'maincontent_1$dprJurisdictions$ctl02$ctl00': ''},
        callback = self.weiter,
        dont_click = True)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

