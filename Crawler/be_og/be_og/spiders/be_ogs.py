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
from selenium.webdriver.chrome.options import Options


class BeOgsSpider(scrapy.Spider):
    name = 'be_ogs'
    allowed_domains = ['be.ch']
    start_urls = ['http://www.zsg-entscheide.apps.be.ch/tribunapublikation/']
    pfad = '/home/peter/testumgebung/files/entscheide/kantone/be_og/'
    zaehl = 0


    def __init__(self):
        scrapy.Spider.__init__(self)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1280x3580')
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
           self.driver.save_screenshot("ERFOLG-Knopf-gedrueckt.png")
       except Exception:
           self.logger.info('GESCHEITERT: Knopf gedrueckt.')
           self.driver.quit()
           self.driver.save_screenshot("knappnachclick-auf-Suchknopf.png")

       time.sleep(3)

# warte bis Suchergebnisse erscheinen
       try:
           page = WebDriverWait(self.driver, 15).until(
               EC.presence_of_element_located((By.XPATH, '//div[@class="grid-row-col3-def"]/div'))
           )
           self.logger.info('Suchergebnisse erscheinen.')
           self.driver.save_screenshot("ERFOLG-SUCHERGEBNISSE-erscheinen.png")
       except Exception:
           self.driver.save_screenshot("scheitern-bei-knappnachclick.png")
           self.logger.info('MISSERFOLG: Ausstieg beim Warten auf die Ergebnisse nach dem Suchklick')
           self.driver.quit()


# -------------------------------------------------------------------------------------------------

# while - Schleife, welche abfragt, ob noch ein naechstes Element vorhanden ist

       next_page = self.driver.find_element_by_xpath('//div[@class="GB2UA-DDMN"]/i[@class="fa fa-angle-right tooltip"][1]')
       print '--------------------------------------'
#       print np
       print next_page
       print '--------------------------------------'


       while next_page is not None:
#           self.driver.save_screenshot("Eingang-while-Schleife.png")

# Auswahl aller Ergebnis-Elemente
           allentpag = self.driver.find_elements_by_xpath('//div[@class="grid-row-col3-def"]/div[1]')

           for einentpag in allentpag:
               self.zaehl += 1
               try:
                   page = WebDriverWait(self.driver, 40).until(
                       EC.presence_of_element_located((By.XPATH, '//div[@class="grid-row"]/div[@class="grid-row-col3-def"]/div[1]'))
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
                   self.driver.quit()

# erste einzelne Auswertung eines einzelnen Entscheides

               ref = self.driver.find_element_by_xpath('//table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[@class="detailwordbreak"]').text
#               lol = ref.replace(' ', '-')+'.pdf'
               fid = 'BE-OG-'+ref.replace(' ', '-')+'.html'
#               ref = 'FR-TC-'+ref.replace(' ', '-')+'.pdf'
#               html = self.driver.page_source.encode('utf-8')
#               html2 = self.driver.find_element_by_tag_name('html').get_attribute('innerHTML').encode('utf-8')

# --------------------------

               ref2 = 'BE-OG-'+ref.replace(' ', '-').encode('utf-8')
               h2s = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"><title>'+ref2+'</title></head><body><h3>'+ref2+'</h3>'.encode('utf-8')

               html2 = self.driver.find_element_by_xpath('//div[@class="gwt-HTML"]/div/ div[@class="document"]').get_attribute('outerHTML').encode('utf-8')

               f2e = '</body></html>'.encode('utf-8') 
               html3 = h2s+html2+f2e

               print html3

# --------------------------

               if os.path.isfile(self.pfad+fid):
                   self.logger.info('CHECK: File existiert.')
                   pass
               else:
                   with open(os.path.join(self.pfad+fid), 'w') as f:
                       f.write(html3)

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

#               self.driver.save_screenshot("ESCAPE.png")

# der naechste Klick macht das Detailfenster zu
               self.driver.find_element_by_xpath('//i[@class="fa fa-close tooltip-down-left"]').click()
#               self.driver.find_element_by_xpath('//div[@class="detailwordbreak"][1]').send_keys(Keys.ESCAPE)
 #              self.driver.find_element_by_xpath('//div[@class="detailwordbreak"]').send_keys(Keys.ESCAPE)
#               time.sleep(1)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

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


