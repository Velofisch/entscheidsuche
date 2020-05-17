# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import logging
# import pprint
import time
# import timeit
# import os.path
from selenium.webdriver.chrome.options import Options
import sys
import random


class BvgspiSpider(scrapy.Spider):
    name = 'bvger_iiis'
    warteauf = ''
    zaehler = 0
    zae_text = '_id63idx'
    index = zae_text+str(zaehler)
    allowed_domains = ['admin.ch']
    start_urls = ['https://jurispub.admin.ch/publiws/pub/search.jsf']
    tempref1=''
    random.seed()

    def __init__(self):
        scrapy.Spider.__init__(self)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1280x4580')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(chrome_options=options)
        LOGGER.setLevel(logging.WARNING)


    def parse(self, response):
        self.driver.get(response.url)

# ist ein eindeutiges Element, das die Suchseite kennzeichnet, vorhanden
        try:
            page = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//input[contains(@id, "searchSubmitButton")]'))
#                EC.presence_of_element_located((By.XPATH, '//div[contains(@id, "_id37")]'))
            )
            self.driver.save_screenshot("ERFOLG-suchseite-da.png")
            self.logger.info('ERFOLG: driver findet Suchknopf searchSubmitButton')
        except Exception:
            self.logger.info('MISSERFOLG: driver steigt aus bei der Pruefung nach dem Vorhandensein der Suche')
            self.driver.save_screenshot("ERFOLG-suchseite-WAHL.png")
            self.driver.quit()


        try:
             wait = WebDriverWait(self.driver, 10)
             knopf = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@id, "n-2:_id76")]')))
             self.driver.find_element_by_xpath('//*[contains(@id, "n-2:_id76")]').click()

             self.logger.info('ERFOLG: Abteilung ausgewaehlt ')
             self.driver.save_screenshot("ERFOLG-ABTEILUNG-WAHL.png")
        except Exception:
             self.logger.info('MISSERFOLG: Abteilung ausgewaehlt ')
             self.driver.save_screenshot("MISSERFOLG-ABTEILUNG-WAHL.png")
             self.driver.quit()

# Klick auf Suchknopf
        try:
            self.driver.find_element_by_xpath('//input[contains(@id, "searchSubmitButton")]').click()
            self.logger.info('ERFOLG: searchSubmitButton gedrueckt')
        except Exception:
            self.logger.info('MISSERFOLG: driver steigt aus beim click-versuch auf searchSubmitButton aus')
            self.driver.quit()

        try:
            page2 = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//table[contains(@id, "resultTable")]'))
            )
            self.logger.info('ERFOLG: Resultate erscheinen nach dem Klick auf den Suchknopf ')
        except Exception:
            self.logger.info('driver steigt aus beim check, ob die neue seite nach dem suchclick erscheint')
            self.driver.quit()

# das Element "iceOutFrmt" wird verwendet bei der Anzeige der Anzahl Resultate
        try:
            page3 = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "iceOutFrmt")]'))
            )
            self.logger.info('ERFOLG: Die Zahlenwerte erscheinen ')
            self.driver.save_screenshot("ERFOLG-Zahlenwerte-erscheinen.png")
        except Exception:
            self.logger.info('MISSERFOLG: Die Zahlenwerte erscheinen NICHT')
            self.driver.quit()

        ergebnis = self.driver.find_element_by_xpath('//span[contains(@class, "iceOutFrmt")]').text
        ergebnis = ergebnis.split(' ', 1)[0]
        print 'Ergebnis: .............................. '+ergebnis

# hier suchen wir Teile von Trefferelementen

        eref = self.driver.find_elements_by_xpath('//a[contains(@id, "_id36")]')
        entscheidpdf0 = self.driver.find_elements_by_xpath('//a[contains(@id, "_id37")]')

        countRef = len(eref)
        countPDF = len(entscheidpdf0)
        
        for x in range(countRef):
            tempref1 = eref[x].get_attribute('text')
#            print 'Schleifenindex x ist: '+str(x)
            item = decision()
            referenz = tempref1.replace("/", "-")
#            print 'Referenz ist: '+str(referenz)
            item['referenz'] = tempref1.replace("/", "-")
            link  = entscheidpdf0[x].get_attribute('href')
            url = response.urljoin(link)
#            print 'url x ist: '+str(url)
            item['url']=response.urljoin(link)
            item['file_urls']=[item['url']]
            self.zaehler = self.zaehler+1
            yield item

#        sys.exit()
        print '------------------------------------- VOR GROSSER SCHLEIFE ------------------------------------- '

# so jetzt die Schleife mit den naechsten Seiten 
    
#        next_page = self.driver.find_elements_by_xpath('//a[containts(@id, "_id63next"]/img[contains(@id, "_id67")]')
        next_page = self.driver.find_element_by_xpath('//a[contains(@id, "_id63next")]')

        while next_page is not None:
            ergebnisvorne = self.driver.find_element_by_xpath('//span[contains(@class, "iceOutFrmt")]').text
            seitevorn = ergebnisvorne.split(' ', 10)[8]
            startzeit = time.time()

            try:
#                self.warteauf = zae_text+str(self.zaehler)
#                print '-----------------------------------------------------             '+self.warteauf
                next_page.click()
#                page = WebDriverWait(self.driver, 9).until(
#                    EC.presence_of_element_located((By.XPATH, '//a[contains(@id, "_id36")]'))
#                    EC.presence_of_element_located((By.XPATH, '//a[contains(@id, self.warteauf) or (self.zaehler>5400)]'))
#                    EC.presence_of_element_located((By.XPATH, '//a[contains(@id, self.warteauf) or (self.zaehler>5400)]'))
#                )
                self.logger.info('ERFOLG: klick auf naechste Seite ')
                self.driver.save_screenshot("ERFOLG-next-page-click.png")
            except Exception:
                self.logger.info(self.warteauf+'keine klickbare naechste Seite')
                self.driver.save_screenshot("MISSERFOLG-next-page-click.png")
                self.driver.quit()

# hier muss die Abfrage rein, ob die naechste Seite schon da ist, sonst gibt es einen Geschwindigkeitsfehler 
            zufall = random.randint(1,9) 
            time.sleep(zufall)

            ergebnis = self.driver.find_element_by_xpath('//span[contains(@class, "iceOutFrmt")]')
            while ergebnis is NoSuchElementException:
                ergebnis = self.driver.find_element_by_xpath('//span[contains(@class, "iceOutFrmt")]')

# ist auch nutzlos, wenn nicht klar ist, ob es ein altes oder ein neues Element ist
            try:
                page = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "iceOutFrmt")]'))
                )
                self.logger.info('ERFOLG: Seiteninfos sind vorhanden.')
                self.driver.save_screenshot("ERFOLG-Seitenaufbau-nach-next-page-click.png")
            except Exception:
                self.logger.info('MISSERFOLG: Seiteninfos sind NICHT vorhanden.')
                self.driver.save_screenshot("MISSERFOLG-Seitenaufbau-Elemente-id-36.png")
                self.driver.quit()

            try:
                page = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(@id, "_id36")]'))
                )
                self.logger.info('ERFOLG: Resultatelemente id36 sind vorhanden.')
                self.driver.save_screenshot("ERFOLG-Seitenaufbau-nach-next-page-click.png")
            except Exception:
                self.logger.info('MISSERFOLG: keine Elemente id 36')
                self.driver.save_screenshot("MISSERFOLG-Seitenaufbau-Elemente-id-36.png")
                self.driver.quit()

           
            try:
                page = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(@id, "_id37")]'))
                )
                self.logger.info('ERFOLG: Resultatelemente id37 sind vorhanden.')
#                self.driver.save_screenshot("ERFOLG-Seitenaufbau-nach-next-page-click.png")
            except Exception:
                self.logger.info('MISSERFOLG: keine Elemente id 37')
                self.driver.save_screenshot("MISSERFOLG-Seitenaufbau-Elemente-id-37.png")
                self.driver.quit()

            try:
                page = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "iceOutFrmt")]'))
                )
                ergebnishinten = self.driver.find_element_by_xpath('//span[contains(@class, "iceOutFrmt")]').text
                self.logger.info('ERFOLG: evaluieren Wert ergebnishinten')
            except Exception:
                self.logger.info('MISSERFOLG: evaluieren Wert ergebnishinten')
                self.driver.quit()


            entscheidreferenzen2 = self.driver.find_elements_by_xpath('//a[contains(@id, "_id36")]')
            countRef2 = len(entscheidreferenzen2)
            entscheidpdf2 = self.driver.find_elements_by_xpath('//a[contains(@id, "_id37")]')
            countPDF2 = len(entscheidpdf2)

            for x in range(0,countRef2):
                self.zaehler = self.zaehler+1
#                print '------------------------------------ '+str(x)+' von countRef2: '+str(countRef2)
                item = decision()

                tempref2=entscheidreferenzen2[x].text


                item['referenz'] = tempref2.replace("/", "-")

                try:
                    link  = entscheidpdf2[x].get_attribute('href')
                except Exception:
                    self.logger.info('MISSERFOLG: scheitert beim Abrufen von Referenzen aus dem ARRAY')
                    self.driver.quit()

#                print 'LINK 2 und Zahl x ist: '+str(link)

#                item['url']=response.urljoin(link)
#                item['file_urls']=[item['url']]
                item['file_urls']=[response.urljoin(link)]
                yield item

            self.driver.save_screenshot("vor-dem-ende-der-schleife.png")
            ergebnis = NoSuchElementException
            next_page = None
            entscheidreferenzen2=[]

            try:
                page = WebDriverWait(self.driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(@id, "_id63next")]'))
                )
                self.logger.info('ERFOLG: naechste Seite ist vorhanden.')
                next_page = self.driver.find_element_by_xpath('//a[contains(@id, "_id63next")]')
            except Exception:
                self.logger.info('MISSERFOLG: keine naechste Seite _id63next')
                self.driver.quit()

        self.driver.quit()

class decision(scrapy.Item):
    file_urls = scrapy.Field()
    url = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

