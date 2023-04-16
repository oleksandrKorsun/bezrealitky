import certifi
import pymongo

class DbHelper():

    def __init__(self, db_name, collection_name):
        self.client = pymongo.MongoClient(
            "mongodb+srv://bersh:testtest@cluster0.jvr3k.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
        self.db = self.client[db_name][collection_name]

    def insert_many(self, list_of_objects):
        self.db.insert_many(list_of_objects)  # insert all values to db

    def insert_one(self, element):
        self.db.insert_one(element)  # insert one value to db

    def update_value_in_db(self, myquery, newvalues):
        # myquery_example = {"id": "840"}
        # newvalues_example = {"$set": {"price": "aaaaa"}}
        self.db.update_one(myquery, newvalues)  # updates value

    def check_value_in_db(self, element_for_check):
        # element_for_check_example = {"id": "99"}
        return self.db.count_documents(element_for_check)  # check if value in db

    def close_connection(self):
        self.client.close()