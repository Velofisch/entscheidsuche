# -*- coding: utf-8 -*-
import scrapy
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time

class ZgNeusSpider(scrapy.Spider):
    name = 'zg_neus'
    zaehl = 0
    allowed_domains = ['zg.ch']
    start_urls = ['https://www.zg.ch/behoerden/staatskanzlei/kanzlei/gvp']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=['--cookies-file=/cookies.txt'])

# --------------------------------- https://github.com/ariya/phantomjs/issues/11637
# ---------------------------------- http://yizeng.me/2014/02/23/how-to-get-window-size-resize-or-maximize-wi...
#        self.driver.maximize_window();
# Achtung, wenn das Fenster zu klein ist, dann klapt der click unten nicht!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.driver.set_window_size(1920, 1400)
        LOGGER.setLevel(logging.WARNING)

    def parse(self, response):

        self.driver.get(response.url)
        alles = self.driver.find_elements_by_xpath('//div/ul/li/a[contains(@href, "gvp/gvp") or contains (@href, "gvp/buch")]')
#        alles = self.driver.find_elements_by_xpath('//a[re:test(text(), "[0-9]\.[0-9]\.[0-9]\.[0-9]")]')
#        alles = self.driver.find_elements_by_xpath('//a[re:test(@href, "1")]')
#        alles = self.driver.find_elements_by_xpath('//div/ul/li/a')
        for sel in alles:
            fllow = sel.get_attribute('href')
            proper_url = response.urljoin(fllow)
            ref = sel.get_attribute('text')
#            print fllow
#            print ref
#            print '---------------------------------'
            yield scrapy.Request(url=fllow, callback=self.weiter)

    def weiter(self, response):
        self.__init__()
        self.driver.get(response.url)
#        ent = self.driver.find_elements_by_xpath('//ul[@class="navTree navTreeLevel3"]/li/div/a')
        time.sleep(1)
        ent = self.driver.find_elements_by_xpath('//ul/li/div/a[contains(@href, "gvp")]')
#        ent = self.driver.find_elements_by_xpath('//a[text()[re:test(., "[0-9]")]')
        for einz in ent:
            item = decision()
            link = einz.get_attribute('href')
            ref = einz.get_attribute('text')
#            ref = ref.encode('utf-8')
            ref = ref.replace(u' ', u'-')
            ref = ref.replace(u'.', u'-')
            ref = ref.replace(u',', u'-')
            ref = ref.replace(u';', u'-')
            ref = ref.replace(u'/', u'-')

            ref = re.sub('[^A-Za-z0-9\-]+', '', ref)
#            ref.replace(unichr(252), 'ue')
#            ref.replace(unichr(246), 'oe')
#            ref.replace(unichr(228), 'ae')
#            ref.replace(unichr(220), 'Ue')
#            ref.replace(unichr(214), 'Oe')
#            ref.replace(unichr(196), 'Ae')
#            ref.replace(unichr(226), 'a')
#            ref.replace(unichr(234), 'e')

            year = str(response.url)
            year = year.rsplit('-', 1)[-1]
#            print year            
            ref = u'ZG-'+year+u'-'+ref+u'.html'

#            print 'Link: '+link

            ref = ref.encode('utf-8')
#            print 'Ref: '+ref
            self.zaehl += 1
#            print 'Anzahl: ---------------------------------------------'+str(self.zaehl)
            item['referenz'] = ref
            item['file_urls'] = [link]
            yield item

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

