from os import getenv, stat
from os.path import exists, isfile, extsep

from ...models.proto.config_pb2 import ServerConfig
from ...models.proto.file_association_pb2 import FileAssociation

from ...models.proto.file_pb2 import File
from ...models.proto.game_pb2 import Game
from ...models.proto.tv_pb2 import TVSeries, Episode
from ...models.proto.video_pb2 import Video
from ...models.proto.document_pb2 import Document

from json import loads
from google.protobuf.json_format import MessageToJson, ParseDict

from pymediainfo import MediaInfo
from ebooklib.epub import EpubReader
from PyPDF2 import PdfReader

from ..server.database import Database

class FileScanner(object):
    def __init__(self, config: ServerConfig, connect=True):
        self.__config = config

        self.__database = Database(self.__config)

        # cached file associations

        if connect:
            self.__database.connect()

    def get_file_associations(self):
        ret = []
        docs = self.__database.list_collection("file_associations", "metadb")
        for doc in docs:
            association = ParseDict(doc, FileAssociation(), ignore_unknown_fields=True)
            ret.append(association)

        return ret

    def get_file_association(self, type: str):
        ret = None
        for association in self.get_file_associations():
            if association.type == type:
                ret = association
                break

        return ret

    def get_association_from_ext(self, file_ext: str):
        ret = None
        for association in self.get_file_associations():
            if file_ext in association.extensions:
                ret = association
                break

        return ret

    def validate_path(self, file_path: str):
        if file_path.startswith("~") is True:
            file_path = file_path.replace("~", getenv("HOME"))
        
        if exists(file_path) is False:
            return False

        if isfile(file_path) is False:
            return False

    def scan_file(self, file_path: str, ign: list = None):
        validate = self.validate_path(file_path)
        if validate is False:
            return None

        file_ext = file_path.split(extsep)[-1]
        association = self.get_association_from_ext(file_ext)
        if association is None:
            print("File ext not recognized by asgard")
            return None # file not recognized by asgard

        file = File()
        
        file_stat = stat(file_path)
        fp_split = file_path.split("/")
        file_name = fp_split[-1]
        
        file.file_name = file_name
        file.file_location = None
        file.file_size = file_stat.st_size

        if association.type == "VIDEO": # regen proto models
            meta = self.fetch_video_meta(file_path)
            file.asgard_type = 1
        elif association.type == "DOCUMENT":
            meta = self.fetch_document_meta(file_path)
            file.asgard_type = 4
        elif association.type == "GAME":
            meta = self.fetch_game_meta(file_path)
            file.asgard_type = 2
        
        meta.file = file

        return meta
            
    def scan_folder(self, folder_path: str, ign: list = None):
        pass
    
    def fetch_video_meta(self, file_path: str):
        media_info = MediaInfo.parse(file_path)
        
        video = Video()
        for track in media_info.tracks:
            if track.track_type == "General":
                video.duration = track.duration
            
            if track.track_type == "Video":
                video.container = track.container
                video.encoder = track.encoding_library
                video.width = track.width
                video.height = track.height

        return video

    def fetch_game_meta(self, file_path: str, file_ext: str):
        game = Game()

        game.console = file_ext

    def fetch_document_meta(self, file_path: str):
        pass