#!/usr/bin/env python3

import logging, coloredlogs

#   class Log():
#
#       logger = None
#
#       def __init__(self):
#           self._logger = logging.getLogger("__file__"+":"+__name__)
#
#           coloredlogs.install(level="DEBUG")
#           coloredlogs.install(fmt='%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')
#           logger = self._logger
#
#       def new():
#           return self._logger
#

class Log():
    '''
    This is a wrapper for the DragonLog.
    Usage: logger = Log.new("DEBUG")
           logger.warning("Crash!!!")

    '''
    def new(logLevel):
        logger = logging.getLogger(__name__)
        if logLevel == None:
            logLevel = "DEBUG"
        coloredlogs.install(level=logLevel)
        coloredlogs.install(fmt='%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')

        return logger

logger = Log.new("DEBUG")
logger.warning("Test logger")
