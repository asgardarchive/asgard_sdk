from sys import exit

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from asgard_sdk.models.config_pb2 import ServerConfig

from json import loads
from bson.json_util import dumps
from bson import ObjectId

"""

    Abstraction of a mongoDB database

"""
class Database(object):
    def __init__(self, config: ServerConfig):
        self.__config = config
        self.__client = None

        self.db_info = None 
        self.meta_db = None
        self.analytics_db = None
        self.post_db = None
        self.logs_db = None

        self.ip_address = self.__config.mongo_ip
        self.port = self.__config.mongo_port

    def get_config(self):
        return self.__config

    def connect(self):
        config = self.get_config()
        try:
            client = MongoClient(config.mongo_ip, config.mongo_port, username="odin", password="Bore@sFurY0336")
            self.db_info = client.server_info()

            self.__client = client
        except ConnectionFailure or ServerSelectionTimeoutError:
            print("[sdk] Failed to connect to mongoDB: {i}:{p}".format(i=config.mongo_ip, p=config.mongo_port))
            exit(1)

        self.meta_db = self.get_database("metadb")
        self.analytics_db = self.get_database("analyticsdb")
        self.post_db = self.get_database("postdb")
        self.logs_db = self.get_database("logsdb")

    def pymongo_to_dict(self, doc: dict):
        return loads(dumps(doc, default=str))

    def get_database(self, database_name: str):
        database = self.__client[database_name]

        return database

    def get_collection(self, collection_name: str, database_name: str):
        database = self.get_database(database_name)

        return database[collection_name]

    def list_collection(self, collection_name: str, database_name: str, limit: int = None) -> list:
        collection = self.get_collection(collection_name, database_name)

        ret = []

        results = collection.find({})

        if limit:
            results = results.limit(limit)
        
        for item in results:
            ret.append(self.pymongo_to_dict(item))

        return ret

    def get_doc(self, doc_query: dict, collection_name: str, database_name: str):
        collection = self.get_collection(collection_name, database_name)

        doc = collection.find_one(doc_query)
        ret = self.pymongo_to_dict(doc)

        return ret

    def insert_doc(self, doc: dict, collection_name: str, database_name: str):
        collection = self.get_collection(collection_name, database_name)

        insert_id = collection.insert_one(doc).inserted_id

        return insert_id

    def remove_doc(self, doc_query: dict, collection_name: str, database_name: str):
        collection = self.get_collection(collection_name, database_name)

        collection.delete_one(doc_query)