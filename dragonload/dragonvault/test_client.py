#!/usr/bin/env python3

import grpc

# import logger and actors
from dragonload.util.logging import logger
from dragonload.dragonvault.actors import User, Room

# imprort grpc Class files
import dragonvault_pb2
import dragonvault_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub
stub = dragonvault_pb2_grpc.DragonvaultStub(channel)
