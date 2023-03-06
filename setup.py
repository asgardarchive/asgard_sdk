from setuptools import setup
from distutils.cmd import Command
from distutils.log import INFO
from subprocess import check_call

# class BuildProtobuf(Command):
    
#     description = "Build protobuf models and convert them to python files"

#     def run(self):
#         command = ["protoc", "--python_out models/", "proto/*.proto"]
#         self.announce("Building protobuf models", level=INFO)
#         check_call(command)

setup(
    name="asgard_sdk",
    version="1.0",
    url="https://github.com/asgardarchive/asgard-sdk.git",
    author="stevezaluk",
    description="SDK for interacting with Asgard"
    )
