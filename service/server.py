import http.server
import urllib.parse
import socket
import threading
from logbook import Logger
import socketserver
import json
import traceback

from service.esiAccess import APIException, GenericSsoError

pyfalog = Logger(__name__)

# https://github.com/fuzzysteve/CREST-Market-Downloader/
class AuthHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path == "/favicon.ico":
            return

        parsed_path = urllib.parse.urlparse(self.path)
        parts = {k: ";".join(v) for k, v in urllib.parse.parse_qs(parsed_path.query).items()}
        is_success = False
        try:
            self.server.callback(parts)
            pyfalog.info("Successfully logged into EVE.")
            is_success = True
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        except (KeyboardInterrupt, SystemExit):
            raise
        except (GenericSsoError, APIException) as ex:
            pyfalog.error("Error logging into EVE")
            pyfalog.error(ex)
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(str.encode(str(ex)))
        except Exception as ex:
            pyfalog.error("Error logging into EVE")
            pyfalog.error(ex)
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(str.encode(str(''.join(traceback.format_tb(ex.__traceback__)))))

            # send error

        if is_success:
            self.server.stop()

    def log_message(self, format, *args):
        return


# http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/
class StoppableHTTPServer(socketserver.TCPServer):
    def server_bind(self):
        # Can't use HTTPServer due to reliance on socket.getfqdn() which seems to be bugged.
        # See https://github.com/pyfa-org/Pyfa/issues/1560#issuecomment-390095101
        socketserver.TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = host
        self.server_port = port

        # self.settings = CRESTSettings.getInstance()

        self.socket.settimeout(1)
        self.run = True

    def get_request(self):
        while self.run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return sock, addr
            except socket.timeout:
                pyfalog.warning("Server timed out waiting for connection")
                pass

    def stop(self):
        pyfalog.warning("Setting pyfa server to stop.")
        self.run = False

    def serve(self, callback=None):
        self.callback = callback
        while self.run:
            try:
                self.handle_request()
            except TypeError:
                pyfalog.debug("Caught exception in serve")
                pass

        self.server_close()


if __name__ == "__main__":
    httpd = StoppableHTTPServer(('', 6461), AuthHandler)
    t = threading.Thread(target=httpd.serve)
    input("Press <RETURN> to stop server\n")
    httpd.stop()
