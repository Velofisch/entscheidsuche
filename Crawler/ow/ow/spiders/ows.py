# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time


class OwsSpider(scrapy.Spider):
    name = 'ows'
    allowed_domains = ['ow.ch']
    start_urls = ['http://rechtsprechung.ow.ch/le/']
#    zahl = 0

    def __init__(self):
        scrapy.Spider.__init__(self)
#        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=['--cookies-file=/cookies.txt'])
# --------------------------------- https://github.com/ariya/phantomjs/issues/11637
# ---------------------------------- http://yizeng.me/2014/02/23/how-to-get-window-size-resize-or-maximize-window-using-selenium-webdriver/
#        self.driver.maximize_window();
# Achtung, wenn das Fenster zu klein ist, dann klapt der click unten nicht!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.driver.set_window_size(1920, 2400)
        LOGGER.setLevel(logging.WARNING)

    def parse(self, response):
        self.driver.get(response.url)

        try:
            page = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="v-button-wrap"]'))
            )
        except Exception:
            self.logger.info('quitting driver on first page trying to get content')
            self.driver.quit()

        self.driver.find_element_by_xpath('//div[@id="searchinput-submit"]/div/span[@class="v-button-wrap"]').click()

        try:
            page2 = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located((By.XPATH, '//img[@class="v-icon"]'))
            )
        except Exception:
            self.logger.info('quitting driver')
            self.driver.quit()

        newlinks2 = self.driver.find_elements_by_xpath('//a[contains(@href, "leid")]')
        pdflinks2 = self.driver.find_elements_by_xpath('//div[contains(@class, "custom-result-component-original")]/a[contains(@href, "download")]')

        self.lauf = 0

        for newlink2 in newlinks2:
            item = decision()
            url = newlink2.get_attribute('href')
            proper_url = response.urljoin(url)
            referenz = newlink2.get_attribute('text')
            referenz = referenz.replace(' Nr. ','-')
            referenz = referenz.replace('/','-')
            referenz = referenz.replace(' ','-')+'.htm'

            print 'URL: '+proper_url
            print 'Referenz: '+referenz
            pdf = pdflinks2[self.lauf]
            pdf_url = pdf.get_attribute('href')
            print 'PDF URL: '+pdf_url

            item['referenz'] = referenz
            item['file_urls'] = [pdf_url]
            yield item

            self.lauf = self.lauf + 1
#            self.zahl = self.zahl + 1

        try:
            next_page = self.driver.find_element_by_xpath('//div[contains(@class, "result-pager-next")]/div[contains(@class, "active")]/div/div[contains(@class, "v-label v-widget simplebutton v-label-simplebutton v-label-undef-w")]')
            self.logger.info('naechste seite vorhanden! -------------------------------')
        except Exception:
            self.logger.info('naechste Seite ist NICHT vorhanden ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ')
            self.driver.quit()      

#        while (next_page.text == 'WEITER' or next_page.text=='Avancer'):
        while next_page is not None:

            next_page.click()            
# -------------------------------------------------------------------

            try:
                page2 = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//img[@class="v-icon"]'))
                )
                self.logger.info('naechste seite vorhanden! -------------------------------')
            except Exception:
                self.logger.info('quitting driver')
                self.driver.quit()

            time.sleep(2)

            newlinks = self.driver.find_elements_by_xpath('//a[contains(@href, "leid")]')
            pdflinks = self.driver.find_elements_by_xpath('//div[contains(@class, "custom-result-component-original")]/a[contains(@href, "download")]')
#            entscheiddatumlinks = self.driver.find_elements_by_xpath('//div[contains(@class, "v-label-field-entscheiddatum")]')
#            publikationsdatumlinks = self.driver.find_elements_by_xpath('//div[contains(@class, "v-label-field-publikationsdatum")]')

            index2 = 0

            for newlink in newlinks:

                item = decision()
                url = newlink.get_attribute('href')
                proper_url = response.urljoin(url)
                referenz = newlink.get_attribute('text')
                referenz = referenz.replace(' Nr. ','-')
                referenz = referenz.replace('/','-')
                referenz = referenz.replace(' ','-')+'.htm'
#                print 'URL: '+proper_url
#                print 'Betreff: '+betreff

                pdf = pdflinks[index2]
                pdf_url = pdf.get_attribute('href')
#                print 'PDF URL: '+pdf_url

                item['referenz'] = referenz
                item['file_urls'] = [pdf_url]
                yield item 

                index2 = index2 + 1
#                self.zahl = self.zahl + 1

            next_page = None

            try:
                next_page = self.driver.find_element_by_xpath('//div[contains(@class, "result-pager-next")]/div[contains(@class, "next-active")]/div/div[contains(@class, "v-label v-widget simplebutton v-label-simplebutton v-label-undef-w")]') 
                self.driver.save_screenshot("weiter.png")

            except Exception:
#            except NoSuchElementException:
                self.logger.info('abbruch bei der abfrage von weiter -----------------------')
                self.driver.save_screenshot("abbruch.png")
                next_page is None
                self.driver.quit()

        self.driver.quit()


class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

