import functools

from src.databases import mongo_operations
from matplotlib import pyplot

mongo_connection = mongo_operations.get_new_connection_to_database()
collection = mongo_connection.collection


def prepare_data():
    result = []

    def get_data_from_found_record(record):
        key_words_related = len(record.get("key_words"))
        print(key_words_related)
        affiliations = record.get("affiliations")
        bibliography_count = len(record.get("bibliography"))
        year = record.get("year")
        is_university = 0
        for affiliation in affiliations:
            if affiliation != 'undefined':
                is_university = 1
                print(affiliation)

        # table KW, BIBLIO, ROK, UCZELNIA
        result.append([key_words_related, bibliography_count, year, is_university])

    for i in collection.find():
        get_data_from_found_record(i)
    for i in result:
        print(i)
    return result


def clasify_keywords(result):
    for i in result:
        if 0 <= i[0] <= 2:
            i[0] = 1
        if 3 <= i[0] <= 4:
            i[0] = 2
        if 5 <= i[0] <= 6:
            i[0] = 3
        if 6 < i[0]:
            i[0] = 4
    for i in result:
        print(i)


def clasify_bibliography(result, coll=1):
    for i in result:
        if 0 <= i[coll] <= 5:
            i[coll] = 1
        if 6 <= i[coll] <= 10:
            i[coll] = 2
        if 11 <= i[coll] <= 15:
            i[coll] = 3
        if 16 <= i[coll] <= 20:
            i[coll] = 4
        if 21 <= i[coll] <= 25:
            i[coll] = 5
        if 26 < i[coll]:
            i[coll] = 6
    for i in result:
        print(i)


def clasify_year(result, coll=2):
    for i in result:
        if 0 <= i[coll] <= 1980:
            i[coll] = 'to 1980'
        if 1981 <= i[coll] <= 1990:
            i[coll] = 'from 1981 to 1990'
        if 1991 <= i[coll] <= 2000:
            i[coll] = 'from 1991 to 2000'
        if 2001 <= i[coll] <= 2005:
            i[coll] = 'from 2001 to 2005'
        if 2006 <= i[coll] <= 2010:
            i[coll] = 'from 2006 to 2010'
        if 2011 <= i[coll] <= 2015:
            i[coll] = 'from 2011 to 2015'
        if 2016 <= i[coll]:
            i[coll] = 'from 2016'
    for i in result:
        print(i)
    return result

def draw_density_plot(list_of_list_to_count, element_no=0):
    key_words_list = []
    for i in list_of_list_to_count:
        key_words_list.append(i[element_no])
    x_dic = set(key_words_list)
    x = []
    y = []
    for i in x_dic:
        y.append(key_words_list.count(i))
    for i in range(len(y)):
        x.append(i)
    print("y parameter: ", y)
    print("x parameter: ", x)
    pyplot.plot(x, y)
    return key_words_list.sort()


result = []
result = prepare_data()
clasify_keywords(result)
# draw_density_plot(result)
clasify_bibliography(result)
draw_density_plot(result, 1)


def get_one_column_form_list(nested_list=[], column=0):
    # return one column from nested list
    list_to_count = []
    for i in nested_list:
        list_to_count.append(i[column])
    return list_to_count


def get_attribute_name(data):
    # return unique value from list
    result = []
    for i in data:
        if i not in result:
            result.append(i)
    return result


def filter_result(result, filter_by_column, criteria):
    function_result = []
    for i in result:
        print(i)
        print(i[filter_by_column])
        if i[filter_by_column] == criteria:
            print(True)
            function_result.append(i)
    return function_result;


def calculate_probability_all_results(result):
    probability_list = []

    for column_no in range(len(result[0])):
        probability = {}
        calculated_column = get_one_column_form_list(result, column_no)
        print(calculated_column)
        column_attributes = get_attribute_name(calculated_column)
        print("column attribute: ", column_attributes)
        for i in column_attributes:
            probability[i] = calculated_column.count(i) / len(calculated_column)
        probability_list.append(probability)
    return probability_list
