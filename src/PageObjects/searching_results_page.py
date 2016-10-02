from src.PageObjects import publication_page


class SearchingResultsPage:
    def __init__(self, browser):
        self.browser = browser
        self.driver = self.browser.driver
        self.results = None
        self.number_of_results_pages = None
        self.number_of_results_pages = None
        self.button_next_pages = None
        self.number_of_current_page = None
        self.get_refresh_page_object()

    def go_to_result_index(self, index):
        self.results[index].click()
        return publication_page.PublicationPage(self.browser)

    def get_refresh_page_object(self):
        self.results = self.driver.find_elements_by_class_name("titleText")
        self.number_of_results_pages = self.driver.find_elements_by_class_name("number-of-pages")[1].text
        self.number_of_results_pages = eval(self.number_of_results_pages[1:])
        self.button_next_pages = self.driver.find_elements_by_xpath('//img[@alt="next"]')
        self.number_of_current_page = self.driver.find_element_by_class_name("currentPage").text

    def go_to_next_result_page(self):
        self.button_next_pages[1].click()
        return SearchingResultsPage(self.browser)





