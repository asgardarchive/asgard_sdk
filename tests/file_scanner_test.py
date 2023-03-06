from unittest import TestCase, main

from core.api.file_scanner import FileScanner
from models.proto.config_pb2 import Config

class FileScannerTest(TestCase):

    def setUp(self):
        self.config = Config()

        self.config.mongo_ip = "192.168.1.221"
        self.config.mongo_port = 27017

        self.scanner = FileScanner(self.config, connect=True)

    def test_file_assocations(self):
        print(self.scanner.get_file_association("VIDEO"))

    def test_file_scan(self):
        print(self.scanner.scan_file(""))

    def test_folder_scan(self):
        self.scanner.scan_folder("")

if __name__ == "__main__":
    main()
