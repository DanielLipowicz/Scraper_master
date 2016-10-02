import json


class Publciation:
    def __init__(self):

        self.article_title = None
        self.authors = []
        self.affiliations = None
        self.publication_source = None
        self.year = None
        self.key_words = []
        self.bibliography = []

    def print_publication(self, i):
        print('lp. ', i)
        print(self.article_title)
        print(self.authors)
        print(self.year)
        print(self.key_words)
        print(self.bibliography)

    def to_json(self):
        to_json = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
        return str(to_json)

    def json_dumps(self):
        to_json = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
        print(to_json)
        return to_json

    def json_encode(self):
        js = json.JSONEncoder(self)
        return js

    def return_list(self):
        to_return = []
        to_return.append(self.article_title)
        for each in self.authors:
            to_return.append(each)
        to_return.append(self.year)
        for each in self.key_words:
            to_return.append(each)
        for each in self.bibliography:
            to_return.append(each)
        return to_return