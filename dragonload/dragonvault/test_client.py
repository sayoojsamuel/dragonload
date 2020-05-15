#!/usr/bin/env python3

import grpc

# import logger and actors
from dragonload.util.logging import logger
from dragonload.dragonvault.actors import User, Room

# imprort grpc Class files
import dragonvault_pb2
import dragonvault_pb2_grpc

# import utils
from dragonload.dragonvault.util import *

# open a gRPC channel
#channel = grpc.insecure_channel('localhost:50051')
channel = grpc.insecure_channel('104.215.197.138:50051')

# create a stub
stub = dragonvault_pb2_grpc.DragonvaultStub(channel)


null = dragonvault_pb2.Empty()

# Create Room
r1 = Room('Download1')
rr1 = encodeRoom(r1)

print(stub.CreateRoom(rr1))

# List Rooms
print("List Rooms")
for r in stub.ListRooms(null):
    print(decodeRoom(r))

# Add User to Room
u1 = User('192.159.1.2', 'sayooj')
uu1 = encodeUser(u1)

ur = dragonvault_pb2.UserRoom()
ur.user.MergeFrom(uu1)
ur.room.MergeFrom(rr1)

print(stub.JoinRoom(ur))
