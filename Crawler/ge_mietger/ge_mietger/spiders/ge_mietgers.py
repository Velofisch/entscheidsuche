# -*- coding: utf-8 -*-
import scrapy
import os.path

class GeMietgersSpider(scrapy.Spider):
    name = 'ge_mietgers'
    pfad = '/home/peter/testumgebung/files/entscheide/kantone/ge_mietger/'
    allowed_domains = ['ge.ch']
    start_urls = ['http://ge.ch/justice/donnees/tdb/pjdoc/pjdoc.tdb?S=+:"*"']

# NICHT VERWECHSELN: Chambre des baux et loyers: http://ge.ch/justice/donnees/tdb/Decis/CJ/ACJCBL/cabl.tdb

    def parse(self, response):
        alles = response.xpath('//tbody/tr[1]')
        for sel in alles:
            url=sel.xpath('.//td/span/a[contains(@href, "/tdb/pjdoc/pjdoc.tdb?L=")]/@href').extract_first()
            url = response.urljoin(url)
#            print url

# ref wird ueber script erzeugt, also vergessen

#            ref=sel.xpath('normalize-space(.//td[1]/text())').extract_first().encode('utf-8').strip()
#            print ref

            fid=sel.xpath('.//td/span/a[contains(@href, "/tdb/pjdoc/pjdoc.tdb?L=")]/text()').extract_first().encode('utf-8').strip()
            fid=fid.rsplit(' ', 1)[-1]
            fid='GE-Mietsachen-Fall-ID-'+fid+'.txt'
#            print fid

            content=sel.xpath('.//../tr[3]/td[1]/text()').extract_first().encode('utf-8')
#            print content

#            https://stackoverflow.com/questions/5214578/python-print-string-to-text-file
#            with open('log.txt', 'a') as f:
#                f.write('name: {0}, link: {1}\n'.format(item['title'], item['link']))

            if os.path.isfile(self.pfad+fid):
               self.logger.info('CHECK: File existiert.')
               pass
            else:
                with open(os.path.join(self.pfad+fid), 'w') as f:
                    f.write(content)

        next_page = response.xpath('//a[contains(text(), "Suivant")]/@href').extract_first()
        next_page = response.urljoin(next_page)
        print next_page
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

