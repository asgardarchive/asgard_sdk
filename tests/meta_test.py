from unittest import TestCase, main

from core.api.meta import MetaAPI

from models.proto.config_pb2 import Config

class MetaAPITest(TestCase):

    def setUp(self):
        self.config = Config()

        self.config.mongo_ip = "192.168.1.221"
        self.config.mongo_port = 27017

        self.meta = MetaAPI(self.config, connect=True)

    # def test_create_section(self):
    #     self.meta.create_section("Movies", "/mnt/volume1/media/movies", 0, plex_section="Movies")

    def test_get_sections(self):
        print(self.meta.get_section("Movies"))
        print(self.meta.get_sections())

    def test_index_sections(self):
        print(self.meta.index_section("Movies"))
if __name__ == "__main__":
    main()