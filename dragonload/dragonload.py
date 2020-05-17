#!/usr/bin/env python3

from dragonload.util.logging import logger

from dragonload.splitfire import splitfire
from dragonload.chainrain import chainrain

def startDragonload(url: str, user_count: int, user_id: int, user_list):
    logger.info("Starting Dragonload!")
    status, filename = splitfire.startDownload(url, user_count, user_id)
    chainrain.startTransfer(filename, user_count, user_id, user_list)
