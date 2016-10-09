from src.DataOperation import scraping_data_operations
from src.DataOperation import key_words_data_procesing as data_processing


keywords = ["Analiza danych", "Statystyka", "Systemy business Intelligence", "Analiza danych", "technologia","Przetwarzanie danych", "informacja w internecie", "internet", "chmura obliczeniowa","data mining"]
# ------------------------------------------
# scraping update data to MongoDb database
# to configure MongoDB database go to src/databases/mongodbConfig.py
# without that application could not work
# ------------------------------------------
scraping_data_operations.scrap_data(keywords)

# data processing and visualisation
# should to define another keywords set which may to compare
keywords = ["Big Data", "Hurtownie danych"]

data_processing.data_visualisation(keywords)

print('end')

