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

# create the global User List, Room List
userList = []
roomList = []

# Encode/Decode functions
"""
Functions designed to translate betwenn grpc class and actor classes
Encode(actor_class) -> grpc_class
Decode(grpc_class) -> actor_class
"""
def encodeUser(user: User) -> dragonvault_pb2.User:
    encoded_user = dragonvault_pb2.User()
    encoded_user.userName = user.userName
    encoded_user.ip_addr = user.ip_addr
    if user.room != None:
        encoded_user.room = encodeRoom(user.room)
    return encoded_user

def decodeUser(user: dragonvault_pb2.User) -> User:
    decoded_user = User(user.userName, user.ip_addr)
    if user.HasField('room'):
        decoded_user.room = decodeRoom(user.room)
    return decoded_user

def encodeRoom(room: Room) -> dragonvault_pb2.Room:
    encoded_room = dragonvault_pb2.Room()
    encoded_room.roomName = room.roomName
    encoded_room.activeUserCount = room.activeUserCount
    if room.activeUsers != list():
        encoded_room.activeUsers = list(map(encodeUser, room.activeUsers))
    encoded_room.status = room.status
    encoded_room.status_message = room.status_message
    return encoded_room

def decodeRoom(room: dragonvault_pb2.Room) -> Room:
    decoded_room = Room(room.roomName)
    if room.HasField('activeUserCount'):
        decoded_room.activeUserCount = room.activeUserCount
    if room.HasField('activeUsers'):
        decoded_room.activeUsers = list(map(decodeUser, room.activeUsers))
    if room.HasField('status'):
        decoded_room.status = room.status
    if room.HasField('status_message'):
        decoded_room.status_message = room.status_message
    return decoded_room

   


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

        if not eflag:
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
