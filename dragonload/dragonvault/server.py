#!/usr/bin/env python3

import grpc
from concurrent import futures
import time

# import logger and actors
from dragonload.util.logging import logger
from dragonload.dragonvault.actors import User, Room

# imprort grpc Class files
import dragonvault_pb2
import dragonvault_pb2_grpc

# import utilities, encode, decode functions
from dragonload.dragonvault.util import (
    encodeUser,
    decodeUser,
    encodeRoom,
    decodeRoom
)

# create the global User List, Room List
userList = []
roomList = []


# Class to define server functions, derived from the
# dragonvault_pb2.grpc.DragonvaultServicer
class DragonvaultServicer(dragonvault_pb2_grpc.DragonvaultServicer):

    """
    Perform the functions here;
    Just the wrappers for the functions that needs to be performed;
    Actuals functions defined miles away
    """

    def LogUser(self, request, context):
        user = decodeUser(request)
        # NOTE: Fix me in next iteration.  add me to database instead.
        userList.append(user)
        logger.info("User Added- {} : {}".format(user.userName, user.ip_addr))
        return dragonvault_pb2.Ack(status=True, msg="User logged successfully")
   

    def ListRooms(self, request: dragonvault_pb2.Empty, context) -> dragonvault_pb2.Room:
        for room in roomList:
            room = encodeRoom(room)
            yield room

    def JoinRoom(self, request: dragonvault_pb2.UserRoom, context):
        user = decodeUser(request.user)
        room = decodeRoom(request.room)

        # Check validity
        _live_room = None
        for _room in roomList:
            if _room.roomName == room.roomName:
                # room Exist inside roomList
                _live_room = _room
                break

        if not _live_room:
            # Room does not exist, reply with apt Ack
            return dragonvault_pb2.Ack(status=False, msg="Invalid Room! Do you want to create a new room?")

        status = Room.addUser(_live_room, user)
        if not status:
            # unable to add user
            msg = "Unable to add user to the Room"
        else:
            msg = "User added successfully to Room -" + room.roomName

        return dragonvault_pb2.Ack(status = status, msg=msg)
   
    def CreateRoom(self, request, context):
        room = decodeRoom(request)

        # Check conflicting names
        for _room in roomList:
            if _room.roomName == room.roomName:
                # Room already exist
                return dragonvault_pb2.Ack(status=False, msg="Another room with name '{}' already exist".format(room.roomName))

        # Create a new room
        roomList.append(room)
        logger.info("Room Created- {} ".format(room.roomName))
        return dragonvault_pb2.Ack(status = True, msg="Room created Successfully")
    

    def InfoRoom(self, request, context):
        room = decodeRoom(request)

        # search in roomList, default None Room
        _live_room = dragonvault_pb2.Room('')
        for _room in roomList:
            if _room.roomName == room.roomName:
                _live_room = _room
                break
            
        return _live_room

    def SubmitUrl(self, request, context):
        pass

    def StartDownload(self, request, context):
        pass

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# Add DragonvaultServicer to function
dragonvault_pb2_grpc.add_DragonvaultServicer_to_server(
    DragonvaultServicer(),
    server
)

logger.info("Starting dragonvault server, Listening on port 50051...")
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
    logger.info("Dragonvault terminated. Please restart the server manually")
