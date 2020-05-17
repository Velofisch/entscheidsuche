# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import time

class Ar1sSpider(scrapy.Spider):
    name = 'ar1s'
    allowed_domains = ['ar.ch']
    start_urls = ['https://www.ar.ch/gerichte/obergericht/gerichtsentscheide-zivil-und-strafrecht/']


    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=['--cookies-file=/cookies.txt'])
#       DAS IST WICHTIG, WEIL SONST AUF DEN LANGEN SEITEN DER LINK NICHT SICHTBAR WIRD, IST ABER NOCH DAS SETZEN DES FOKUS NOETIG
        self.driver.set_window_size(2000, 3000)

    def parse(self, response):
        self.driver.get(response.url)

        try:
            page = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div/ul/li'))
            )
        except Exception:
            self.logger.info('quitting driver')
            self.driver.quit()

        links2 = self.driver.find_elements_by_xpath('//tr/td/a[contains(@href, "jumpurl")]')

        for link2 in links2:
            item = decision()
            url2 = link2.get_attribute('href')
            proper_url2 = response.urljoin(url2)
            proper_url2 = url2

            cl = str(proper_url2)
            cl = cl.replace('%2F', '/')

            item['file_urls']=[proper_url2]
            ref = re.search(r'[0-9A-Z]{1,3}_[0-9].*_[0-9].*.pdf', cl)
# ------------------- https://stackoverflow.com/questions/38579725/return-string-with-first-match-regex
            ref_text = ref.group()
            item['referenz']= ref_text

#            print 'URL:                      '+proper_url2
#            print 'REFERENZ                  '+ref_text
#            print '==========================================='
            yield item


        try:
            next_page = self.driver.find_element_by_xpath('//li/a[@class="notTextLink"][@ng-click="nextPage()"]')
            self.logger.info('erste naechste seite vorhanden???')
            print 'Laenge: '+next_page.text
        except Exception:
            self.logger.info('quitting driver beim Versuch das Element fuer den ersten Klick zu finden - vor der Schleife')
            print 'naechste ERSTE Seite ist NICHT vorhanden ,,,,,,,,,,,,,,,,,,'
            self.driver.quit()

# --------------------------------------------
        while next_page is not None:

            self.driver.execute_script("window.scrollTo(0, 3280)")

            try:
#                np_link = next_page.get_attribute('href')
#                np = response.urljoin(np_link)
                next_page.click()
#                next_page.send_keys(Keys.RETURN)
                self.driver.save_screenshot("weiter.png")
            except Exception:
                self.logger.info('quitting driver an der Stelle des ersten Klickes in der Schleife')
                self.driver.quit()

            links3 = self.driver.find_elements_by_xpath('//tr/td/a[contains(@href, "jumpurl")]')

            for link3 in links3:
                link3.location_once_scrolled_into_view
                item = decision()
                url3 = link3.get_attribute('href')
                proper_url3 = response.urljoin(url3)
                proper_url3 = url3

                cl3 = str(proper_url3)
                cl3 = cl3.replace('%2F', '/')

                item['file_urls']=[proper_url3]
                ref = re.search(r'[0-9A-Z]{1,3}_[0-9].*_[0-9].*.pdf', cl3)
# --------------- https://stackoverflow.com/questions/38579725/return-string-with-first-match-regex
                ref_text3 = ref.group()
                item['referenz']= ref_text3

#                print 'URL:                      '+proper_url3
#                print 'REFERENZ                  '+ref_text3
#                print '--------------------------------------  '
                yield item



            next_page = None

#            time.sleep(4)

#            self.driver.execute_script('window.scrollTo(0, 1920)')
            self.driver.save_screenshot("vornachsteselement.png")

#            print body.scrollHeight

            try:
                self.driver.execute_script('window.scrollTo(0, 2520)')
#                time.sleep(3)
#                next_page = self.driver.find_element_by_xpath('//li/a[@class="notTextLink"][@ng-click="nextPage()"]')
                next_page = self.driver.find_element_by_xpath('//li[not(@class="disabled")]/a[@class="notTextLink"][@ng-click="nextPage()"]')
                self.logger.info('In Schleife: Versuch, den Link zu finden ')

            except Exception:
                self.driver.save_screenshot("fail.png")
                self.logger.info('in Schleife: quitting driver: naechste Seite ist NICHT vorhanden ,,,,,,,,,,,,,,,,,,')
                self.driver.quit()

# -------------------------- https://stackoverflow.com/questions/44995042/phantomjs-raise-oserror-errno-9-bad-file-descriptor
        self.driver.quit()

class decision(scrapy.Item):
    url = scrapy.Field()
    referenz = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


