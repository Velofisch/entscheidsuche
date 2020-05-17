# -*- coding: utf-8 -*-
import scrapy

class ZhZivstrsSpider(scrapy.Spider):
    name = 'zh_zivstrs'
    allowed_domains = ['gerichte-zh.ch']
    start_urls = ['http://www.gerichte-zh.ch/entscheide/entscheide-suchen.html']
    base_url = 'http://www.gerichte-zh.ch/entscheide/entscheide-drucken.html?tx_frpentscheidsammlung_pi3[entscheidDrucken]='

#        https://stackoverflow.com/questions/35330707/scrapy-handle-302-response-code

    handle_httpstatus_list = [302]

# "http://www.gerichte-zh.ch/entscheide/entscheide-drucken.html?tx_frpentscheidsammlung_pi3[entscheidDrucken]="
# basis des bash-skriptes
# https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy-spider
#    def start_requests(self):
#        yield scrapy.Request('http://www.example.com/1.html', self.parse)

#        https://stackoverflow.com/questions/35330707/scrapy-handle-302-response-code

    def start_requests(self):
#        for i in xrange(1,24000):
        for i in xrange(19000,24000):
            ziel = self.base_url+str(i) 
#            print ziel
            yield scrapy.Request(ziel, self.parse, dont_filter=True)

    def parse(self, response):
        print '-------------------------------------------'
        print "Ergebnis: ", response.status
        print "Headers: ", response.headers
        print '-------------------------------------------'

        if response.status in (302,) and 'Location' in response.headers:
            self.logger.debug("(parse_page) Location header: %r" % response.headers['Location'])
            yield scrapy.Request(
                response.urljoin(response.headers['Location']),
                callback=self.parse)

        item = decision()
        link = response.xpath('//div[@class="pdf"]/p/a/@href').extract_first()
        ref = str(link)
        ref = ref.rsplit('/', 1)[-1]
        link = response.urljoin(link)
        print ref
        print 'LINK: '+link
        print 'REF: '+ref
        print '-------------------------------------------'

        item['referenz'] = ref
        item['file_urls'] = [link]

        yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

