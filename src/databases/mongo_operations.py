from src.databases import mogodbConfig
from src.data_visualisation import pyplot_usage
from src.DataOperation import select_operations


def select_distinct_key_words(collection):
    list = []
    for i in collection.distinct("key_words"):
        list.append(i)
    return list
con = mogodbConfig.mongoConnection()
# keywords_base = select_distinct_key_words(con.collection)


def find_in_database_by_keyword(conn, keyword, to_find='_id'):
    result = []
    for i in conn.collection.find({"key_words": keyword}, {"key_words": 1, to_find: 1}):
        result.append(i[to_find])
    return result


def get_publications_with_keyword(conn, keyword):
    # publication_id_table = find_in_database_by_keyword(conn, keyword, '_id')
    keywords_table = find_in_database_by_keyword(conn, keyword, "key_words")
    result = list(set(keywords_table))
    result.sort()
    return result


def get_connected_publication(conn, connectet_with_keyword):
    result = find_in_database_by_keyword(conn, connectet_with_keyword, "_id")
    return result


def get_density_of_keywords(keywords):
    density_of_keywords = {}
    set_keywords = set(keywords)
    for keyword in set_keywords:
        keyword_quantity = keywords.count(keyword)
        density_of_keywords.update({keyword: keyword_quantity})
    return density_of_keywords


def get_data_about_keyword(keyword):
    data = select_operations.get_all_keywords_related(con, keyword)
    quantity_keywords = get_density_of_keywords(data)
    return quantity_keywords

