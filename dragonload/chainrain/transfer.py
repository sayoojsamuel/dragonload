#!/usr/bin/env python3

import os.path
import shutil # this instead of mmap
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
    if os.path.exist(fileName):
        return True

    return False


def getIPAddress():
    hostName, ip_addr = get_host_details()

    return ip_addr


# NOTE: This is robust, but address reuse issue is bothering.  Also, implemen
class FileServerHandler:
    """ File Server Handler, using subprocess calls
    Usage:
        FileServerHandler.start() # To start the server
        FileServerHandler.stop() # To stop the server
    """

    fileServer = None

    # was startFileServer
    @classmethod
    def start(cls):
        """ Start the File Server """
        cls.fileServer = Popen(['python','httpServer.py'], stdout=PIPE, stderr=PIPE)
        logger.info("Initiating local file server at %s" % (HOME))

    @classmethod
    def stop(cls):
        """ Stop the File Server """
        cls.fileServer.kill()
        logger.info("Terminated local file server at %s" % (HOME))


# FIXME: hostPort
def getPart(partNumber: int, hostIP: str) -> (bool, str):
   # determine the filename
   # FIX: Database?
   filename = None
   hostPort = None # ?? from config file
   url = ":".join(hostIP, hostPort) + "/" + filename
   try:
       r = requests.get(url, stream = True)
       r.raise_for_status()
   except requests.exceptions.HTTPError as err:
       logger.fatal(err)
       return (False, None)

   logger.info("Getting part %s from user %.." % (filename, hostIP))
   fileSegmentSize = int(r.headers.get('Content-Length'))
   chunkSize = 1024
   with open(os.path.join(HOME, filename), "wb") as fp:
       pbar = tqdm(unit = "B", total = fileSegmentSize)
       for chunk in r.iter_content(chunk_size = chunkSize):
           if chunk: # filter-out keep-alive chunks
               pbar.update(len(chunk))
               fp.write(chunk)
   logger.info("Downloading complete for %s from %s" % (filename, hostIP))
   return (True, filename)




# TODO: Test mergePartitions
def mergePartitions(filename: str, total_partitions: int) -> (bool, str):

    CHUNK_SIZE = 1024 * 1024
    # make sure that all the parts exists
    fileExistStatus = True
    for part in range(total_partitions):
        partitionFilename = os.path.join(HOME, filename) + ".part" + (str(part).rjust(3, '0'))
        fileExistStatus = fileExistStatus and checkFilesExist(partitonFilename)

    if not fileExistStatus:
        logger.critical("Not all parts available in the directory: Initiating Chainrain again")
        return False, None

    """ Merger all the partitions together into one output file """
    outputFile = open(os.join(HOME, filename),'ab')

    for part in range(total_partitions):
        partitionFilename = os.path.join(HOME, filename) + ".part" + (str(part).rjust(3, '0'))
        with open(partitionFilename, 'rb') as inputFile:
            # Think why you scraped the idea of mmap
            #shutil.copyfileobj(inputFile, outputFile, CHUNK_SIZE * 10)
            while True:
                inputBuffer = inputFile.read(CHUNK_SIZE * 10)
                if not inputBuffer:
                    break
                outputFile.write(intputBuffer)
        logger.info("Completed merging part %d of %d" % (part, total_partitions))

    outputFile.close()
    logger.info("Complted merge procedure")

    assert checkFileExist(os.path.join(HOME, filename))

    return True, filename


def Handler():
    """
    Handle the proto
    """
    pass

def checkInactiveUsers():
    pass
