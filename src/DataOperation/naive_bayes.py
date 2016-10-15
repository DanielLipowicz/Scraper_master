from src.databases import mongo_operations
from matplotlib import pyplot
class naive_bayes:
    mongo_connection = mongo_operations.get_new_connection_to_database()
    collection = mongo_connection.collection


    def density(field_in_database, value_of_field):
        print (collection.find({field_in_database: value_of_field}).count())

    density("key_words","Big Data")



    def draw_density_plot(list_of_list_to_count, element_no=0):
        key_words_list=[]
        for i in list_of_list_to_count:
            key_words_list.append(i[element_no])
        x_dic = set(key_words_list)
        x = []
        y = []
        for i in x_dic:
            y.append(key_words_list.count(i))
        for i in range(len(y)):
            x.append(i)
        print(y)
        print(x)
        pyplot.scatter(y,x)
        return key_words_list.sort()

    def prepare_data():
        result = []
        def get_data_from_found_record(record):
            key_words_related = len(i.get("key_words"))
            print(key_words_related)
            affiliations = i.get("affiliations")
            bibliography_count = len (i.get("bibliography"))
            year = i.get("year")
            is_university= 0
            for affiliation in affiliations:
                if affiliation!='undefined':
                   is_university = 1
                   print (affiliation)

            # table KW, BIBLIO, ROK, UCZELNIA
            result.append([key_words_related,bibliography_count,year,is_university])

        for i in collection.find({"key_words":"Big Data"}):
            get_data_from_found_record(i)
        for i in collection.find({"key_words":"Hurtownie danych"}):
            get_data_from_found_record(i)
        for i in result:
            print(i)
        return result


def clasify(result):
    for i in result:
        if (i[0]<3):
            i[0]=1
        if (i[0]>=3 and i[0]<5):
            i[0]=2
        if (i[0]>=5):
            i[0]=3
    for i in result:
        print (i)


