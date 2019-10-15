import pymongo

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    COLLECTION = "sensor_data"

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI) 
        Database.DATABASE = client["dature"]

    @staticmethod
    def insert(data):
        Database.DATABASE[Database.COLLECTION].insert(data)

    @staticmethod
    def find(query):
        return Database.DATABASE[Database.COLLECTION].find(query,{"_id":0})

    @staticmethod
    def find_one(query):
        return Database.DATABASE[Database.COLLECTION].find_one(query)

