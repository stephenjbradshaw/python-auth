from http.server import BaseHTTPRequestHandler, HTTPServer
import controllers


class Handler(BaseHTTPRequestHandler):

    def response(self, status_code, message):
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-8'))

    def do_POST(self):
        try:
            content_type = self.headers['Content-Type']

            # Only accept JSON payloads
            if content_type != 'application/json':
                self.response(400, "Only JSON payloads allowed")
                return

            # Read the body of the request
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            # Routing
            if self.path == '/register':
                controllers.register(self, body)
            elif self.path == '/verify-email':
                controllers.verify_email(self, body)
            elif self.path == '/login':
                controllers.login(self, body)
            else:
                self.response(404, 'Not Found')
        except Exception as e:
            # Catch any exceptions not handled in the controllers
            print(e)
            self.response(500, 'Internal Server Error')


if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'server running on port {PORT}')
    server.serve_forever()
