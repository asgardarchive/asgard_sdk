#!/bin/bash

protoc -I proto/ --python_out asgard_sdk/models proto/*.proto
