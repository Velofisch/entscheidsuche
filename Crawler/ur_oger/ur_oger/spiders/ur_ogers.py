# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
from scrapy.linkextractors import LinkExtractor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector

from selenium.webdriver.remote.remote_connection import LOGGER
import logging


class UrOgersSpider(scrapy.Spider):
    name = 'ur_ogers'
    allowed_domains = ['ur.ch']
#    start_urls = ['http://www.ur.ch/de/behoerdenmain/gerichtetop/gericht/gerichte/welcome.php?departement_id=62&page=5']
    start_urls = ['https://www.ur.ch/rechtsprechung']
    schleife = 0
    nezae = 1

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=['--cookies-file=/cookies.txt'])
        LOGGER.setLevel(logging.WARNING)

    def parse(self, response):
        self.driver.get(response.url)

# https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html
        try:
            page = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located((By.XPATH, '//tr/td/a[contains(@href, "publikation")]'))
            )
            self.logger.info('ERFOLG: Entscheid auf erster Seite vorhanden')
        except Exception:
            self.logger.info('MISSERFOLG: quitting driver beim Pruefen des Vorhandenseins der ersten Seite')
            self.driver.quit()

        xpath='//a[contains(@href, "/publikation/")]'
        links = self.driver.find_elements_by_xpath(xpath)

        for link in links:
            item = decision()
            url = link.get_attribute('href')
            proper_url = response.urljoin(url)
#            betreff = proper_url.rsplit('/', 1)[-1] 
            ref = link.get_attribute('text')
            ref = 'UR-'+ref.split(' ',2)[0]+'-'+ref.split(' ',2)[1]
            ref = ref.replace('/','-')+'.pdf'

#            item['referenz'] = betreff
            item['referenz'] = ref
            item['file_urls'] = [proper_url]
            print proper_url
            print ref
            print '----------------------------------------------'
            self.schleife = self.schleife+1
            yield item 

        try:
#            next_page = self.driver.find_element_by_xpath('//span[@class="next fg-button ui-button ui-state-default"]')
            next_page = self.driver.find_element_by_xpath('//li[@class="paginate_button page-item next"]/a')
            self.logger.info('ERFOLG: auf der Suche nach der ersten naechsten seite ???')
        except Exception:
            self.logger.info('quitting driver')
            print 'naechste Seite ist NICHT vorhanden ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,'
            self.driver.quit()

        while next_page is not None:

            next_page.click()
            links2 = self.driver.find_elements_by_xpath(xpath)
            for link2 in links2:
                item = decision()
                url2 = link2.get_attribute('href')
                proper_url2 = response.urljoin(url2)
                betreff = proper_url2.rsplit('/', 1)[-1] 

                ref = link2.get_attribute('text')
                ref = 'UR-'+ref.split(' ',2)[0]+'-'+ref.split(' ',2)[1]
                ref = ref.replace('/','-')+'.pdf'

                item['referenz'] = ref
                item['file_urls'] = [proper_url2]
                print proper_url2
                print ref
                self.schleife = self.schleife+1
                print ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                '+str(self.schleife)
                yield item 

            next_page = None
            try:
#                next_page = self.driver.find_element_by_xpath('//span[@class="next fg-button ui-button ui-state-default"]')
                next_page = self.driver.find_element_by_xpath('//li[@class="paginate_button page-item next"]/a')
                time.sleep(2)
                self.nezae = self.nezae+1
                print "naechste Seite ist: ----------------------------------------------"+str(self.nezae)
            except Exception:
                self.logger.info('quitting driver')
                self.driver.quit()

        self.driver.quit()

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()


