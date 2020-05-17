# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider

# ---------------------------------  https://stackoverflow.com/questions/34242455/extracting-links-from-xml-using-scrapy

# class Bge2000Spider(scrapy.Spider):
class Bge2000Spider(XMLFeedSpider):
    name = 'bge2000'
    url_teil_eins = 'http://relevancy.bger.ch/php/aza/http/index.php?highlight_docid=aza%3A%2F%2F'
    url_teil_drei = '&lang=de&type=show_document'
    
    allowed_domains = ['bger.ch']
#    start_urls = ['http://relevancy.bger.ch/sitemaps/sitemapindex.xml']
    start_urls = [
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_1996.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_1997.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_1998.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_1999.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2000.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2001.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2002.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2003.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2004.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2005.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2006.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2007.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2008.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2009.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2010.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2011.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2012.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2013.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2014.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2015.xml',
#                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2016.xml',
                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2017.xml',
                    'http://relevancy.bger.ch/sitemaps/sitemap_aza_2018.xml'
                 ]

# ---------------- https://doc.scrapy.org/en/latest/topics/selectors.html#removing-namespaces

    def parse(self, response):
        response.selector.remove_namespaces()
#        ausgangspunkte = response.xpath('//sitemap/loc[contains(text(), "aza")]')
        bge2000 = response.xpath('//loc[contains(text(), "Jump")]')
        for dec in bge2000:
            item = decision()
# ---------- The r prefix, making the literal a raw string literal
            url = dec.xpath('.//text()').re_first(r'http\S*\/\d\d\d\d')
            urlt = dec.xpath('.//@href').extract_first()
            url1 = response.urljoin(urlt) 
#            item['url'] = url

            ref = dec.xpath('.//text()').re_first('[0-9A-Z]*[-_]\d*\/\d\d\d\d')
            ref = ref.replace('/','-')+'.html'

            refneu = dec.xpath('.//text()').re_first('[0-3][0-9]\.[0-3][0-9]\.[0-9]...\_[0-9A-Z]*[-_]\d*\/\d\d\d\d')
            refclear = refneu.replace('.','-')
            refclear = refclear.replace('/','-')
            refclear = refclear.replace('_','-',1)

            urlclear = self.url_teil_eins+refclear+self.url_teil_drei
            urlclear = urlclear.encode('utf-8') 

            item['referenz'] = ref
            item['file_urls'] = [urlclear]
            yield item

#            print 'URLCLEAR: '+str(urlclear)
#            print 'REF: '+ref
#            print '-------------------------------------------------------'

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

