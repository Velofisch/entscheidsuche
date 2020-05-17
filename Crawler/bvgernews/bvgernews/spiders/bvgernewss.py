# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options
import sys
import random
from datetime import date
from time import strftime
from datetime import datetime

class BvgernewssSpider(scrapy.Spider):
    name = 'bvgernewss'
    warteauf = ''
    zaehler = 0
    zae_text = '_id63idx'
    index = zae_text+str(zaehler)
    allowed_domains = ['jurispub.admin.ch']
    start_urls = ['https://jurispub.admin.ch/publiws/pub/news.jsf']
    tempref1=''
    random.seed()

    def __init__(self):
        scrapy.Spider.__init__(self)
        options = Options()
#        options.binary_location = '/usr/local/bin/chromedriver'
#        options.add_argument('start-maximized')
#        options.add_argument('--disable-gpu')
#        options.add_argument('--disable-dev-shm-usage')
#        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)

#_______________________
#        options.add_argument('--headless')
#        options.add_argument('--window-size=1280x4580')
#        options.add_argument('--no-sandbox')
#        options.add_argument('--disable-extensions')
#        options.add_argument('disable-infobars')
#        self.driver = webdriver.Chrome(driver_path='/usr/local/bin/chromedriver',chrome_options=options)
#_______________________

        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')


        LOGGER.setLevel(logging.WARNING)


    def parse(self, response):
        self.driver.get(response.url)

# --------------------- NEW
# Versuch, mit Datumbereich alles zu suchen!!!!!!!!!!!!
#  https://www.seehuhn.de/pages/pdate.html
#https://stackoverflow.com/questions/22739015/convert-date-from-mm-dd-yyyy-to-another-format-in-python#22739059

#        startdatum = "01.01."+str(date.today().year)

        endtag = str(date.today().day)
        endmonat = str(date.today().month)
        endjahr = str(date.today().year)
        enddatum = endtag+'.'+endmonat+'.'+endjahr
        startdatum = "01."+endmonat+"."+endjahr

        print 'Startdatum: '+startdatum
        print 'Enddatum: '+enddatum
        print '==================================================================='

        try:
            startdatumsfeld = self.driver.find_element_by_xpath('//tr[@class="icePnlGrdRow1"]/td/div/input[@id="form:fromDate"]')
            self.logger.info('STARTDATUMSFELD gefunden.')
        except Exception:
            self.logger.info('STARTDATUMSFELD NICHT gefunden.')
            self.driver.quit()

        try:
            enddatumsfeld = self.driver.find_element_by_xpath('//tr[@class="icePnlGrdRow2"]/td/div/input[@id="form:toDate"]')
            self.logger.info('ENDDATUMSFELD gefunden.')
        except Exception:
            self.logger.info('ENDDATUMSFELD NICHT gefunden.')
            self.driver.quit()
 
        startdatumsfeld.send_keys(startdatum)
        enddatumsfeld.send_keys(enddatum)
        self.driver.save_screenshot("Datumseingabe.png")
#       time.sleep(2)
#       sys.exit()


# suche Suchknopf
        try:
            anzeigeknopf = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//input[contains(@id, "_id37")]'))
#                EC.presence_of_element_located((By.XPATH, '//input[@id="form:_id37"]'))
#                EC.presence_of_element_located((By.XPATH, '//div[contains(@id, "_id37")]'))
            )
            self.driver.save_screenshot("ERFOLG-entscheide-da.png")
            self.logger.info('ERFOLG: driver findet Anzeigeknopf')
        except Exception:
            self.logger.info('MISSERFOLG: driver steigt aus bei der Pruefung nach Anzeigeknopf')
            self.driver.save_screenshot("ERFOLG-suchseite-WAHL.png")
            self.driver.quit()

# druecke Suchknopf
        try:
#            self.driver.find_element_by_xpath('//input[@id="form:_id37"]').click()
            self.driver.find_element_by_xpath('//input[contains(@id, "_id37")]').click()
            self.logger.info('Knopf mit anzeigen gedrueckt.')
#            self.driver.save_screenshot("ERFOLG-Knopf-gedrueckt.png")
        except Exception:
            self.logger.info('GESCHEITERT: Knopf mit anzeige gedrueckt.')
#            self.driver.save_screenshot("knappnachclick-auf-Suchknopf.png")
            self.driver.quit()

# --------------------- NEW

# ist ein eindeutiges Element, dass Entscheide auf der Seite  kennzeichnet, vorhanden, SONST QUIT
        try:
            sindentscheideda = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//tr/td/a[contains(@id, "_id56")]'))
#                EC.presence_of_element_located((By.XPATH, '//div[contains(@id, "_id37")]'))
            )
            self.driver.save_screenshot("ERFOLG-entscheide-da.png")
            self.logger.info('ERFOLG: driver findet Entscheide')
        except Exception:
            self.logger.info('MISSERFOLG: driver steigt aus bei der Pruefung nach Entscheiden')
            self.driver.save_screenshot("ERFOLG-suchseite-WAHL.png")
            self.driver.quit()

# das Element "iceOutFrmt" wird verwendet bei der Anzeige der Anzahl Resultate
        try:
            page3 = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "iceOutFrmt")][1]'))
            )
            self.logger.info('ERFOLG: Die Zahlenwerte erscheinen ')
            self.driver.save_screenshot("ERFOLG-Zahlenwerte-erscheinen.png")
        except Exception:
            self.logger.info('MISSERFOLG: Die Zahlenwerte erscheinen NICHT')
            self.driver.quit()

#        ergebnis = self.driver.find_element_by_xpath('//span[contains(@class, "iceOutFrmt")]').get_attribute('text')
#        ergebnis = self.driver.find_element_by_xpath('//div[4]/div/span[contains(@class, "iceOutFrmt")]').text
#        ergebnis = self.driver.find_elements_by_xpath('//span[contains(@class, "iceOutFrmt")][1]')
# /html/body/div[1]/form/div[1]/div[4]/div/span
#        ergebnis = str(ergebnis)
#        ergebnis = ergebnis.split(' ', 1)[0]
#        print 'Ergebnis: .............................. '+ergebnis

# hier suchen wir Teile von Trefferelementen

#        if sindentscheideda is not None:
#            yield scrapy.Request(url=response.url, callback=self.weiter, dont_filter=True) 


        eref = self.driver.find_elements_by_xpath('//a[contains(@id, "_id56")]')
        entscheidpdf0 = self.driver.find_elements_by_xpath('//a[contains(@id, "_id57")]')

        countRef = len(eref)
        countPDF = len(entscheidpdf0)

        for x in range(countRef):
            tempref1 = eref[x].get_attribute('text')
#            print 'Schleifenindex x ist: '+str(x)
            item = decision()
            referenz = tempref1.replace("/", "-")+'.pdf'
            referenz = referenz.replace(" ", "-")
            print 'Referenz ist: '+str(referenz)
            item['referenz'] = referenz 

            link  = entscheidpdf0[x].get_attribute('href')
            url = response.urljoin(link)
            print 'url x ist: '+str(url)
            print '==========================================================='
#            item['url']=response.urljoin(link)
#            item['file_urls']=[item['url']]
            item['file_urls']= [url]
            self.zaehler = self.zaehler+1
            yield item

# --------------------- CHECK auf naechste Seite ----------------------------------------------

        try:
            page = WebDriverWait(self.driver, 10).until(
#               EC.presence_of_element_located((By.XPATH, '//span[contains(@id, "_id83next") and contains(@class, "iceCmdLnk")]'))
               EC.presence_of_element_located((By.XPATH, '//span[@id="form:_id83next"][@class="iceCmdLnk-dis")]'))
            )
            self.logger.info('ERFOLG: naechste Seite ist nicht vorhanden.')
            next_page = None
        except Exception:
            next_page = self.driver.find_element_by_xpath('//a[@id="form:j_id83next"][@class="iceCmdLnk"]')
#            next_page = self.driver.find_element_by_xpath('//a[@id="form:_id83next"][@class="iceCmdLnk"]')
            self.logger.info('ANDERER ERFOLG: naechste Seite wohl vorhanden')
#            self.driver.quit()

#        no_next_page = self.driver.find_element_by_xpath('//span[contains(@id, "_id83next") and contains(@class, "iceCmdLnk")]')

        while next_page is not None:

            try:
                next_page.click()
                self.logger.info('ERFOLG: klick auf naechste Seite ')
                self.driver.save_screenshot("ERFOLG-next-page-click.png")
            except Exception:
                self.logger.info(self.warteauf+'keine klickbare naechste Seite')
                self.driver.save_screenshot("MISSERFOLG-next-page-click.png")
                self.driver.quit()

            time.sleep(3)

#            yield scrapy.Request(url=response.url, callback=self.weiter, dont_filter=True)

            eref2 = self.driver.find_elements_by_xpath('//a[contains(@id, "_id56")]')
            entscheidpdf02 = self.driver.find_elements_by_xpath('//a[contains(@id, "_id57")]')

            countRef2 = len(eref2)
            countPDF2 = len(entscheidpdf02)

            for y in range(countRef2):
                tempref12 = eref2[y].get_attribute('text')
#                print 'Schleifenindex x ist: '+str(x)
                item = decision()
                referenz2 = tempref12.replace("/", "-")+'.pdf'
                referenz2 = referenz2.replace(" ", "-")
                print 'Referenz ist: '+str(referenz2)
                item['referenz'] = referenz2

                link2 = entscheidpdf02[y].get_attribute('href')
                url2 = response.urljoin(link2)
                print 'url x ist: '+str(url2)
                print '==========================================================='
#                item['url']=response.urljoin(link2)
                item['file_urls']=[url2]
                self.zaehler = self.zaehler+1
                yield item

            next_page = None

            try:
                page = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@id="form:j_id83next"][@class="iceCmdLnk"]'))
                )
                self.logger.info('ERFOLG: naechste Seite ist vorhanden.')
                next_page = self.driver.find_element_by_xpath('//a[@id="form:j_id83next"][@class="iceCmdLnk"]')
            except Exception:
                self.logger.info('MISSERFOLG: keine naechste Seite _id63next')
                self.driver.quit()

        self.driver.quit()
#        sys.exit()

class decision(scrapy.Item):
    file_urls = scrapy.Field()
    url = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

 
