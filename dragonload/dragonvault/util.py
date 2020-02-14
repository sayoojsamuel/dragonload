#!/usr/bin/env python3

import socket
from dragonload.util.logging import logger

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
