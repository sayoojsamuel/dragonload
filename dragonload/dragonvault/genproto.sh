#!/usr/bin/env bash

echo -n "Generating Protobuf files..."
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/dragonvault.proto

