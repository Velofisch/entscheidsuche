# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from scrapy.selector import Selector
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time
import sys
from selenium.webdriver.common.keys import Keys
from scrapy.utils.response import get_base_url
from datetime import date
from time import strftime
from datetime import datetime


class ZhZivstr2sSpider(scrapy.Spider):
    name = 'zh_zivstr2s'
    allowed_domains = ['gerichte-zh.ch']
    start_urls = ['http://www.gerichte-zh.ch/entscheide/entscheide-suchen.html']
    basis='http://www.gerichte-zh.ch/fileadmin/user_upload/entscheide/oeffentlich/'

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        LOGGER.setLevel(logging.WARNING)
        self.driver.set_window_size(1920, 2640)

    def parse(self, response):
        self.driver.get(response.url)

#         sys.exit()

# ist die Seite suchbar - weil Suchfeld vorhanden 
        try:
            erweiterteSucheKnopf = WebDriverWait(self.driver, 42).until(
                 EC.presence_of_element_located((By.XPATH, '//div/span[@id="extendSearch"]'))
#                 EC.presence_of_element_located((By.XPATH, '//div/p/span/a[contains(@class, "detaillink")]'))
            )
            self.driver.save_screenshot('suchfeld-vorhanden.png')
        except Exception:
            self.logger.info('quitting driver: Suchfeld fuer Texteingabe nicht vorhanden')
            self.driver.save_screenshot('suchfeld-NICHT-vorhanden.png')
            self.driver.quit()


        self.driver.find_element_by_xpath('//div/span[@id="extendSearch"]').click()
        self.driver.save_screenshot('erweiterteSuche.png')

#        self.driver.find_element_by_xpath('//form/div/input[@class="inputSuche"][@type="text"]').click()
#        self.driver.find_element_by_xpath('//form/div/input[@class="inputSuche"][@type="text"]').send_keys("Art")
#        self.driver.find_element_by_xpath('//form/div/input[@class="inputSuche"][@type="text"]').send_keys(Keys.RETURN)

# ist die Seite fuer die erweiterte Suche erschienen 
        try:
            DatumSuchFeldVon = WebDriverWait(self.driver, 420).until(
                 EC.presence_of_element_located((By.XPATH, '//span/input[@name="entscheiddatum_von"]'))
#                 EC.presence_of_element_located((By.XPATH, '//div/p/span/a[contains(@class, "detaillink")]'))
            )
            self.driver.save_screenshot('suchfeld-ERWEITERTE-SUCHE-vorhanden.png')
        except Exception:
            self.driver.save_screenshot('suchfeld-ERWEITERTE-SUCHE-vorhanden.png')
            self.logger.info('quitting driver: DatumSuchFeldVon nicht vorhanden')
            self.driver.quit()

#        startdatum = "01.01."+str(date.today().year-1)
        startdatum = "01.01."+str(date.today().year)

        DatumSuchFeldVon.click()
        DatumSuchFeldVon.send_keys(startdatum)
        DatumSuchFeldVon.send_keys(Keys.RETURN)
        self.driver.save_screenshot('DatumVON-Eingabe.png')

# ------------------------------------------------------------
# ist fuer die Loesung mit allen Entscheiden
        try:
            page = WebDriverWait(self.driver, 420).until(
                 EC.presence_of_element_located((By.XPATH, '//*[@id="entscheideText"]'))
#                 EC.presence_of_element_located((By.XPATH, '//div/p/span/a[contains(@class, "detaillink")]'))
            )
            self.driver.save_screenshot('alleEntscheide.png')
        except Exception:
            self.logger.info('quitting driver: entweder braucht das Laden zu lange oder das Suchmuster ist falsch')
            self.driver.quit()

#        self.driver.save_screenshot('suchfenster.png')
# ------------------------------------------------------------

# fragt sich, ob nicht mit find_elementSSSS die bessere Loesung gefunden wird
        linkliste = self.driver.find_elements_by_xpath('//div/p/span/a[contains(@class, "detaillink")][text()="Details"]')
        refliste = self.driver.find_elements_by_xpath('//*[@id="livesearch"]/div/p[3]/span[3]')

        print "Anzahl Treffer: "+str(len(linkliste))
        print "----------------------------------------------"

        time.sleep(2)
        self.driver.save_screenshot('alleEntscheide_nach-Pause.png')

#        for sel in linkliste:
        for sel in refliste:
#            sel.click()

#            self.driver.save_screenshot('VOR-self-driver-refresh.png')
#            time.sleep(1)
#            self.driver.refresh()
#            time.sleep(1)

#            try:
#                details_ausgeklappt = WebDriverWait(self.driver, 19).until(
#                    EC.presence_of_element_located((By.XPATH, '//span/a[contains(@text(), "ausblenden")]'))
#                )
#                self.driver.save_screenshot('in-schleife-vorhanden.png')
#                self.logger.info('quitting driver: liste nicht vorhanden')
#            except Exception:
#                self.logger.info('quitting driver: das pdf kommt nicht')
#                self.driver.save_screenshot('in-schleife-NICHT-vorhanden.png')
#                self.driver.quit()

#            test = sel.get_attribute('href')
#            testjoin = response.urljoin(test)
#            print 'TEST: '+test
#            print 'TESTJOIN: '+testjoin
#            print ' ------------------------------- '

#            self.driver.save_screenshot('irgendeinclick.png')

#            pdf = self.driver.find_element_by_xpath('//div/p/a[contains(@href, "pdf")]')

            item = decision()
            ref = sel.get_attribute('text')
            ref = sel.get_attribute('href')
            ref = self.basis+sel.text+'.pdf'
#            url = sel.get_attribute('href')
#            url = self.basis+ref 
#            referenz = str(url)
#            referenz = referenz.rsplit('/',1)[-1]

#            item['file_urls'] = [url]
#            item['referenz'] = referenz
            
#            print 'URL: '+url
            print 'REFERENZ: '+str(ref)
            print ' ------------------------------- '

#            time.sleep(6)
#            sel.click()

#            zumachen = self.driver.find_element_by_xpath('//div/p/span/a[contains(@class, "detaillink")][contains(text(), "Details ausblenden")]')
#            zumachen.click()

#            time.sleep(3)

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

