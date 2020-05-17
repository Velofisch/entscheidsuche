# -*- coding: utf-8 -*-
import scrapy


class NeTriadmsSpider(scrapy.Spider):
    name = 'ne_triadms'
    schleife = 0
    allowed_domains = ['ne.ch']
    start_urls = ['http://jurisprudenceadm.ne.ch/scripts/omnisapi.dll?OmnisPlatform=WINDOWS&WebServerUrl=jurisprudenceadm.ne.ch&WebServerScript=/scripts/omnisapi.dll&OmnisLibrary=JURISWEB&OmnisClass=rtFindinfoWebHtmlService&OmnisServer=JURISWEB,localhost:8000&Aufruf=loadTemplate&cTemplate=search.html&Schema=NE_JURWEB&cSprache=FRE&Parametername=NEJURWEB&nAnzahlTrefferProSeite=5&nSeite=1&bSelectAll=1&bSelectAll2=1']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath=('//div/form/button[@name="evSubmit"]'),
            callback=self.weiter
        )

    def weiter(self, response):

        for sel in response.xpath('//tr/td/a[contains(@href, "refferzeile") and contains(@href, "result")]'):
#            response = response.replace(body=response.body.replace('<br />', '\n'))
#        for sel in response.xpath('//table/tr/td/table/tr/td/table/tr/td/table/tr'):

            url = sel.xpath('.//@href').extract_first()
            url = response.urljoin(url)
#            print 'url: '+url
#            url = sel.xpath('.//td[@class="resultValue"]/a/@href').extract_first()
#            referenz = sel.xpath('.//acronym/text()').extract_first()
            self.schleife = self.schleife+1
            referenz = sel.xpath('normalize-space(span/text())').extract_first().strip()
            referenz = referenz.replace('.', '-')
#            referenz = 'NE-triadm-'+referenz+'-'+str(self.schleife)+'.html'
            referenz = 'NE-triadm-'+referenz+'-'+'.html'
#            print 'Referenz: '+referenz

#            time.sleep(5)

            item = decision()
            item['referenz'] = referenz
            item['file_urls'] = [url]
            yield item

#        next_page = response.xpath('//tr/td/a[//img[contains(@src, "arrow_foward")]]/@href').extract_first()
#        next_page = response.xpath('//tr/td/a[contains(@img, "foward")][contains(@href, "reffer")]/@href').extract_first()
        next_page = response.xpath('//a/img[contains(@src, "arrow_foward.gif")]/../@href').extract_first()
#        next_page = response.urljoin(next_page)
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.weiter, dont_filter=True)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

