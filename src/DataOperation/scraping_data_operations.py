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
# scraper end


def create_file_and_set_json_starting_brackets(file_name):
    file = open(file_name, 'w', encoding='utf-8')
    file.writelines('{\n')
    return file


def close_file_and_set_json_ending_bracets(file):
    file.writelines("}")
    file.close()


def transform_publication_to_json_object(publication):

    json_object = str('"publication": \n' + publication.to_json())
    return json_object


def write_scraped_data_to_file(file, scraped_data):
    scraped_len = len(scraped_data)-1
    for i in range(scraped_len+1):
        #  print(i, 'iteracja ')
        file.writelines(transform_publication_to_json_object(scraped_data[i]))
        if scraped_data[i] != scraped_data[scraped_len]:  # not last element
            file.writelines(', \n')  # file expect next json object


def create_file_path(file_name='newFile'):
    file_path_name = os.path.join(os.path.dirname(sys.argv[0]), 'data/')+file_name
    print(file_path_name)
    return file_path_name


# stat main functionality
# save to JSON object format
def save_to_file(scraped, file_name="scraped"):
    file_name = create_file_path(file_name+".json")
#  that could doesn't exist
    scraped_len = len(scraped)-1
    print(scraped_len, 'scraped len')
#  until here
    file = create_file_and_set_json_starting_brackets(file_name)
    write_scraped_data_to_file(file, scraped)
    close_file_and_set_json_ending_bracets(file)


#  sample data scraping
def scrap_page(Browser, keyword):
    Browser.get_sarching_page()
    page = main_search_page.MainSearchPage(Browser)
    page = page.search_by_keyword(keyword)
    scraped = []
    for j in range(page.number_of_results_pages):  # range(page.number_of_results_pages): # range(1):  #
        for i in range(len(page.results)):  # range(len(page.results)):
            # create publication_page; scrap publication data; kill publication_page
            publication_page = page.go_to_result_index(i)
            publication_page.create_publication()
            page.driver.back()
            page.get_refresh_page_object()
        page = page.go_to_next_result_page()
    print('pobrano dane ')
    return scraped

