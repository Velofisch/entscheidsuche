#  -*- coding: utf-8 -*-
__author__ = 'Tobias Mérinat, Stefan Balmer, Jörn Erbguth'

import scrapy
import re


class BernSpider(scrapy.Spider):
    """ Downloader for 'Entscheide der Zivil- und Strafgerichtsbarkeit'
        at http://www.zsg-entscheide.apps.be.ch/tribunapublikation/
    """
    name = "bern"

    # the following stuff has been extracted through manual analysis of page requests and responses
    RESULT_PAGE_URL = 'https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/loadTable'
    #RESULT_QUERY_TPL = r'''7|0|67|http://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/|9012D0DA9E934A747A7FE70ABB27518D|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.util.Map||0|OG|BM|BJS|EO|O|0;false|5;true|E:\\webapps\\a2j\\a2j-www-trbpub100web\\Thesaurus\\suisse.fts|1|java.util.HashMap/1797211028|reportpath|E:\\webapps\\a2j\\a2j-www-trbpub100web\\Reports\\ExportResults.jasper|viewtype|2|reporttitle|reportexportpath|E:\\webapps\\a2j\\a2j-www-trbpub100web\\Reports\\Export_1508526009959|reportname|Export_1508526009959|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|Gericht|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|40|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|5|5|5|5|7|9|9|5|5|5|5|5|5|10|11|6|0|0|6|5|5|12|5|13|5|14|5|15|5|16|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|20|{page_nr}|17|18|19|20|0|21|5|5|22|5|23|5|24|5|25|5|26|5|10|5|27|5|28|5|29|5|30|21|18|5|31|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|39|5|40|5|41|5|42|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|5|59|5|60|5|61|5|62|5|63|5|64|5|65|5|66|10|67|10|10|11|11|'''
    RESULT_QUERY_TPL = r'''7|0|67|https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/|9012D0DA9E934A747A7FE70ABB27518D|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.util.Map||0|OG|BM|BJS|EO|O|0;false|5;true|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Thesaurus\\suisse.fts|1|java.util.HashMap/1797211028|reportpath|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Reports\\ExportResults.jasper|viewtype|2|reporttitle|reportexportpath|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Reports\\Export_1592254990808|reportname|Export_1592254990808|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|Gericht|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|41|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|5|5|5|5|7|9|9|5|5|5|5|5|5|5|10|11|6|0|0|6|5|5|12|5|13|5|14|5|15|5|16|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|20|{page_nr}|17|18|19|20|0|21|5|5|22|5|23|5|24|5|25|5|26|5|10|5|27|5|28|5|29|5|30|21|18|5|31|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|39|5|40|5|41|5|42|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|5|59|5|60|5|61|5|62|5|63|5|64|5|65|5|66|10|67|10|10|11|11|0|'''
    HEADERS = { 'Content-type': 'text/x-gwt-rpc; charset=utf-8'
              , 'X-GWT-Permutation': 'C56BCDCE0FCCE64CB5164DE7BBAF017B'
              , 'X-GWT-Module-Base': 'https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/'
              }
    MINIMUM_PAGE_LEN = 148
    DOWNLOAD_URL = 'http://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/ServletDownload/'

    def request_generator(self):
        """ Generates scrapy requests for result pages
        """
        page_nr = 0
        while True:
            body = BernSpider.RESULT_QUERY_TPL.format(page_nr=page_nr)
            yield scrapy.Request(url=BernSpider.RESULT_PAGE_URL, method="POST", body=body,
                                 headers=BernSpider.HEADERS, callback=self.parse_page)
            page_nr += 1

    def __init__(self):
        super().__init__()
        self.request_gen = self.request_generator()

    def start_requests(self):
        # treat the first request, subsequent ones are generated and processed inside the callback
        yield next(self.request_gen)

    def parse_page(self, response):    
        """ Parses the current search result page, downloads documents and yields the request for the next search
        result page
        """

        if response.status == 200 and len(response.body) > BernSpider.MINIMUM_PAGE_LEN:
            # construct and download document links
            content = response.body_as_unicode().split('[')[2].split(']')[0]

            numbers = re.findall('\\"\D{2,3}\s\d\d\d\d\\s\d+\\"', content)
            identifiers = re.findall('\\"[0-9a-f]{32}\\"', content)

            for num, id_ in zip(numbers, identifiers):
                num = num[1:-1].replace(" ", "_")
                id_ = id_[1:-1]
                path_ = 'E:\\webapps\\a2j\\a2j-www-trbpub100web\\pdf_temp'
                href = "{}{}_{}.pdf?path={}\\{}.pdf&dossiernummer={}".format(BernSpider.DOWNLOAD_URL, num, id_,
                                                                             path_, id_, num)
                request = scrapy.Request(href, callback=self.download_doc)
                request.meta['number'] = num
                yield request
            yield next(self.request_gen)
        else:
            # base urls are depleted, let the download queue finish and then stop the spider
            pass
            
    def download_doc(self, response):
        """ Downloads and saves a single document
        """
        print("Download document")
        filename = "{}.pdf".format(response.meta['number'])
        with open(filename, 'wb') as f:
            f.write(response.body)
