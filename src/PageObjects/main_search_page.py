from src.PageObjects import searching_results_page


class MainSearchPage:
    def __init__(self, browser):
        self.driver = browser.driver
        self.input_element_search_by_title = self.driver.find_element_by_id("EQUALS_names")
        self.input_element_search_by_author = self.driver.find_element_by_id("EQUALS_author")
        self.input_element_search_by_keyword = self.driver.find_element_by_id("EQUALS_keywords")
        self.combo_search_from_year = self.driver.find_element_by_name("GREATER_EQUAL_published_combo")
        self.combo_search_to_year = self.driver.find_element_by_name("LESS_EQUAL_published_combo")
        self.button_element_search = self.driver.find_element_by_id("ANY_submitButton")
        self.button_element_clean = self.driver.find_element_by_id("ANY_resetButton")

    def search_by_keyword(self, keyword):
        self.button_element_clean.click()
        self.input_element_search_by_keyword.send_keys(keyword)
        self.button_element_search.click()
        return searching_results_page.SearchingResultsPage(self.browser)

    def input_author(self, author):
        self.input_element_search_by_author.send_keys(author)

    def input_keyword(self, keyword):
        self.input_element_search_by_keyword.send_keys(keyword)

    def click_search(self):
        self.button_element_search.click()
        return searching_results_page.SearchingResultsPage(self.browser)

    def click_clean(self):
        self.button_element_clean.click()
