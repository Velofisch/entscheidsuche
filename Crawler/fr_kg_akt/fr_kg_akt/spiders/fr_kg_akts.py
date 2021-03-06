# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import logging
import time
import os.path

# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options

from selenium.webdriver.chrome.options import Options

class FrKgAktsSpider(scrapy.Spider):
    name = 'fr_kg_akts'
    pfad = '/home/peter/testumgebung/files/entscheide/kantone/fr_kg_akt/'
    zaehl = 0
    allowed_domains = ['fr.ch']
    start_urls = ['https://publicationtc.fr.ch/?locale=de']


    def __init__(self):
# set user agent
        chrome_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36';
        firefox_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0';
        ie_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko';
        edge_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063';
        ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 " "(KHTML, like Gecko) Chrome/15.0.87'

        scrapy.Spider.__init__(self)

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x2580')
        self.driver = webdriver.Chrome(chrome_options=options)

        LOGGER.setLevel(logging.WARNING)


    def parse(self, response):
       self.driver.get(response.url)

# warte, bis der Suchknopf erscheint
       try:
           page = WebDriverWait(self.driver, 15).until(
               EC.presence_of_element_located((By.XPATH, '//i[contains(@class, "fa-search")][1]'))
           )
           self.logger.info('Warten auf Such-Knopf.')
#           self.driver.save_screenshot("wartenaufSuchKNOPF.png")
       except Exception:
           self.logger.info('Ausstieg bei Warten auf den Suchknopf')
           self.driver.quit()


# druecke Suchknopf
       try:
#           self.driver.find_element_by_xpath('//i[contains(@class, "fa-search")][1]').send_keys(Keys.RETURN)
           self.driver.find_element_by_xpath('//i[contains(@class, "fa-search")][1]').click()
           self.logger.info('Knopf gedrueckt.')
#           self.driver.save_screenshot("ERFOLG-Knopf-gedrueckt.png")
       except Exception:
           self.logger.info('GESCHEITERT: Knopf gedrueckt.')
           self.driver.quit()
       
#       self.driver.save_screenshot("knappnachclick-auf-Suchknopf.png")


# warte bis Suchergebnisse erscheinen
       try:
           page = WebDriverWait(self.driver, 15).until(
               EC.presence_of_element_located((By.XPATH, '//div[@class="grid-row-col3"]/div'))
           )
           self.logger.info('Suchergebnisse erscheinen.')
#           self.driver.save_screenshot("ERFOLG-SUCHERGEBNISSE-erscheinen.png")
       except Exception:
#           self.driver.save_screenshot("scheitern-bei-knappnachclick.png")
           self.logger.info('Ausstieg beim Warten auf die Ergebnisse nach dem Suchklick')
           self.driver.quit()


# -------------------------------------------------------------------------------------------------

# while - Schleife, welche abfragt, ob noch ein naechstes Element vorhanden ist

       next_page = self.driver.find_element_by_xpath('//div[@class="GB2UA-DDMN"]/i[@class="fa fa-angle-right tooltip"][1]') 

       while next_page is not None:
#           self.driver.save_screenshot("Eingang-while-Schleife.png")

# Auswahl aller Ergebnis-Elemente
           allentpag = self.driver.find_elements_by_xpath('//div[@class="grid-row-col3"]/div[1]')

           for einentpag in allentpag:
               self.zaehl += 1
               try:
                   page = WebDriverWait(self.driver, 40).until(
                       EC.presence_of_element_located((By.XPATH, '//div[@class="grid-row-col3"]/div[1]'))
                   )
                   einentpag.click()
#                   self.driver.save_screenshot("ERFOLG-bei-click.png")
                   self.logger.info('ERFOLG: klick hat geklappt.')
               except Exception:
                   self.driver.save_screenshot("scheitern-bei-click.png")
                   self.logger.info('MISSERFOLG: Titel im Ergebnisfenster ist vorhanden.')
                   self.driver.quit()

# hier wird geprueft, ob der Link mit der Bezeichnung vorhanden ist
               try:
                   page = WebDriverWait(self.driver, 40).until(
                       EC.presence_of_element_located((By.XPATH, '//div[@id="x-widget-3-label"]'))
                   )
#                   self.logger.info('ERFOLG: Titel im Ergebnisfenster ist vorhanden.')
#                   self.driver.save_screenshot("ERFOLG-Titel_im_Ergebnisfenster.png")
               except Exception:
                   self.driver.save_screenshot("scheitern-bei-knappnachclick.png")
                   self.logger.info('MISSERFOLG: Titel im Ergebnisfenster ist vorhanden.')
#           self.logger.info('Titel im Ergebnisfenster ist NICHT vorhanden')
                   self.driver.quit()

# erste einzelne Auswertung eines einzelnen Entscheides

               ref = self.driver.find_element_by_xpath('//div[@class="detailwordbreak"]').text
               fid = 'FR-TC-'+ref.replace(' ', '-')+'.html'
               html2 = self.driver.find_element_by_xpath('//div[@class="gwt-HTML"]/div/ div[@class="document"]').get_attribute('outerHTML').encode('utf-8')

               if os.path.isfile(self.pfad+fid):
                   self.logger.info('CHECK: File existiert.')
                   pass
               else:
                   with open(os.path.join(self.pfad+fid), 'w') as f:
                       f.write(html2)

               counter = self.driver.find_element_by_xpath('//div/span[@class="counter-result-lbl"]').text
               zmax = counter.rsplit(' ', 1)[-1]
               zmax = zmax.replace(')', '')
               zhoch = counter.rsplit(' ', 3)[-3]
               zmaxi = int(zmax)
               zhochi = int(zhoch)

               print fid
               print counter
               print zmaxi
               print zhochi

               print '-------------------------------------'+str(self.zaehl)


# der naechste Klick macht das Detailfenster zu
               self.driver.find_element_by_xpath('//i[@class="fa fa-close tooltip-down-left"]').click()
#               self.driver.find_element_by_xpath('//div[@class="detailwordbreak"][1]').send_keys(Keys.ESCAPE)
 #              self.driver.find_element_by_xpath('//div[@class="detailwordbreak"]').send_keys(Keys.ESCAPE)


           next_page = None

           if zhochi < zmaxi:
               try:
                   page = WebDriverWait(self.driver, 40).until(
                       EC.presence_of_element_located((By.XPATH, '//div[@class="GB2UA-DDMN"]/i[@class="fa fa-angle-right tooltip"]'))
                   )
                   next_page = self.driver.find_element_by_xpath('//div[@class="GB2UA-DDMN"]/i[@class="fa fa-angle-right tooltip"]') 
                   self.logger.info('ERFOLG: In while-Schleife am Ende.')
                   self.driver.save_screenshot("ERFOLG-In-while-Schleife-am-Ende.png")
               except Exception:
                   self.logger.info('MISSERFOLG: In while-Schleife am Ende.')
                   self.driver.save_screenshot("MISSERFOLG-In-while-Schleife-am-Ende.png")
                   self.driver.quit()


               try:
                   next_page.click()
#                   time.sleep(1)
                   self.logger.info('ERFOLG: In while-Schleife am Ende bei next_page-click.')
                   self.driver.save_screenshot("Erfolg-next-page-click-In-while-Schleife.png")
               except Exception:
#                   self.driver.save_screenshot("scheitern-bei-knappnachclick.png")
                   self.logger.info('GESCHEITERT: In while-Schleife beim Warten auf die Referenz') 
                   self.driver.quit()

       self.driver.quit()

# -------------------------------------------------------------------------------------------------

class decision(scrapy.Item):
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referenz = scrapy.Field()

