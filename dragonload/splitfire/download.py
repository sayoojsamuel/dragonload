#!/usr/bin/env python3

import requests
import os
from tqdm import tqdm

from dragonload.util.logging import logger


# Download Path
# Fix: expanduser vs os.environ and get home address for ~
HOME = os.path.expanduser('~/Downloads/Dragonload/')

# The total file will be split to userCount*TRESHOLD partitions
TRESHOLD: int = 5


def checkAcceptRange(url: str) -> (bool, str):
    """Return a tuple, (bool, fileSize)

    Validates if partial download is possible over the url.
    Also returns the Content-Length, and Content-Type if true
    """
    status = (False, None)

    try:
        r = requests.head(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        # sys.exit(1)
        return status

    if r.headers.get('Accept-Ranges'):
        if r.headers.get('Accept-Ranges') == "bytes":
            logger.info("Supports partial download")
            # Parse the file size from the header
            fileSize = int(r.headers.get('Content-Length'))
            return (True, fileSize)
        else:
            # Handle unsupported partial download
            logger.fatal("Unsupported partial Download for file")
    else:
        logger.warn("File not suitable for download")
    return status


def calculateByteRange(fileSize: int, parts: int):
    """Return byteRangesList

    Creates the list of partition byteRange
    """
    byteRanges = list()
    partitionSize = fileSize // parts
    current = 0
    for i in range(parts-1):
        byteRanges.append((current, current+partitionSize))
        current += partitionSize
    byteRanges.append((current, fileSize))
    return byteRanges


def checkDownloadDirectory(path: str=HOME) -> bool:
    """ Verify if the download path exist. Else create new directory"""

    if os.path.isdir(HOME):
        return True

    try:
        os.makedirs(HOME)
        logger.info("Created Dragonload directory at %s" % HOME)
    except Exception as err:
        logger.fatal("Unable to create download home directory: %s" % err)
        return False

    return True


def partitionManager(url: str, fileSize: int, user_count: int) -> bool:
    """Returns the segmentRanges for the partitions.

    This is supposed to be a multiple of activeParties
    - Manages File Names
    - Defines Byte Ranges
    - Divides Download Tasks among Parties
    """
    checkDownloadDirectory(HOME)

    filename = url.split('/')[-1]
    total_partitions = TRESHOLD * user_count

    byteRanges = calculateByteRange(fileSize, total_partitions)
    downloadStatus = list()
    # InitiateDownload
    for counter, (start, end) in enumerate(byteRanges):
        # Each partition is specified by three digit representation
        partitionFilename = filename + ".part" + (str(counter).rjust(3, '0'))
        status, successFile = downloadPart(url, start, end, partitionFilename)
        if not status:
            logger.fatal('Download Failed for %s; retrying now' % partitionFilename)
            status, successFile = downloadPart(url, start, end, partitionFilename)
        downloadStatus.append((status, successFile))
    statusList, _ = zip(*downloadStatus)
    if all(status == True for status in statusList):
        logger.info("splitfire Successfull")
    return True


def downloadPart(url: str, start: int, end: int, filename: str) -> (bool, str):
    """Returns statusCode

    Helps to download a segment of a data as filename. Uses tqdm to display progressbar
    """

    headers = {'Range' : 'bytes=%d-%d' % (start, end)}
    try:
        r = requests.get(url, headers = headers, stream = True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.fatal(err)
        return (False, None)
        # sys.exit(1)
    logger.info("Initiating download of %s" % filename)
    fileSegmentSize = int(r.headers.get('Content-Length'))
    chunkSize = 1024
    with open(os.path.join(HOME, filename), "wb") as fp:
        pbar = tqdm(unit = "B", total = fileSegmentSize)
        for chunk in r.iter_content(chunk_size = chunkSize):
            if chunk: # filter-out keep-alive new chunks; needs investigation
                pbar.update(len(chunk))
                fp.write(chunk)
    logger.info("Download completed for %s" % filename)
    return (True, filename)

    """obsolete
    with open(filename, "r+b") as fp:
        fp.seek(start)
        currentPoint = fp.tell()
        fp.write(r.content)
    """
    #return True


class Test():
    #testFileURL="https://fgig.ir/movie/2019/Aladdin-2019_480.mp4"
    testFileURL = "http://9092.ultratv100.com:9090/movies/Batch219/47%20Ronin%20%282013%29/47%20Ronin%20%282013%29.mp4"
    status, fileSize = checkAcceptRange(testFileURL)
    out = partitionManager(testFileURL, fileSize, 100)
    #if status:
    #    status, filename = downloadPart(testFileURL, 0, int(fileSize/100), "Alladin-2019.mp4.part1")
