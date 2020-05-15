#!/usr/bin/env python3

import socket
from dragonload.util.logging import logger

# import Actors, grpc classes
from dragonload.dragonvault.actors import User, Room
import dragonvault_pb2


def get_host_details():
    """Returns the hostname and IP address of the node
    """
    hostName = ""
    ip_addr = ""
    try:
        hostName = socket.gethostname()
        ip_addr = socket.gethostbyname(hostName)
    except Exception as err:
        logger.error("Unable to obtain Host Details: %s" % err)

    return hostName, ip_addr


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
    # Change the activeUsers
    if user.room != None:
        encoded_user.room.MergeFrom(encodeRoom(user.room, strip = True))
    return encoded_user

def decodeUser(user: dragonvault_pb2.User) -> User:
    decoded_user = User(user.ip_addr, user.userName)
    if user.HasField('room'):
        decoded_user.room = decodeRoom(user.room)
    return decoded_user

def encodeRoom(room: Room, strip = False) -> dragonvault_pb2.Room:
    encoded_room = dragonvault_pb2.Room()
    encoded_room.roomName = room.roomName
    encoded_room.activeUserCount = room.activeUserCount
    if room.activeUsers != list() and not strip:
        #encoded_room.activeUsers = list(map(encodeUser, room.activeUsers))
        encoded_room.activeUsers.MergeFrom(list(map(encodeUser, room.activeUsers)))
    encoded_room.status = room.status
    encoded_room.status_message = room.status_message
    return encoded_room

def decodeRoom(room: dragonvault_pb2.Room) -> Room:
    decoded_room = Room(room.roomName)
    decoded_room.activeUserCount = room.activeUserCount
    decoded_room.activeUsers = list(map(decodeUser, room.activeUsers))
    decoded_room.status = room.status
    decoded_room.status_message = room.status_message
    return decoded_room
