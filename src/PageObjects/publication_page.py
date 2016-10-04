from src.DataOperation import Publication



class PublicationPage:
    def __init__(self, browser):
        self.browser = browser
        self.driver = self.browser.driver
        self.article_author_elements = self.driver.find_elements_by_xpath \
            ('//div[@class="contributors"]//div[contains(@class,"articleDetails-contributorContentCell")]')
        self.article_author_affiliations = self.driver.find_elements_by_xpath \
            ('//div[@class="contributors"]//ul[@class="affiliations"]')
        self.article_title = self.driver.find_element_by_xpath('//div[@class="articleTitle hide-bullet"]/h3')
        self.article_keywords = self.driver.find_elements_by_xpath(
            '//div[@class="articleDetails-langCell articleDetails-langCell-first lang-icon lang-keyword"]'
            '[contains(text(),"PL")]/..//a')
        # optional elements
        self.browser.set_wait_time(5)
        self.publication_source = self.driver.find_element_by_xpath('//div[text()="Czasopismo"]/../..//a')
        self.article_year = self.driver.find_element_by_xpath('//div[text()="Rocznik"]/../..//a')
        self.article_bibliography = self.driver.find_elements_by_xpath('//ul[@class="plainList"]/li')
        self.browser.reset_waiting_time()

    def create_publication(self):
        publication = Publication.Publciation()
        publication.article_title = self.article_title.text
        for i in range(try_to_count_elements(self.article_author_elements)):
            publication.authors.append(try_to_read(self.article_author_elements[i]))
            publication.affiliations.append(try_to_read(i))
        publication.publication_source = try_to_read(self.publication_source)
        publication.year = try_to_read(self.article_year)
        for i in range(try_to_count_elements(self.article_keywords)):
            publication.key_words.append(try_to_read(self.article_keywords[i]))
        for i in range(try_to_count_elements(self.article_bibliography)):
            publication.bibliography.append(try_to_read(self.article_bibliography[i]))

        print(publication.__dict__)
        self.browser.db.insert_one_if_doesnt_exist(publication.__dict__)

        return publication

    def try_to_read_affiliations(self, affiliations_index):
        try:
            return self.article_author_affiliations[affiliations_index]
        except:
            return "undefined"

def try_to_read(element):
    try:
        return element.text
    except:
        return "undefined"


def try_to_count_elements(elements):
    try:
        return len(elements)
    except:
        return 0


