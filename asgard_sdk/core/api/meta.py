from asgard_sdk.models.config_pb2 import ServerConfig
from asgard_sdk.models.section_pb2 import Section

from asgard_sdk.models.file_pb2 import File
from asgard_sdk.models.game_pb2 import Game
from asgard_sdk.models.tv_pb2 import TVSeries, Episode
from asgard_sdk.models.video_pb2 import Video
from asgard_sdk.models.document_pb2 import Document

from json import loads
from google.protobuf.json_format import MessageToJson, ParseDict

from ..server.database import Database

class MetaAPI(object):
    def __init__(self, config: ServerConfig, connect=False):
        self.__config = config

        self.__database = Database(self.__config)

        if connect:
            self.__database.connect()
    
    # update section

    def create_section(self, section_name: str, path: str, section_type: int, description: str = "", plex_section: str = ""):
        section = Section()

        section.section_name = section_name
        section.section_description = description
        section.section_count = 0
        section.type = section_type # change 

        section.section_path = path

        section.mongo_collection = section_name.strip().lower()
        section.plex_section = plex_section

        ret = MessageToJson(section)
        dict = loads(ret)

        self.__database.insert_doc(dict, "sections", "metadb")

    def get_section(self, section_name: str):
        doc = self.__database.get_doc({"sectionName":section_name}, "sections", "metadb")

        section = ParseDict(doc, Section(), ignore_unknown_fields=True)
        return section

    def get_sections(self):
        ret = []
        for doc in self.__database.list_collection("sections", "metadb"):
            section = ParseDict(doc, Section(), ignore_unknown_fields=True)
            ret.append(section)

        return ret

    def index_section(self, section_name: str):
        section = self.get_section(section_name)
        if section is None:
            return None

        ret = []
        collection = self.__database.list_collection(section.mongo_collection, "metadb")
        for doc in collection:
            file = ParseDict(doc, descriptor_pool=[File, Video, TVSeries, Game, Document], ignore_unknown_fields=True)
            ret.append(file)

        return ret

    def get_file_meta(self, file_sha: str, section_name: str = None):
        ret = None

        if section_name is None:
            sections = self.get_sections()

            for section in sections:
                doc = self.__database.get_doc({"file_sha":file_sha}, section.mongo_collection, "metadb")
                if doc is not None:
                    ret = doc
                    break
        else:
            doc = self.__database.get_doc({"file_sha":file_sha}, section.mongo_collection, "metadb")
            ret = doc
        
        if ret is not None:
            ret = ParseDict(ret, descriptor_pool=[File, Video, TVSeries, Game, Document], ignore_unknown_fields=True)
            
        return ret


    def search(self, query: str, section_name: str = None):
        pass

    def add_file_meta(self, model, section_name: str):
        section = self.get_section(section_name)
        if section is None:
            return False

        ret = MessageToJson(model)
        dict = loads(ret)

        self.__database.insert_doc(dict, section.mongo_collection, "metadb")

        return True