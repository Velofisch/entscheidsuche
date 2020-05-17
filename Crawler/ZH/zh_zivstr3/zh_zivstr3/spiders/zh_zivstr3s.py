# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time
from selenium.webdriver.common.keys import Keys
from scrapy.utils.response import get_base_url
import sys

class ZhZivstr3sSpider(scrapy.Spider):
    name = 'zh_zivstr3s'
    allowed_domains = ['www.gerichte-zh.ch']
    start_urls = ['http://www.gerichte-zh.ch/entscheide/entscheide-suchen.html']
    base_url = 'http://www.gerichte-zh.ch/entscheide/entscheide-drucken.html?tx_frpentscheidsammlung_pi3[entscheidDrucken]='

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        LOGGER.setLevel(logging.WARNING)
        self.driver.set_window_size(1920, 1080)

    def start_requests(self):
#        self.__init__()
        for i in xrange(1,23000):
            ziel = self.base_url+str(i)
#            print ziel
            yield scrapy.Request(ziel, self.parse)

    def parse(self, response):
#        self.__init__()
#          https://stackoverflow.com/questions/45831217/function-driver-switchto-frame-not-working-in-selenium 
#        time.sleep(14)
#        self.driver.switch_to_frame("Drucken")
#        self.driver.find_element_by_xpath('//form/div/input[@class="inputSuche"][@type="text"]').send_keys("Art")
#        self.driver.find_element_by_xpath('//.').send_keys(Keys.ESCAPE)
#        self.driver.send_keys(Keys.ESCAPE)

# https://stackoverflow.com/questions/41649916/python-selenium-how-to-send-esc-key-to-close-pop-up-window
#        self.driver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

        link = self.driver.find_element_by_xpath('//div[@class="pdf"]/p/a')
 
# ---------------------
#        try:
#            page = WebDriverWait(self.driver, 420).until(
#                 EC.presence_of_element_located((By.XPATH, '//*[@id="entscheideText"]'))
#                 EC.presence_of_element_located((By.XPATH, '//div/p/span/a[contains(@class, "detaillink")]'))
#            )
#        except Exception:
#            self.logger.info('quitting driver: entweder braucht das Laden zu lange oder das Suchmuster ist falsch')
#            self.driver.quit()

        item = decision()
        url = link.get_attribute('href')
        referenz = str(url)
        referenz = referenz.rsplit('/',1)[-1]

        item['file_urls'] = [url]
        item['referenz'] = referenz

        print 'URL: '+url
        print 'REFERENZ: '+referenz
        print ' ------------------------------- '

        time.sleep(6)
#            sel.click()

# ------------

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

