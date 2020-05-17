#!/usr/bin/env python3

import os.path
import shutil # this instead of mmap
import time
import requests
from tqdm import *
from subprocess import Popen, PIPE
from dragonload.util.logging import logger
from dragonload.chainrain.util import get_host_details

"""
program should handle sharing files!!!
- [x] get ip addresses  - [completed! available as util function from util.py]
- [-] spawn the server
- ** share only relavant files
- ** get required files.
- ** needs to keep the files in a unique directory!!!
- [x] merge the parts into one downloaded file - completed
- check for curruptions and handle errors
- ** design the protocol for efficient transfer
- handle dishonest parties - call splitFire again to hadle missing parts
- ??
"""


# Download Path
# Fix: expanduser vs os.environ and get home address for ~
HOME = os.path.expanduser('~/Downloads/Dragonload/')


def checkFilesExist(fileName: str) -> bool:
    """ Returns True if the file exist """
    if os.path.exists(fileName):
        return True

    return False


def getIPAddress():
    hostName, ip_addr = get_host_details()

    return ip_addr


# NOTE: This is robust, but address reuse issue is bothering.
# Refactor the code to use non-blocking threads in future.
class FileServerHandler:
    """
    File Server Handler, using subprocess calls
    Usage:
        FileServerHandler.start() # To start the server
        FileServerHandler.stop() # To stop the server
    """

    fileServer = None

    # was startFileServer
    @classmethod
    def start(cls):
        """ Start the File Server """
        # python = python3 FIXME: Decide universally
        cls.fileServer = Popen(['python3','httpServer.py'], stdout=PIPE, stderr=PIPE)
        logger.info("Initiating local file server at %s" % (HOME))

    @classmethod
    def stop(cls):
        """ Stop the File Server """
        cls.fileServer.kill()
        logger.info("Terminated local file server at %s" % (HOME))


def getPart(filename: str, partNumber: int, hostIP: str) -> (bool, str):

   hostPort = 11112 #NOTE: fixed port for all #None # ?? from config file
   partitionFilename = filename + ".part" + (str(partNumber).rjust(3, '0'))

   url = "http://" + ":".join([hostIP, str(hostPort)]) + "/" + partitionFilename
   try:
       r = requests.get(url, stream = True)
       r.raise_for_status()
   except requests.exceptions.HTTPError as err:
       logger.fatal(err)
       return (False, None)

   logger.info("Getting part %s from user %s" % (partitionFilename, hostIP))
   fileSegmentSize = int(r.headers.get('Content-Length'))
   chunkSize = 1024
   with open(os.path.join(HOME, partitionFilename), "wb") as fp:
       pbar = tqdm(unit = "B", total = fileSegmentSize)
       for chunk in r.iter_content(chunk_size = chunkSize):
           if chunk: # filter-out keep-alive chunks
               pbar.update(len(chunk))
               fp.write(chunk)
   logger.info("Downloading complete for %s from %s" % (partitionFilename, hostIP))
   return (True, partitionFilename)




# TODO: Test mergePartitions
def mergePartitions(filename: str, total_partitions: int) -> (bool, str):

    CHUNK_SIZE = 1024 * 1024
    # make sure that all the parts exists
    fileExistStatus = True
    for part in range(total_partitions):
        partitionFilename = os.path.join(HOME, filename) + ".part" + (str(part).rjust(3, '0'))
        fileExistStatus = fileExistStatus and checkFilesExist(partitionFilename)

    if not fileExistStatus:
        logger.critical("Not all parts available in the directory: Initiating Chainrain again")
        return False, None

    """ Merger all the partitions together into one output file """
    outputFile = open(os.path.join(HOME, filename),'ab')

    for part in range(total_partitions):
        partitionFilename = os.path.join(HOME, filename) + ".part" + (str(part).rjust(3, '0'))
        with open(partitionFilename, 'rb') as inputFile:
            # Think why you scraped the idea of mmap
            #shutil.copyfileobj(inputFile, outputFile, CHUNK_SIZE * 10)
            while True:
                inputBuffer = inputFile.read(CHUNK_SIZE * 10)
                if not inputBuffer:
                    break
                outputFile.write(inputBuffer)
        logger.info("Completed merging part %d of %d" % (part, total_partitions))

    outputFile.close()
    logger.info("Complted merge procedure")

    assert checkFilesExist(os.path.join(HOME, filename))

    return True, filename


def transferManager(filename: str, user_count: int, user_id: int, user_list):
    """
    Handle the proto

    user_list contains user_id, ip_address
    """

    assert(user_count == len(user_list)), "Users do not Match"


    ## Initiate local fileserver
    ## FIXME: Initiate long before server start?
    #fs = FileServerHandler()
    #fs.start() # non blocking

    time.sleep(6) # waiting for other user to complete the download
    
    ## see to the sharing part
    for other_id, other_ip_address in user_list:
        if other_id == user_id:
            # Self user, continue
            continue

        # blocking wait for other_user to start the server
        checkInactiveUsers(other_ip_address, filename, other_id)


        # FIXME: calculate part number instead of this dirty trick
        status, _ = getPart(filename, other_id, other_ip_address)
       


    ## Call merge parts
    status, _filename = mergePartitions(filename, user_count)

    pass

def checkInactiveUsers(ip_addr, filename, partNumber):

    partitionFilename = filename + ".part" + (str(partNumber).rjust(3, '0'))
    while True:
        try:
            if requests.head('http://' + ip_addr + ":11112/"+partitionFilename).status_code == 200:
                return True
                break
        except:
            time.sleep(1)
            logger.info("Waiting for user at ip: "+ip_addr)
    return True
