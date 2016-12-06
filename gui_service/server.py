import BaseHTTPServer
import logging
import socket
import thread
import urlparse

import wx

from gui_service.settings import CRESTSettings

logger = logging.getLogger(__name__)

HTML = '''
<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
    <title>pyfa Local Server</title>
    <style type="text/css">
        body { text-align: center; padding: 150px; }
        h1 { font-size: 40px; }
        body { font: 20px Helvetica, sans-serif; color: #333; }
        #article { display: block; text-align: left; width: 650px; margin: 0 auto; }
        a { color: #dc8100; text-decoration: none; }
        a:hover { color: #333; text-decoration: none; }
    </style>
</head>

<body>

<!-- Layout from Short Circuit's CREST login. Shout out! https://github.com/farshield/shortcircuit -->
<div id="article">
    <h1>pyfa</h1>
    <div>
        <p>If you see this message then it means you should be logged into CREST. You may close this window and return to the application.</p>
    </div>
</div>
<script type="text/javascript">
function extractFromHash(name, hash) {
    var match = hash.match(new RegExp(name + "=([^&]+)"));
    return !!match && match[1];
}

var hash = window.location.hash;
var token = extractFromHash("access_token", hash);

if (token){
    var redirect = window.location.origin.concat('/?', window.location.hash.substr(1));
    window.location = redirect;
}
else {
    console.log("do nothing");
}
</script>
</body>
</html>
'''


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

        wx.CallAfter(self.server.callback, parts)

    def log_message(self, format, *args):
        return


# http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/
class StoppableHTTPServer(BaseHTTPServer.HTTPServer):
    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.settings = CRESTSettings.getInstance()

        # Allow listening for x seconds
        sec = self.settings.get('timeout')
        logger.debug("Running server for %d seconds", sec)

        self.socket.settimeout(0.5)
        self.max_tries = sec / self.socket.gettimeout()
        self.tries = 0
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

    def handle_timeout(self):
        # logger.debug("Number of tries: %d"%self.tries)
        self.tries += 1
        if self.tries == self.max_tries:
            logger.debug("Server timed out waiting for connection")
            self.stop()

    def serve(self, callback):
        self.callback = callback
        while self.run:
            try:
                self.handle_request()
            except TypeError:
                pass
        self.server_close()


if __name__ == "__main__":
    httpd = StoppableHTTPServer(('', 6461), AuthHandler)
    thread.start_new_thread(httpd.serve, ())
    raw_input("Press <RETURN> to stop server\n")
    httpd.stop()
