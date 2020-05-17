# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time
import unidecode
import urllib 


class BgertaeglichsSpider(scrapy.Spider):
    name = 'bgertaeglichs'
    allowed_domains = ['bger.ch']
    start_urls = ['https://www.bger.ch/ext/eurospider/live/de/php/aza/http/index_aza.php?lang=de&mode=index&search=false']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        LOGGER.setLevel(logging.WARNING)

    def parse(self, response):
#        print response.body
#        print response.url

        self.driver.get(response.url)

        try:
            page = WebDriverWait(self.driver, 29).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="eit"]'))
            )
        except Exception:
            self.logger.info('quitting driver beim warten auf den Seitenaufbau')
            self.driver.quit()

#        tage = self.driver.find_elements_by_xpath('//div[@class="eit"]/p/a[contains(@href, "index_az")]')
#        for einzeltag in tage:
#            urltag = einzeltag.get_attribute('href')
#            yield scrapy.Request(url=urltag, callback=self.weiter)

        tag = self.driver.find_element_by_xpath('//div[@class="eit"]/p/a[contains(@href, "index_az")]')
        urltag = tag.get_attribute('href')
        yield scrapy.Request(url=urltag, callback=self.weiter)


    def weiter(self, response):
       self.__init__()
       self.driver.get(response.url)

       try:
           page = WebDriverWait(self.driver, 29).until(
#               EC.presence_of_element_located((By.XPATH, '//div[@class="eit"]'))
               EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "docid")]'))
           )
       except Exception:
           self.logger.info('quitting driver beim warten auf den Seitenaufbau bei den Einzelentscheiden')
           self.driver.quit()

#       aktent = self.driver.find_elements_by_xpath('//div[@class="eit"]/p/a[contains(@href, "inde_za")]')
#       aktent = self.driver.find_elements_by_xpath('//tr/td/a[contains(@href, "docid")]')
       aktent = self.driver.find_elements_by_xpath('//a[contains(@href, "docid")]')
       for sel in aktent:
#           time.sleep(2)
           urlent = sel.get_attribute('href')
           urlent = response.urljoin(urlent)
#           urlent = urllib.unquote(urlent).decode('utf8')
#           urlref = urlref.replace('https:\/\/www.bger.ch\/ext\/eurospider\/live\/de\/','http:\/\/relevancy.bger.ch\/')+'.html'
           urlent = urlent.replace('https','http')
           urlent = urlent.replace('www','relevancy')
           urlent = urlent.replace('ext/eurospider/live/de/','')
           urlent = urlent.replace('aza://','')
           urlent = urlent.replace('&zoom=','')

           urlref = sel.get_attribute('text')
#           urlref = unidecode.unidecode(urlref)
           urlref = urlref.replace('/','-')+'.html'
           print urlent
           print urlref
           print '---------------------------------'

           item = decision()
           item['referenz'] = urlref
           item['file_urls'] = [urlent]

           yield item


class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

