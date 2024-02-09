from http.server import BaseHTTPRequestHandler, HTTPServer
import controllers
import traceback


class Handler(BaseHTTPRequestHandler):
    def response(self, status_code, message):
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-8'))

    # Basic GET endpoint to check API is functioning
    def do_GET(self):
        if self.path == '/':
            self.response(200, 'OK')
        else:
            self.response(404, 'Not Found')

    # POST endpoints
    def do_POST(self):
        try:
            # Only accept JSON payloads
            content_type = self.headers['Content-Type']
            if content_type != 'application/json':
                self.response(400, "Only JSON payloads allowed")
                return

            # Read the body of the request
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            # Ensure the body is not empty
            if len(body) == 0:
                self.response(400, 'Empty request body')
                return

            # Routing
            if self.path == '/register':
                controllers.register(self, body)
            elif self.path == '/verify-email':
                controllers.verify_email(self, body)
            elif self.path == '/login':
                controllers.login(self, body)
            else:
                self.response(404, 'Not Found')

        except Exception:
            # Catch any exceptions not handled in the controllers
            print(traceback.format_exc())
            self.response(500, 'Internal Server Error')


if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'server running on port {PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print('server stopped')
