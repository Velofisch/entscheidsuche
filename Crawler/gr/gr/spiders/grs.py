# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.remote_connection import LOGGER
from datetime import date
from time import strftime
from datetime import datetime
import logging
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys


class GrsSpider(scrapy.Spider):
    name = 'grs'
    allowed_domains = ['lawsearch.gr.ch']
    start_urls = ['http://www.lawsearch.gr.ch/le/']

    def parse(self, response):
        pass

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=['--cookies-file=/cookies.txt'])
# --------------------------------- https://github.com/ariya/phantomjs/issues/11637
# ---------------------------------- http://yizeng.me/2014/02/23/how-to-get-window-size-resize-or-maximize-window-using-selenium-webdriver/
#        self.driver.maximize_window();
# Achtung, wenn das Fenster zu klein ist, dann klapt der click unten nicht!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.driver.set_window_size(1500, 2500)
        LOGGER.setLevel(logging.WARNING)

    def parse(self, response):
        self.driver.get(response.url)

# Versuch, mit Datumbereich alles zu suchen!!!!!!!!!!!!
#  https://www.seehuhn.de/pages/pdate.html
#https://stackoverflow.com/questions/22739015/convert-date-from-mm-dd-yyyy-to-another-format-in-python#22739059

#        startdatum = "01.01."+str(date.today().year-1)
        startdatum = "01.01."+str(date.today().year)

        endtag = str(date.today().day)
        endmonat = str(date.today().month)
        endjahr = str(date.today().year)

        enddatum = endtag+'.'+endmonat+'.'+endjahr

#        startdatum = "01.01.2015"
#        enddatum = "01.01.2016"

        print 'Heute_string:: '+enddatum
        print 'Startdatum: '+startdatum
        print '==================================================================='

# suche nach dem Knopf fuer das Publikationsdatum

        try:
            page = WebDriverWait(self.driver, 19).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="v-button-caption"][contains(., "Publikationsdatum")]'))
            )
#            self.driver.save_screenshot("SUCCESS-SUCHE-NACH-DEM-KNOPF-FUER-DAS-PULIKATIONSDATUM.png")
        except Exception:
            self.logger.info('quitting driver on SUCHE NACH DEM KNOPF FIER DAS PUBLIKATIONSDATUM')
#            self.driver.save_screenshot("ERROR-SUCHE-NACH-DEM-KNOPF-FUER-DAS-PULIKATIONSDATUM.png")
            self.driver.quit()

# Klick auf das Publikationsdatumsfeld

        self.driver.find_element_by_xpath('//div[@class="v-button v-widget link v-button-link"]/span/span[@class="v-button-caption"][contains(., "Publikationsdatum")]').click()

# suche nach dem Knopf fuer BENUTZERDEFINIERTE BENUTZEREINGABEN FUER DAS DATUM

        try:
            page = WebDriverWait(self.driver, 19).until(
                EC.presence_of_element_located((By.XPATH, '//div/span/span[@class="v-button-caption"][contains(., "Benutzerdefiniert")]'))
            )
#            self.driver.save_screenshot("SUCCESS-BENUTZERDEFINIERTE-BENUTZEREINGABEN-FUER-DAS-DATUM.png")
        except Exception:
            self.logger.info('quitting driver on BENUTZERDEFINIERTE BENUTZEREINGABEN FUER DAS DATUM ')
#            self.driver.save_screenshot("ERROR-BENUTZERDEFINIERTE-BENUTZEREINGABEN-FUER-DAS-DATUM.png")
            self.driver.quit()

# Klick auf das FELD fuer benutzerdefinierte Benutzereingaben

        self.driver.find_element_by_xpath('//div/span/span[@class="v-button-caption"][contains(., "Benutzerdefiniert")]').click()

# MUSS MAN JETZT NOCH DEN FOCUS WECHSELN ???????????????????????????????????????????# MUSS MAN JETZT NOCH DEN FOCUS WECHSELN ?????????????????????????????????????????????


# nach drte auf den Knopf fuer PERIODE 

        try:
            page = WebDriverWait(self.driver, 19).until(
                EC.presence_of_element_located((By.XPATH, '//div/span/span[@class="v-button-caption"][contains(., "Periode")]'))
            )
#            self.driver.save_screenshot("SUCCESS-PERIODE.png")
        except Exception:
            self.logger.info('quitting driver on BENUTZERDEFINIERTE BENUTZEREINGABEN FUER PERIODE ')
#            self.driver.save_screenshot("ERROR-PERIODE.png")
            self.driver.quit()

# Klick auf das FELD fuer benutzerdefinierte PERIODE 

        self.driver.find_element_by_xpath('//div/span/span[@class="v-button-caption"][contains(., "Periode")]').click()

# nach drte auf den Knopf fuer PERIODE

        try:
            page = WebDriverWait(self.driver, 19).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="gwt-uid-15"][@type="text"]'))
            )
#            self.driver.save_screenshot("SUCCESS-PERIODE-EINGABEFELD-STARTDATUM.png")
        except Exception:
            self.logger.info('quitting driver on BENUTZERDEFINIERTE BENUTZEREINGABEN FUER STARTDATUM ')
#            self.driver.save_screenshot("ERROR-PERIODE-EINGABEFELD-STARTDATUM.png")
            self.driver.quit()


# Klick auf das STARTFELD

        self.driver.find_element_by_xpath('//input[@id="gwt-uid-15"][@type="text"]').click()


# EINGABE des STARTDATUMTS

        eingabefeld = self.driver.find_element_by_xpath('//input[@id="gwt-uid-15"][@type="text"]')

        eingabefeld.send_keys(startdatum)
#        eingabefeld.send_keys(Keys.RETURN)
        eingabefeld.send_keys("\n")
#        self.driver.save_screenshot("STARTDATUM-EINGEGEBEN-RETURN-GEDRUECKT.png")


# ist hinzufuegen - Knopf hier`?????????????????
        try:
            page = WebDriverWait(self.driver, 19).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="v-button-caption"][contains(., "hinzuf")]'))
            )
            self.driver.save_screenshot("SUCCESS-HINZUFUEGEN-KNOPF-IST-ERREICHBAR.png")
        except Exception:
            self.logger.info('quitting driver on BENUTZERDEFINIERTE BENUTZEREINGABEN FUER STARTDATUM ')
            self.driver.save_screenshot("ERROR-HINZUFUEGEN-KNOPF-IST-ERREICHBAR.png")
            self.driver.quit()

        
#        self.driver.find_element_by_xpath('//span[@class="v-button-caption"][contains(text(), "hinzuf")]').click
#        time.sleep(1)
#        self.driver.find_element_by_xpath('//span[@class="v-button-caption"][contains(., "schliess")]').click
#        time.sleep(1)
#        self.driver.save_screenshot("STARTDATUM-HINZUGEFUEGT-999999999.png")

# --------------------------------- https://stackoverflow.com/questions/17870528/double-clicking-in-python-selenium fuer doppelclick

        driver=self.driver
        actionChains = ActionChains(driver)
        knopf = self.driver.find_element_by_xpath('//span[@class="v-button-caption"][contains(text(), "hinzuf")]')
#        actionChains.double_click(knopf).perform()        
        actionChains.click(knopf).perform()        
        time.sleep(1)
        self.driver.save_screenshot("STARTDATUM-00000000000000.png")

# jetzt noch den Datumsbereich in das LABELFELD ziehen mit DOPPELKLICK

#        bereich = self.driver.find_element_by_xpath('//div[contains(@aria-describedby="gwt-uid-2")][contains(., "01.01")]')
#        bereich = self.driver.find_element_by_xpath('//div[contains(@class="v-label v-widget lefieldlabel-full v-label-lefieldlabel-full field-publikationsdatum v-label-field-publikationsdatum v-label-undef-w")][contains(., "01.01")]')

#        driver1=self.driver
#        actionChains1 = ActionChains(driver1)
        liste = self.driver.find_elements_by_xpath('//div[@class="v-label v-widget lefieldlabel-full v-label-lefieldlabel-full field-publikationsdatum v-label-field-publikationsdatum v-label-undef-w"]')
        bereich = liste[5]
#        bereich = self.driver.find_element_by_xpath('//div[contains(., "01.01.20")]')
#        actionChains1.double_click(bereich).perform()
        actionChains.double_click(bereich).perform()
        time.sleep(1)
        self.driver.save_screenshot("DOPPELKLICK-00000000000000.png")

#        sys.exit()

# suche nach dem SuchFELD
        print '===================== vor dem check, ob das suchfeld da ist =============================================='

        try:
            page = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="v-button-wrap"]'))
            )
        except Exception:
            self.logger.info('quitting driver on first page trying to get content')
            self.driver.quit()


# Klick auf das Suchfeld
        print '===================== vor dem click ins suchfeld  =============================================='

# ------------------------------------ cut 

#        self.driver.find_element_by_xpath('//div[@id="searchinput-submit"]/div/span[@class="v-button-wrap"]').click()

#        try:
#            page2 = WebDriverWait(self.driver, 9).until(
#                EC.presence_of_element_located((By.XPATH, '//img[@class="v-icon"]'))
#            )
#            self.logger.info('ist die Klasse v-icon da - JAAAAAAAA ')
#        except Exception:
#            self.logger.info('quitting driver')
#            self.driver.quit()

# ------------------------------------ cut 

#        newlinks2 = self.driver.find_elements_by_xpath('//a[contains(@href, "lehit")]')
#        pdflinks2 = self.driver.find_elements_by_xpath('//div[contains(@class, "custom-result-component-original")]/a[contains(@href, "download")]')

        try:
            page2 = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "dossnr")]'))
            )
            self.logger.info('sind die DOSSNR da - JAAAAAAAA ')
        except Exception:
            self.logger.info('quitting driver')
            self.driver.quit()


        newlinks2 = self.driver.find_elements_by_xpath('//a[contains(@href, "dossnr")]')
        pdflinks2 = self.driver.find_elements_by_xpath('//div[contains(@class, "custom-result-component-original")]/a[contains(@href, "ntscheid")]')

        self.lauf = 0

        for newlink2 in newlinks2:
            item = decision()
            url = newlink2.get_attribute('href')
            proper_url = response.urljoin(url)
            referenz = newlink2.get_attribute('text')
            referenz = referenz.replace(' Nr. ','-')
            referenz = referenz.replace('/','-')
            referenz = referenz.replace(' ','-')+'.pdf'
#            referenz = referenz.replace(' ','-')+'.html'

            print 'URL: '+url
            print 'Referenz: '+referenz
            pdf = pdflinks2[self.lauf]
            pdf_url = pdf.get_attribute('href')
#            print 'PDF URL: '+pdf_url

            item['referenz'] = referenz
            item['file_urls'] = [pdf_url]
#            item['file_urls'] = [proper_url]
            yield item

            self.lauf = self.lauf + 1
#            self.zahl = self.zahl + 1

        try:
            next_page = self.driver.find_element_by_xpath('//div[contains(@class, "result-pager-next")]/div[contains(@class, "active")]/div/div[contains(@class, "v-label v-widget simplebutton v-label-simplebutton v-label-undef-w")]')
            self.logger.info('naechste seite vorhanden (untere schleife) ! -------------------------------')
        except Exception:
            self.logger.info('naechste Seite ist NICHT vorhanden ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ')
            self.driver.quit()      

        self.driver.save_screenshot("wiesobrichtdasdinghierab.png")
#        while (next_page.text == 'WEITER' or next_page.text=='Avancer'):
        while next_page is not None:

            next_page.click()            
# -------------------------------------------------------------------
            self.driver.save_screenshot("nach-click.png")

            try:
                page2 = WebDriverWait(self.driver, 25).until(
                    EC.presence_of_element_located((By.XPATH, '//img[@class="v-icon"]'))
                )
                self.logger.info('naechste seite nach click vorhanden (Wartefunktion) ! -------------------------------')
                self.driver.save_screenshot("naechste-seite-nach-click-vorhanden.png")
            except Exception:
                self.logger.info('quitting driver')
                self.driver.quit()

#            time.sleep(3)

            try:
                page2 = WebDriverWait(self.driver, 25).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "dossnr")]'))
                )
                self.logger.info(' Suche nach dossnummer ! -------------------------------')
                self.driver.save_screenshot("suche-nach-dossnummer.png")
            except Exception:
                self.logger.info('quitting driver')
                self.driver.quit()


            try:
                page2 = WebDriverWait(self.driver, 25).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "download")]'))
                )
                self.logger.info(' Suche nach download ! -------------------------------')
                self.driver.save_screenshot("suche-nach-download.png")
            except Exception:
                self.logger.info('quitting driver bei download ')
                self.driver.quit()


#            newlinks = self.driver.find_elements_by_xpath('//a[contains(@href, "lehit")]')
            newlinks = self.driver.find_elements_by_xpath('//a[contains(@href, "dossnr")]')

            pdflinks = self.driver.find_elements_by_xpath('//div[contains(@class, "custom-result-component-original")]/a[contains(@href, "download")]')
#            pdflinks = self.driver.find_elements_by_xpath('//div[contains(@class, "custom-result-component-original")]/a[contains(@href, "ntscheid")]')
#            entscheiddatumlinks = self.driver.find_elements_by_xpath('//div[contains(@class, "v-label-field-entscheiddatum")]')
#            publikationsdatumlinks = self.driver.find_elements_by_xpath('//div[contains(@class, "v-label-field-publikationsdatum")]')

            self.driver.save_screenshot("vor-zweiter-schlaufe.png")

            index2 = 0

            for newlink in newlinks:

                item = decision()
                url = newlink.get_attribute('href')
                proper_url = url
#                proper_url = response.urljoin(url)
                referenz = newlink.get_attribute('text')
                referenz = referenz.replace(' Nr. ','-')
                referenz = referenz.replace('/','-')
                referenz = referenz.replace(' ','-')+'.pdf'
#                referenz = referenz.replace(' ','-')+'.html'
#                print 'URL: '+proper_url
#                print 'Referenz: '+referenz
#                print 'Betreff: '+betreff

                pdf = pdflinks[index2]
                pdf_url = pdf.get_attribute('href')
#                print 'PDF URL: '+pdf_url

                item['referenz'] = referenz
#                item['file_urls'] = [proper_url]
                item['file_urls'] = [pdf_url]
                yield item 

                self.driver.save_screenshot("in-zweiter-schlaufe.png")
                index2 = index2 + 1
#                self.zahl = self.zahl + 1

            next_page = None

            time.sleep(2.5)

            try:
                page = WebDriverWait(self.driver, 59).until(
#                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "result-pager-next")]/div[contains(@class, "next-active")]/div/div[contains(@class, "v-label v-widget simplebutton v-label-simplebutton v-label-undef-w")]'))
                    EC.presence_of_element_located((By.XPATH, '//div/div/div[contains(@class, "v-label v-widget simplebutton v-label-simplebutton v-label-undef-w")][contains(., "Weiter")]'))
                )
            except Exception:
                self.logger.info('sucht in der try-Abfrage den next button und findet ihn nicht')
                self.driver.quit()

            try:
                self.driver.save_screenshot("evaluiert-nextpage-pfad.png")
#                next_page = self.driver.find_element_by_xpath('//div[contains(@class, "result-pager-next")]/div[contains(@class, "next-active")]/div/div[contains(@class, "v-label v-widget simplebutton v-label-simplebutton v-label-undef-w")]') 
                next_page = self.driver.find_element_by_xpath('//div/div/div[contains(@class, "v-label v-widget simplebutton v-label-simplebutton v-label-undef-w")][contains(., "Weiter")]') 
                self.driver.save_screenshot("weiter-in-2-schleife-am-ende-vor-next-page.png")
                self.logger.info('versucht, die naechste Seite zu finden - zweite Schlaufe')
            except Exception:
#            except NoSuchElementException:
                self.logger.info('abbruch bei der abfrage von weiter element -----------------------')
                self.driver.save_screenshot("abbruch-ganz-hinten.png")
                next_page is None
                self.driver.quit()

#        self.driver.quit()


class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

