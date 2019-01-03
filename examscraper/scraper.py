import urllib3

import splinter
from selenium import webdriver

def __init__():
    pass

urllib3.disable_warnings()

class Scraper:
    def __init__(self, starturl):
        self.url = starturl
        self.filters = []
        self.documents = []

        # Initialize HTTP
        self.http = urllib3.PoolManager()
        # Start browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        self.browser = splinter.Browser('chrome', options=chrome_options)
        self.browser.driver.maximize_window()
        self.browser.visit(starturl)

    def set_filters(self, filters):
        self.filters = filters

    # Append an array of filters to the current array of filters
    def add_filters(self, filters):
        self.filters += filters

    # Apply filters
    def apply_filters(self):
        filtered = self.documents
        for curfilter in self.filters:
            filtered = filter(curfilter, filtered)
        self.documents = list(filtered)

    def find_urls(self, contained_word):
        elements = self.browser.find_link_by_partial_href(contained_word)
        for element in elements:
            document = {
                'href': element['href'],
                'linkText': element['text'],
                'filename': element['href'].split('/')[-1]
            }
            print(document)
            self.documents.append(document)
        if self.filters:
            self.apply_filters()

    def read(self):
        for document in self.documents:
            response = self.http.request('GET', document['href'])
            document['data'] = response.data

        result = self.documents
        self.documents = {}
        return result

    def close(self):
        self.browser.quit()
