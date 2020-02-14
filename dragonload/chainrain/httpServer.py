#!/usr/bin/env python3

import os
import http.server
import socketserver
import functools
from dragonload.util.logging import logger

# Go for a global home
HOME = os.path.expanduser("~/Downloads/Dragonload/")
PORT = 11112

class FileServer:
    PORT = 11112
    HOME = os.path.expanduser("~/Downloads/Dragonload/")

    def __init__(self, PORT=PORT, directory=HOME):
        self.PORT = PORT
        self.Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
        self.httpd = None

    def run(self):
        with socketserver.TCPServer(("0.0.0.0", self.PORT), self.Handler) as self.httpd:
            logger.info("File Server serving at port " + str(PORT))
            self.httpd.serve_forever()
            logger.info("Terminated the File Server")

    def terminate(self):
        try:
            self.httpd.server_close()
            logger.info("Terminated the File Server")
        except Exception as err:
            logger.error("Unable to terminate the File Server: %s" % err)


fs = FileServer()
fs.run()
