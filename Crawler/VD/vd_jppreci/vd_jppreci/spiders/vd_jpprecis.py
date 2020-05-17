# -*- coding: utf-8 -*-
import scrapy


class VdJpprecisSpider(scrapy.Spider):
    name = 'vd_jpprecis'
    allowed_domains = ['www.vd.ch']
    start_urls = ['https://www.vd.ch/themes/etat-droit-finances/protection-des-donnees-et-transparence/acces-aux-documents-officiels/jurisprudence/']

    def parse(self, response):
        urls = response.xpath('//div/p/a[contains(@href, "omnis")]')
        for url in urls:
            item = decision()
            link = url.xpath('.//@href').extract_first()
            ref = url.xpath('.//text()').extract_first().encode('utf-8')
            ref = str(ref)
            ref = ref.replace('.', '-')+'.html'

#            print link
#            print ref
#            print '----------------'

            item['referenz'] = ref
            item['file_urls'] = [link]
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()


