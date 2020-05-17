# -*- coding: utf-8 -*-
import scrapy


class ArksSpider(scrapy.Spider):
    name = 'arks'
    allowed_domains = ['ark-cra.ch']
    start_urls = ['http://www.ark-cra.ch/emark/2006.htm',
                  'http://www.ark-cra.ch/emark/2005.htm',
                  'http://www.ark-cra.ch/emark/2004.htm',
                  'http://www.ark-cra.ch/emark/2003.htm',
                  'http://www.ark-cra.ch/emark/2002.htm',
                  'http://www.ark-cra.ch/emark/2001.htm',
                  'http://www.ark-cra.ch/emark/2000.htm',
                  'http://www.ark-cra.ch/emark/1999.htm',
                  'http://www.ark-cra.ch/emark/1998.htm',
                  'http://www.ark-cra.ch/emark/1997.htm',
                  'http://www.ark-cra.ch/emark/1996.htm',
                  'http://www.ark-cra.ch/emark/1995.htm',
                  'http://www.ark-cra.ch/emark/1994.htm',
                  'http://www.ark-cra.ch/emark/1993.htm']

    def parse(self, response):
        links = response.xpath('//tr/td/a[contains(@href, ".htm") and (contains(@href, "19") or contains(@href, "20"))] [not(contains(@href, "mit"))] [not(contains(@href, "englis"))]')
        for link in links:
            url = response.urljoin(link.xpath('@href').extract_first())
            referenz = link.xpath('normalize-space(text())').extract_first().strip().encode('utf-8')

            ref = str(referenz)
            ref = ref.replace('/', '-')
            ref = ref.replace(' ', '')+'.htm'

            item=decision()
            item['referenz'] = ref
            item['url'] = url
            item['file_urls'] = [url]
            yield item
#            self.zaehler = self.zaehler+1

#            print 'URL: '+str(url)
#            print 'Referenz: '+ref

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

