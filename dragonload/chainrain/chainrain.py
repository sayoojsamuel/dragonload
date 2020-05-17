#!/usr/bin/env python3

from dragonload.util.logging import logger
from dragonload.chainrain.transfer import *

def startTransfer(filename: str, user_count: int, user_id: int, user_list):
    logger.info("Initializing chainrain")
    transferManager(filename, user_count, user_id, iuser_list)
    return True
