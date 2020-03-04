#!/usr/bin/env python3

import sqlite3 as sqlite
import asyncore # NOTE: This needed??
from typing import Union

from dragonload.util.logging import logger
from dragonload.dragonvault.server import Room
from dragonload.dragonvault.server import User

# from dragonload.configs import db_path
db_path = 'dragonvault.sqlite3'

"""
Expectations:
- [ ] Store the user and room into a database
- [ ] Ability to clear the database, the make it atomic
- [ ] Data Integrity
- [ ] DB should handle API calls to return Currently active Rooms
      and the U
for user in Userssers in the room.
- [ ] Mutex lock on Room once downlaoding starts? Lock database? or the code?
- [ ] Setup basic authentication for the users, store the creds in the db
"""


# NOTE: CRAZY sayooj building a wrapper???
# either user @_handleCursor or the combo of (_getConn and _closeConn)
def _handleCursor(func):
    def cursorWrapper(*args, **kwargs):
        db = sqlite.connect(db_path)
        db.row_factory = sqlite.Row
        cursor = db.cursor()
        logger.debug("Setting: db prelude for " + func.__name__)

        # Invoke the function and record optional result here
        result = func(cursor, *args, **kwargs)

        cursor.commit()
        cursor.close()
        db.close()
        logger.debug("Done: db epilogue for " + func.__name__)

        return result
    return cursorWrapper

def _getConnection():
    """
    Database connection prelude
    This function executes the connection and \
    return a cursor object
    Handle the cursor to commit and close properly

    Usag
    cursor, db = _getConnection()
    # User code here
    _closeConnection(cursor, db)

    """
    db = sqlite.connect(db_path)
    db.row_factory = sqlite.Row
    cursor = db.cursor()
    return cursor, db

def _closeConnection(cursor, db):
    """
    Database connection trailer
    commit the connection if not commited.
    Close the cursor and the db
    """
    cursor.commit()
    cursor.close()
    db.close()


def initDB():
    db = sqlite.connect(db_path)
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS rooms (roomID INTEGER NOT NULL UNIQUE, roomName TEXT NOT NULL, \
        creator TEXT references user.userName,  PRIMARY KEY(roomID));"
    )

    # FIXME: The foreign key reference on the roomID from Room table might be wrong in syntax
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userID INTEGER NOT NULL UNIQUE,
            userName TEXT,
            userAuth INTEGER NOT NULL,
            ipAddress TEXT NOT NULL UNIQUE,
            port INT NOT NULL,
            roomID INTEGER references room.roomID,
            PRIMARY KEY(userID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            url TEXT NOT NULL,
            userName TEXT,
            roomID INTEGER NOT NULL,
        )
    """)

    cursor.commit()
    cursor.close()
    db.close()

def deleteDB():
    """
    Delete the database entries, while keeping the table structure intact
    Delete hasbeen implemented for tables
    - rooms
    - users
    - urls
    """
    db = sqlite.connect(db_path)
    db.row_factory = sqlite.Row
    cursor = db.cursor()
    cursor.execute("DELETE from rooms")

    cursor.execute("DELETE from users")

    cursor.execute("DELETE from urls")

    cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()

@_handleCursor
def insertUser(cursor, user: User) -> None:
    """
    Wrapper to insert users
    """

    # TODO: Calculate the values to be inserted
    # user object comes with just the userName, and ipAdderss, and maybe roomID
    # calculate the userID, userAuth
    cursor.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
        (userID, userName, userAuth, ipAdress, port, roomID)
    )

@_handleCursor
def insertRoom(cursor, room: Room) -> None:
    """
    Wrapper to insert room into rooms table
    """

    # TODO: Calculate the values. room object may not contain the creator
    # or maybe remove that feature
    cursor.execute(
        "INSERT INTO rooms VALUES (?, ?, ?)",
        (roomID, roomName, creator)
    )

@_handleCursor
def insertUrl(cursor, url: str, user: User, room: Room) -> None:
    """
    Wrapper to insert URL to url table
    """
    cursor.execute(
        "INSERT INTO urls VALUES (?, ?, ?)",
        (url, user.userName, room. roomID)

    )

@_handleCursor
def updateUserRoom(cursor, user: User, room: Room):
    """
    Wrapper to update user room
    """
    cursor.execute(
        "UPDATE user SET " # fille the remaining
    )

@_handleCursor
def updateRoom(cursor, room: Room):
    pass
