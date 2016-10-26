import functools

import numpy

from src.databases import mongo_operations
from matplotlib import pyplot

mongo_connection = mongo_operations.get_new_connection_to_database('test', 'masterTest')
collection = mongo_connection.collection


def prepare_data():
    result = []

    def get_data_from_found_record(record):
        key_words_related = len(record.get("key_words"))
        # print(key_words_related)
        affiliations = record.get("affiliations")
        bibliography_count = len(record.get("bibliography"))
        year = record.get("year")
        is_university = 0
        for affiliation in affiliations:
            if affiliation != 'undefined':
                is_university = 1
                # print(affiliation)

        # table KW, BIBLIO, ROK, UCZELNIA
        result.append([key_words_related, bibliography_count, year, is_university])

    for i in collection.find():
        get_data_from_found_record(i)
    # for i in result:
    #     print(i)
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
            # for i in result:
            #     print(i)


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
        if 26 <= i[coll]:
            i[coll] = 6
            # for i in result:
            # print(i)


def clasify_year(result, coll=2):
    for i in result:
        colvar = i[coll].replace(")", "", 10)
        colvar = colvar.replace("(", "", 10)
        colvar = colvar.replace("'", "", 10)
        if len(colvar) <= 4:
            val = colvar[-4:]
        else:
            Exception()
        if type(int(val)) == type(str()):
            print(i[coll])
        elif 0 <= int(val) <= 1980:
            i[coll] = 0
        elif 1981 <= int(val) <= 1990:
            i[coll] = 1
        elif 1991 <= int(val) <= 2000:
            i[coll] = 2
        elif 2001 <= int(val) <= 2005:
            i[coll] = 3
        elif 2006 <= int(val) <= 2010:
            i[coll] = 4
        elif 2011 <= int(val) <= 2015:
            i[coll] = 5
        elif 2016 <= int(val):
            i[coll] = 6
    print("year clasyfi result", result)
    return result


def count_density_array(list_of_list_to_count, element_no=0):
    # return density_plot_list
    # table: y-density
    #       x-label
    density_plot_list = []
    for i in list_of_list_to_count:
        density_plot_list.append(i[element_no])
    x_dic = set(density_plot_list)
    x = []
    y = []
    for i in x_dic:
        y.append(density_plot_list.count(i))
    for i in range(len(y)):
        x.append(i)
    print("y parameter: ", y)
    print("x parameter: ", x)
    resultArray = [x, y]
    return resultArray


def count_density(list_to_count):

    x_dic = set(list_to_count)
    sorted(x_dic)
    x = []
    y = []
    for i in x_dic:
        y.append(list_to_count.count(i))
    for i in x_dic:
        if i==263:
            i=43
        x.append(i)

    print("y parameter: ", y)
    print("x parameter: ", x)
    resultArray = [x, y]
    return resultArray


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
        # print(i)
        # print(i[filter_by_column])
        if i[filter_by_column] == criteria:
            # print(True)
            function_result.append(i)
    return function_result;


def calculate_probability_all_results(result):
    probability_list = []

    for column_no in range(len(result[0])):
        probability = {}
        calculated_column = get_one_column_form_list(result, column_no)
        # print(calculated_column)
        column_attributes = get_attribute_name(calculated_column)
        # print("column attribute: ", column_attributes)
        for i in column_attributes:
            probability[i] = calculated_column.count(i) / len(calculated_column)
        probability_list.append(probability)
    return probability_list


def create_numpy_array(data_array, *take_columns):
    created_array = []
    for i in data_array:
        row = []
        for j in take_columns:
            row.append(i[j])
            # print(row)
        created_array.append(row)
    # print(created_array)
    return numpy.array(created_array)


result = []
result = prepare_data()
clasify_keywords(result)
clasify_bibliography(result)
clasify_year(result)
# draw_density_plot(result)
key_words_hist = count_density_array(result, 0)
# pyplot.bar(key_words_hist[0], key_words_hist[1], 1, label=key_words_hist[1])

bibliography_hist = count_density_array(result, 1)
pyplot.bar(bibliography_hist[0], bibliography_hist[1], 1, tick_label=bibliography_hist[0])

pyplot.bar(bibliography_hist[0], bibliography_hist[1])
pyplot.xticks(bibliography_hist[0], bibliography_hist[0])
pyplot.margins(0.02)

year_hist = count_density_array(result, 2)
pyplot.bar(year_hist[0], year_hist[1], 1)
# its works
width = 1
ind = numpy.arange(len(key_words_hist[0]))
pyplot.bar(ind, key_words_hist[1], 1)
pyplot.xticks(ind + width/2., key_words_hist[0])
# end
column = get_one_column_form_list(result, 1)
column.sort()
column = count_density(column)
width = 1
ind = numpy.arange(len(column[1]))
pyplot.bar(ind, column[1], 1)
pyplot.xticks(ind + width/2., column[0])


