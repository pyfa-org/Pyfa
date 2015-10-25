import SimpleHTTPServer, BaseHTTPServer
import urlparse
import socket
import thread
import wx

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

from html import HTML

import logging

logger = logging.getLogger(__name__)

# https://github.com/fuzzysteve/CREST-Market-Downloader/
class AuthHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            return
        parsed_path = urlparse.urlparse(self.path)
        parts = urlparse.parse_qs(parsed_path.query)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(HTML)

        wx.CallAfter(pub.sendMessage, 'sso_login', message=parts)

    def log_message(self, format, *args):
        return

# http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/
class StoppableHTTPServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True

    def get_request(self):
        while self.run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self.run = False

    def serve(self):
        while self.run:
            try:
                self.handle_request()
            except TypeError:
                # this can happen if stopping server in middle of request?
                pass

if __name__ == "__main__":
    httpd = StoppableHTTPServer(('', 6461), AuthHandler)
    thread.start_new_thread(httpd.serve, ())
    raw_input("Press <RETURN> to stop server\n")
    httpd.stop()
