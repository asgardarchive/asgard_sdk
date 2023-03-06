FROM ubuntu:latest

LABEL name="asgard-sdk"
LABEL description="Software Development Kit for interacting with asgard"

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install apt-utils python3 python3-pip git protobuf-compiler -y

RUN git clone https://github.com/asgardarchive/asgard-sdk.git /sdk
WORKDIR /sdk

RUN pip3 install -r requirements.txt 
RUN pip3 install -e .