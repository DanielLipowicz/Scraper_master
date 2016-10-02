import operator
from src.data_visualisation import pyplot_usage as plot
from src.DataOperation import select_operations
from src.databases import mongo_operations


def data_visualisation(keywords_to_visualisation):
    data_to_process = []
    keywords_data = []

    for i in range(len(keywords_to_visualisation)):
        data_to_process.append(key_word(keywords_to_visualisation[i]))
    for each in data_to_process:
        each.related_keywords = mongo_operations.get_data_about_keyword(each.keyword)

    row_data_to_plot = merge_two_related_keyword_dictionary(data_to_process[0], data_to_process[1])
    filtered_data_to_plot = filter_data_list_by_density(row_data_to_plot, 3)

    plot.plot_two_keyword_data_list(filtered_data_to_plot, keywords_to_visualisation[0], keywords_to_visualisation[1])


class key_word:
    def __init__(self, keyword):
        self.keyword = keyword
        #  dictionary:
        #  {keyword: quantity_of_related_keywords}
        self.related_keywords = {}
        print('Created object: ', self.keyword)


def merge_dictionaries(dictionaries):
    merged = []
    for dictionary in dictionaries:
        for keyword in dictionary:
            if keyword not in merged:
                merged.append(keyword)
    return merged


def merge_two_related_keyword_dictionary(dictionary1, dictionary2):
    dictionary1_keys = dictionary1.related_keywords
    dictionary2_keys = dictionary2.related_keywords
    keywords_to_search = merge_dictionaries([dictionary1_keys, dictionary2_keys])
    merged_list = []
    merged_list_tmp = []
    i = 1
    for each in keywords_to_search:
        dict1_counted = dictionary1_keys.get(each)
        dict2_counted = dictionary2_keys.get(each)

        if dict1_counted is None:
            dict1_counted = 0
        if dict2_counted is None:
            dict2_counted = 0
        dicts_differential = dict1_counted-dict2_counted

        merged_list_tmp.append([i, dict1_counted, dict2_counted, each, dicts_differential])
    merged_list_tmp = sorted(merged_list_tmp, key=operator.itemgetter(4))

    for each in merged_list_tmp:
        merged_list.append([i, each[1], each[2], each[3]])
        i += 1
    merged_list.insert(0, ['no', 'dictionary1', 'dictionary2', 'keyword'])
    return merged_list


def filter_data_list_by_density(data_list, density):
    filtered_list = []
    for each in data_list[1:]:
        if each[1] >= density or each[2] >= density:
            filtered_list.append(each)
    i = 1
    for each in filtered_list:
        each[0] = i
        i += 1
    return filtered_list



















