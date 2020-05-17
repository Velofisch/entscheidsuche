# -*- coding: utf-8 -*-
import scrapy

class BsSpider(scrapy.Spider):
    name = 'bs_'
    allowed_domains = ['rechtsprechung.gerichte-bs.ch']
    start_urls = ['https://www.rechtsprechung.gerichte-bs.ch']
    zaehler = 0

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath=('//form[@id="FindinfoSuche"]/button[@name="evSubmit"]'),
            callback=self.weiter
        )

    def weiter(self, response):
        selection = response.xpath('//tr/td/a[contains(@href, "Trefferzeile")]')
        for sel in selection:
            item = decision()
#            ref = sel.xpath('.//span/text()').extract_first().encode('utf-8')
            ref = sel.xpath('.//span/text()').extract_first()
#            ref = str(self.zaehler)+'-'+ref.replace('.', '-')+'.html'
            ref = ref.replace('.', '-')+'.html'
            link = sel.xpath('@href').extract_first()
            link = response.urljoin(link)
            item['url'] = link
            item['referenz'] = ref
            item['file_urls'] = [link]
            self.zaehler = self.zaehler+1
#            print ref
#            print link
            yield item

        next_page = response.xpath('//a/img[contains(@src, "arrow_foward.gif")]/../@href').extract_first()
        if next_page is not None:
#            print '---------------------------'
#            print next_page.encode('utf-8').strip()
#            print '---------------------------'
#            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.weiter)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field() 

