# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time


class TgsSpider(scrapy.Spider):
    name = 'tgs'
    allowed_domains = ['ogbuch.tg.ch']
    start_urls = ['http://ogbuch.tg.ch']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        LOGGER.setLevel(logging.WARNING)

    def parse(self, response):
        self.driver.get(response.url)

        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//frame[@name='menuFrame']"))
        )

        self.driver.switch_to.frame(element)

#        links = self.driver.find_elements_by_xpath('//a[contains(@href, "parent.aufzu")]')
#        links = self.driver.find_elements_by_xpath('//a[(contains(@href, "parent.aufzu")) and not (contains(@href, "register"))]')
#        links = self.driver.find_elements_by_xpath('//body/font/nobr/a and .//img[contains(@alt, "RBOG")]')
        links = self.driver.find_elements_by_xpath('//body/font/nobr/a')

#        self.driver.save_screenshot("weiter.png")

        for link in links:
            url = link.get_attribute('href')
            ref = link.get_attribute('text')
#            proper_url = response.urljoin(url)
#            print proper_url
            print url
            print ref
            link.click()
            time.sleep(2)
            self.driver.save_screenshot("weiter0.png")
            
            yield scrapy.Request(url=url, callback=self.entscheide)


    def entscheide(self, response):
        self.driver.save_screenshot("weiter2.png")
        self.__init__()
        self.driver.get(response.url)
        
        response.url.click()
        self.driver.save_screenshot("weiter3.png")
        unstu = self.driver.find_elements_by_xpath('//a[containts(text(), "html")]')
        for nr in unstu:
            u2 = nr.get_attribute('href')
            print u2

#        next_rbogs = self.driver.find_elements_by_xpath('')
#        for ent in next_rbogs:
#            link = ent.get_attribute('href')
#            print link 


    class decision(scrapy.Item):
        url = scrapy.Field()
        file_urls = scrapy.Field()
        files = scrapy.Field()
        referenz = scrapy.Field()
