#!/usr/bin/env python3

from dragonload.util.logging import logger
from dragonload.splitfire.download import *

def startDownload(url: str, user_count: int, user_id: int):
    logger.info("Initiating Splitfire")
    status, fileSize = checkAcceptRange(url)
    if status == True:
        out = partitionManager(url, fileSize, user_count, user_id)
    return out
