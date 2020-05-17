# -*- coding: utf-8 -*-
import scrapy

class ZgAltsSpider(scrapy.Spider):
    name = 'zg_alts'
    allowed_domains = ['zg.ch']
    start_urls = ['https://www.zg.ch/behoerden/staatskanzlei/kanzlei/gvp']

# https://www.zg.ch/behoerden/staatskanzlei/kanzlei/gvp/downloads/gvp-entscheide-2007/@@download/file/gvp-2007.pdf	# https://www.zg.ch/behoerden/staatskanzlei/kanzlei/gvp/downloads/gvp_2004/@@download/file/gvp_2004_komplett.pdf

    def parse(self, response):
        alles = response.xpath('//td[@class="column-sortable_title"]/span[@class="linkWrapper"]/a[contains(text(), "199") or contains(text(), "200") or contains(text(), "2010") or contains(text(), "2011")][not(contains(@img, "pdf"))]')
        for sel in alles:
            item = decision()
            url = sel.xpath('.//@href[normalize-space()]').extract_first()
            url = response.urljoin(url)
            ref = sel.xpath('.//text()').extract_first()
            ref = ref.replace(' ', '-')+'.pdf'
            item['file_urls'] = [url]
            item['referenz'] = ref
            yield item

#            print url
#            print ref
#            print '----------------------------------------------'

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()
