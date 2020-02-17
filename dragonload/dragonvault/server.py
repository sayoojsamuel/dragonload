#!/usr/bin/env python3

from copy import deepcopy
from dragonload.util.logging import logger


class User:

    # Do we require user state?
    # register log time

    def __init__(self, ip_addr=None, userName=None):
        if userName == None:
            userName = "- anonymous -"
        self.userName = userName
        self.room = None
        self.ip_addr = ip_addr


    def __repr__(self):
        name = "\tUser Name: %s,\n" %(self.userName)
        room = "\tRoom Enrolled: %s,\n" %(self.room)

        return "User(\n" \
            + name \
            + room \
            + "\n)"


    def getName(self):
        """ Returns the Username """
        return userName


    def updateName(self, newName):
        self.userName = newName


    def currentRoom(self):
        return self.room


    def joinRoom(self, roomObject):
        """ Join the specified Room.

        Arguments:
        roomObject: object of class Room

        Return:
        None <- Unsuccessful
        roomObject<- Successfull
        """
        if not isinstance(roomObject, Room):
            # Format string %s is error; FIXME later
            logger.error(
                "User %s cannot join Room: %s is not a valid Room object" % (self.userName, roomObject)
            )
            return None
        self.room = roomObject
        logger.info(
            "User %s joined room %s" %(self.userName, roomObject.roomName)
        )
        return self.room


    # FIX: Debug a 1000 times. This might not be a good implementation
    # The state of the room may vary
    def leaveRoom(self, roomObject: Room) -> bool:
        """ Leave the specified room.

        Arguments:
        roomObject: object of class Room

        Return:
        True <- Successfully exited Room roomObject
        False <- Unable to leave the Room roomObject
        """
        if self.room == roomObject:
            self.room = None
            logger.info(
                "User %s exited room %s" %(self.userName, roomObject.roomName)
            )
            return True

        logger.error(
            "User %s unable to exit room %s" %(self.userName, roomObject.roomName)
        )
        return False


class Room:

    OFFLINE = 1
    ONLINE = 2
    IN_SPLITFIRE = 3
    IN_CHAINRAIN = 4

    statusCodes = {
        OFFLINE: "Room Offline",
        ONLINE: "Room Online, active",
        IN_SPLITFIRE: "Splitfire Protocol in progress",
        IN_CHAINRAIN: "Chainrain Protocol in progress"
    }

    def __init__(self, roomName):
        self.roomName = roomName
        self.activeUserCount = 0
        self.activeUsers = list()
        self.status = Room.ONLINE
        self.status_message = Room.statusCodes[self.status]


    # FIX: Not usefull and cannot trust the garbage collector
    def __del__(self):
        """Release all the users, and kill the room

        Currently not clearing the Room.activeUsers (just deleting object clears the air)
        """
        for user in self.activeUsers:
            user.leaveRoom(self)

        logger.info(
            "Successfully deleted room %s" % self.roomName
        )


    def __repr__(self):
        name = "\tRoomName: %s,\n" %(self.roomName)
        status = "\tRoom Status: %s,\n" %(self.status_message)
        userCount = "\tUser Count: %d,\n" %(self.activeUserCount)
        users = "\tUsers in Room\n\t\t" + "\n\t\t".join(self.getActiveUsers())

        return "Room(\n" \
            + name \
            + status \
            + userCount \
            + users \
            + "\n)"


    def __str__(self):
        return "Room(name: %s)" %(self.roomName)
       

    def changeStatus(self, statusCode):
        """Change the status of the Room to statusCode

        Returns:
           True <- if successfull
           False <- if unsuccessfull
        """
        backup_status = self.status
        try:
            self.status = statusCode
            self.status_message = Room.statusCodes[self.status]
            logger.info("Room %s switched to status: %s " %(self.roomName, self.status))
        except Exception as err:
            logger.error(
                "Error changing room %s status from %s to %s ;; %s"\
                %(self.roomName, backup_status, statusCode, err)
            )
            self.status = backup_status
            self.status_message = Room.statusCodes[self.status]
            return False
        return True


    def addUser(self, user):
        """Adds a user to the Room. Also updates the User.room
       
        Returns:
            True <- If task successfull
            Fasle <- if unable to add user
        """
        if user.currentRoom() != None:
            logger.error(
                "User %s is already in room %s" %(user.userName, user.room)
            )
            return False

        back_self_user = self.activeUsers[:]
        back_self_count = self.activeUserCount

        try:
            self.activeUsers.append(user)
            self.activeUserCount += 1
            back_room = user.joinRoom(self)
        except Exception as err:
            logger.error(
                "Error adding user %s to room %s" % (user.userName, self.roomName)
            )
            self.activeUsers = back_self_user
            self.activeUserCount = back_self_count
            return False

        return True


    def removeUser(self, user):
        """Remove user from the Room. Also update the User.room

        Returns:
            True <- If task successfull
            Fasle <- if unable to add user
        """
        if user not in self.activeUsers:
            logger.error(
                "Unable to remove user %s; user not in room %s"\
                %(user.userName, self.roomName)
            )
            return False

        back_self_user = self.activeUsers[:]
        back_self_count = self.activeUserCount
        try:
            self.activeUsers.remove(user)
            self.activeUserCount -=1
            user.leaveRoom(self) # returns bool value
        except Exception as err:
            logger.error(
                "Unable to remove user %s; %s"\
                %(user.userName, err)
            )
            self.activeUsers = back_self_user
            self.activeUserCount = back_self_count
            return False

        return True


    def getActiveUsers(self):
        """Returns the list of active users in the Room"""
        if self.activeUserCount == 0:
            logger.info("Empty room %s" % self.roomName)
            return list()
       
        userList = list()
        for user in self.activeUsers:
            userList.append(user.userName)

        return userList


    # delete all users in the active users list
    # FATAL: FIXME: FIXME: This cannot be a classmethod - were you sleeping while coding???
    # Change it to static method and pass the object room.
    @classmethod
    def terminateRoom(cls):
        """Force quit the users from the room

        Return: (status <bool>, remaining users <int>)
            (True, 0) if no users in the room
            (True, count) if room is deleted, and count users are still left
            (False, count) if room is not deleted
        """
        if cls.activeUserCount == 0:
            logger.info('Successfully deleted room %s' %(cls.roomName))
            return True, cls.activeUserCount

        # Handle active users
        for user in cls.activeUsers:
            user.leaveRoom(cls)
            cls.activeUserCount -= 1

        remainingUsers = cls.activeUserCount
        del cls  # Delete the class
        return True, remainingUsers


def Test():
    from IPython import embed
    u1 = User()
    u2 = User()
    u3 = User('sayooj')
    u4 = User('samuel')

    r1 = Room('Download-1')
    # test changeStatus()
    r1.changeStatus(Room.OFFLINE)
    r1.changeStatus(Room.ONLINE)

    # test addUser()
    r1.addUser(u3)
