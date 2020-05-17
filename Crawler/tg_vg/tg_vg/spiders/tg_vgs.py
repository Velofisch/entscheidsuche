# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time

class TgVgsSpider(scrapy.Spider):
    name = 'tg_vgs'
    allowed_domains = ['vgbuch.tg.ch']
    start_urls = ['http://vgbuch.tg.ch']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=['--cookies-file=/cookies.txt'])
        LOGGER.setLevel(logging.WARNING)

# -------------------- https://stackoverflow.com/questions/15464808/how-to-navigate-a-subframe-inside-a-frameset-using-selenium-webdriver

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(1)

        try:
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('/html/frameset/frameset/frameset/frame[3]'))
        except Exception:
            self.logger.info('quitting driver bei switch to Klappframe')
            self.driver.quit()

        time.sleep(1)
        try:
            self.driver.find_element_by_xpath('//font[@class="menu"]/a[@href="javascript:parent.allesaufzu(1)"]').click()
            time.sleep(1)
#            page = WebDriverWait(self.driver, 15).until(
#                EC.presence_of_element_located((By.NAME, 'tx_iscourtcases_entscheidesuche[querysearch]'))
#            )
        except Exception:
            self.logger.info('quitting driver bei Knopf alles aufmachen')
            self.driver.quit()

        self.driver.switch_to.default_content()

        try:
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('/html/frameset/frameset/frameset/frame[2]'))
        except Exception:
            self.logger.info('quitting driver bei switch to MENUFRAME')
            self.driver.quit()

        time.sleep(1)

        links = self.driver.find_elements_by_xpath('//body/font/nobr/a')
#        links = self.driver.find_elements_by_xpath('//body/font/nobr/a[contains(@href, "aufzu")]')
        praefix = ''
        referenz = ''

        for link in links:     
            item = decision()
            url = link.get_attribute('href')
            ref = link.get_attribute('text')
            ref = ref.strip()
            ref = ref.replace(' ', '-')

            if 'TVR' in ref:
                praefix = ref
                ref = ''
#                print 'Praefix ist: '+praefix
#                print 'ref ist: '+ref
            else:
                pass

#            if praefix nicht gleich leer und ref nicht gleich leer, dann setze sie zur referenz zusammen

            if ref != '':
                ref = ref.replace('.', '')
                referenz = praefix+'-'+ref+'.html'
                referenz = str(referenz)
                item['referenz'] = referenz
                item['file_urls'] = [url]
                yield item

#            print 'ref ist: '+ref
#            print 'Praefix ist: '+praefix
#            print 'Referenz: '+referenz
#            print 'Link: '+url


class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

