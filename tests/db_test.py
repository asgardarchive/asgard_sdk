import unittest

from core.server.database import Database
from models.proto.config_pb2 import Config

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.config = Config()

        self.config.mongo_ip = "192.168.1.221"
        self.config.mongo_port = 27017

        self.db = Database(self.config)

    def test_config(self):
        self.assertEqual(self.config.mongo_ip, "192.168.1.221")
        self.assertEqual(self.config.mongo_port, 27017)

    def test_list(self):
        self.db.connect()
        coll = self.db.list_collection("sections", "metadb")
        print(coll)

    def test_ins(self):
        self.db.connect()

        doc = {"new_test":"new_test"}
        self.db.insert_doc(doc, "sections", "metadb")
        print(self.db.list_collection("sections", "metadb"))

    def test_rm(self):
        self.db.connect()
        doc = {"new_test":"new_test"}
        self.db.remove_doc(doc, "sections", "metadb")

    def test_get(self):
        self.db.connect()

        print(self.db.get_doc({"test":"test"}, "sections", "metadb"))


if __name__ == "__main__":
    unittest.main()