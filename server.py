from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        bits = urlparse.urlparse(self.path)
        print urlparse.parse_qs(bits.query)


def main():
    try:
        server = HTTPServer(('', 6461), RequestHandler)
        print('Test server running...')
        server.serve_forever()
    except KeyboardInterrupt:
        print "Closing socket"
        server.socket.close()

if __name__ == '__main__':
    main()
