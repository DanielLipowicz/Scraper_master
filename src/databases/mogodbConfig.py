import pymongo

client = pymongo.MongoClient()
client = pymongo.MongoClient('92.222.68.207', 27017)


class mongoConnection:
    def __init__(self, database='test', collection='scrap3'):
        self.db = client[database]
        self.collection = self.db[collection]
        self.connection_test()

    @staticmethod
    def connection_test():
        try:
            client.server_info()
            print(client.database_names())
        except pymongo.errors.ServerSelectionTimeoutError:
            print(err)

    def insert_one_object(self, objectJSON):
        post_id = self.collection.insert_one(objectJSON).inserted_id
        return post_id

    def insert_one_if_doesnt_exist(self, objectJSON):
        query = self.collection.find_one(objectJSON)

        if query is None:
            post_id = self.collection.insert_one(objectJSON).inserted_id
            return post_id
        else:
            print("record already exist")
            return "record already exist"

    def find_in_collection(self, find={}):
        for i in self.collection.find(find):
            print(i)
