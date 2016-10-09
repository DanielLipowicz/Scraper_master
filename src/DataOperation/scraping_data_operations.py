import os.path
import sys
import codecs
from src import Browser
from src.PageObjects import main_search_page


# scraper
#
def scrap_data(keywords):
    browser = Browser.Browser()
    for keyword in keywords:
        print(keyword, ' starts:')
        scrap_page(browser, keyword)
        print(keyword, ' ends')


def scrap_page(Browser, keyword):
    Browser.get_bazEkon_page()
    page = main_search_page.MainSearchPage(Browser)
    page = page.search_by_keyword(keyword)
    scraped = []
    for j in range(page.number_of_results_pages):  # range(page.number_of_results_pages): # range(1):  #
        for i in range(len(page.results)):  # range(len(page.results)):
            publication_page = page.go_to_result_index(i)
            publication_page.create_publication()
            page.driver.back()
            page.get_refresh_page_object()
        page = page.go_to_next_result_page()
    print('pobrano dane ')
    return scraped

