import functools

import numpy

from src.databases import mongo_operations
from matplotlib import pyplot

mongo_connection = mongo_operations.get_new_connection_to_database()
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

# result=secound_prepare_date()
def secound_prepare_date():
    result = []
    for result_row in collection.find():
        for affiliation_dict in result_row['affiliations']:
            if affiliation_dict!='undefined':
                result.append(result_row)


    return result
def print_distinct(result):
    lista=[]
    for i in result:
        for j in i["affiliations"]:
            lista.append(j)
    dist_list = set(lista)
    dist_list = sorted(dist_list)
    for i in dist_list:
        print(i)

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
# draw_density_plot(result),

# column = get_one_column_form_list(result, 1)
# column.sort()
# column = count_density(column)
# width = 1
# ind = numpy.arange(len(column[1]))
# pyplot.bar(ind, column[1], 1)
# pyplot.xticks(ind + width/2., column[0])
#
def generate_pyplot_bar(x,y, len=None):
    if len==None:
        len=len(x)
    width = 1
    ind = numpy.arange(len)
    pyplot.bar(ind, y, 1)
    pyplot.xticks(ind + width/2., x)

key_words_hist = count_density_array(result, 0)
# pyplot.bar(key_words_hist[0], key_words_hist[1], 1)
# generate_pyplot_bar(key_words_hist[0],key_words_hist[1])

bibliography_hist = count_density_array(result, 1)
# pyplot.bar(bibliography_hist[0], bibliography_hist[1], 1)
# generate_pyplot_bar(bibliography_hist[0],bibliography_hist[1])

year_hist = count_density_array(result, 2)
# pyplot.bar(year_hist[0], year_hist[1], 1)
# generate_pyplot_bar(year_hist[0],year_hist[1])

count_density_array(result, 1)
true_affiliation = filter_result(result, 3, 1)
false_affiliation = filter_result(result, 3, 0)
true_affiliation_number = len(true_affiliation)
false_affiliation_number = len(false_affiliation)

true_affiliation_density_key_words = count_density_array(true_affiliation, 0)
true_affiliation_density_bibliography = count_density_array(true_affiliation, 1)
true_affiliation_density_year = count_density_array(true_affiliation, 2)

false_affiliation_density_key_words = count_density_array(false_affiliation, 0)
false_affiliation_density_bibliography = count_density_array(false_affiliation, 1)
false_affiliation_density_year = count_density_array(false_affiliation, 2)

table_result = {"key_words": {}, "bibliography": {}, "year": {}, "affiliation": {}}

for class_name in true_affiliation_density_key_words[0]:
    table_result["key_words"][class_name] = {}
    table_result["key_words"][class_name]['true_affiliation_density'] = true_affiliation_density_key_words[1][
        class_name]
    table_result["key_words"][class_name]['false_affiliation_density'] = false_affiliation_density_key_words[1][
        class_name]

for class_name in true_affiliation_density_bibliography[0]:
    table_result["bibliography"][class_name] = {}
    table_result['bibliography'][class_name]['true_affiliation_density'] = true_affiliation_density_bibliography[1][
        class_name]
    table_result['bibliography'][class_name]['false_affiliation_density'] = false_affiliation_density_bibliography[1][
        class_name]

for class_name in true_affiliation_density_year[0]:
    table_result["year"][class_name] = {}
    table_result['year'][class_name]['true_affiliation_density'] = int(true_affiliation_density_year[1][class_name])
    table_result['year'][class_name]['false_affiliation_density'] = int(false_affiliation_density_year[1][class_name])

# table_result['NB']={}
# table_result['Posteriori']={}
all_result_len = len(result)
table_result['affiliation']["P(T)"] = len(true_affiliation) / all_result_len
table_result['affiliation']["P(F)"] = len(false_affiliation) / all_result_len
for category in table_result:
    if category=='affiliation':
        pass
    else:
        for class_name in table_result[category]:
            print(class_name,category)
            print(table_result[category][class_name])
            table_result[category][class_name]['probability_true_affiliation'] = table_result[category][class_name]['true_affiliation_density'] / \
                                                                                 (table_result[category][class_name][
                                                                                      'true_affiliation_density'] +
                                                                                  table_result[category][class_name][
                                                                                      'false_affiliation_density'])
            table_result[category][class_name]['probability_false_affiliation'] = table_result[category][class_name][
                                                                                      'false_affiliation_density'] / \
                                                                                  (table_result[category][class_name][
                                                                                       'true_affiliation_density'] +
                                                                                   table_result[category][class_name][
                                                                                       'false_affiliation_density'])

            table_result[category][class_name]["P(" + str(class_name) + ")"] = (table_result[category][class_name][
                                                                                    'true_affiliation_density'] \
                                                                                + table_result[category][class_name][
                                                                                    'false_affiliation_density']) \
                                                                               / all_result_len
            table_result[category][class_name]["P(" + str(class_name) + "|T)"] = \
                table_result[category][class_name]['true_affiliation_density'] / true_affiliation_number
            table_result[category][class_name]["P(" + str(class_name) + "|F)"] = \
                table_result[category][class_name]['false_affiliation_density'] / false_affiliation_number

# for category in table_result:
#     print(category)
#     for class_name in table_result[category]:
#         print(class_name)
#         table_result[category][class_name]['twierdzenieBayesa'] = (table_result[category][class_name][
#                                                                        'probability_true_affiliation'] * 0.6399) / \
#                                                                   table_result[category][class_name][
#                                                                       'probability_occurence']
#         print(table_result[category][class_name]['twierdzenieBayesa'])
#         print(table_result[category][class_name]['probability_true_affiliation'])
#         print(table_result[category][class_name]['probability_occurence'])
# #
# for class_name in table_result['year']:
#     print(table_result['year'][class_name])
#     print("clas name: ", class_name)
#     print(table_result['year'][class_name])
# def present_all_data_from_table(table_result):
#   for category in table_result:
#         print("Kategoria: %s" % category)
#         if class_name == 'affiliation':
#             pass
#         else:
#             for class_name in table_result[category]:
#                 print(table_result[category][class_name])
#                 print("Nazwa klasy: %s" % class_name)
#                 print("P(" + str(class_name) + "):", table_result[category][class_name]["P(" + str(class_name) + ")"])
#                 print("P(" + str(class_name) + "|T):", table_result[category][class_name]["P(" + str(class_name) + "|T)"])
#                 print("P(" + str(class_name) + "|F):", table_result[category][class_name]["P(" + str(class_name) + "|F)"])
# table_result['year'][class_name]
# posteriori
for category in table_result:
    print("Kategoria: %s" % category)
    for class_name in table_result[category]:
        if category == 'affiliation':
            pass
        else:
            table_result[category][class_name]["P(T|" + str(class_name) + ")"] = \
                (table_result[category][class_name]["P(" + str(class_name) + "|T)"] * table_result['affiliation'][
                    "P(T)"]) \
                / table_result[category][class_name]["P(" + str(class_name) + ")"]
            print("P(T|" + str(class_name) + "): ",table_result[category][class_name]["P(T|" + str(class_name) + ")"])

#
words=[]
bib=[]
year=[]
aff=[]
for i in result:
    words.append(i[0])
    bib.append(i[1])
    year.append(i[2])
    aff.append(i[3])

result=prepare_data()