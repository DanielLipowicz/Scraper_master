def read_all_publication(publications):
    publication_dict = publications['publication']
    for each in publication_dict:
        print(each)


def get_all_keywords_related(conn, keyword):
    related_keywords_with_duplicates = []
    print('getting all keywords related')
    for i in conn.collection.find({'key_words': keyword}, {"key_words": 1, '_id': 0}):
        for j in i['key_words']:
            related_keywords_with_duplicates.append(j)
    return related_keywords_with_duplicates

