from src.DataOperation import Publication
import logging


class PublicationPage:
    def __init__(self, browser):
        self.browser = browser
        self.driver = self.browser.driver
        self.article_author_elements = self.driver.find_elements_by_xpath \
            ('//div[@class="contributors"]//div[contains(@class,"articleDetails-contributorContentCell")]')
        self.article_title = self.driver.find_element_by_xpath('//div[@class="articleTitle hide-bullet"]/h3')
        self.article_keywords = self.driver.find_elements_by_xpath(
            '//div[@class="articleDetails-langCell articleDetails-langCell-first lang-icon lang-keyword"]'
            '[contains(text(),"PL")]/..//a')
        # optional elements
        self.browser.set_wait_time(1)
        self.article_author_affiliations = self.driver.find_elements_by_xpath \
            ('//div[@class="contributors"]//ul[@class="affiliations"]')
        self.publication_source = self.driver.find_element_by_xpath(
            '//div[@id="cont-source"]//div[text()="Czasopismo"]/../..//a')
        self.article_year = self.driver.find_element_by_xpath(
            '//div[@id="cont-source"]//div[text()="Rocznik"]/../..//a')
        self.article_bibliography = self.driver.find_elements_by_xpath('//ul[@class="plainList"]/li')
        self.browser.reset_waiting_time()

    def create_publication(self):
        publication = Publication.Publication()
        publication.article_title = self.article_title.text
        for i in range(len(self.article_author_elements)):
            print("affiliation loop: " + str(i))
            publication.authors.append(self.article_author_elements[i].text)
            try:
                self.browser.set_wait_time(1)
                affiliations= self.article_author_affiliations[i].text
            except:
                affiliations = 'undefined'
                self.browser.reset_waiting_time()
            publication.affiliations.append(affiliations)
        publication.publication_source = self.publication_source.text
        publication.year =self.article_year.text
        for i in range(len(self.article_keywords)):
            publication.key_words.append(self.article_keywords[i].text)
        for i in range(len(self.article_bibliography)):
            publication.bibliography.append(self.article_bibliography[i].text)

        print(publication.__dict__)
        self.browser.db.insert_one_if_doesnt_exist(publication.__dict__)

        return publication
